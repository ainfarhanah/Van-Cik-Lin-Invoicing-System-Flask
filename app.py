import os
from flask import Flask, render_template, request, redirect, flash, url_for, session
import MySQLdb.cursors
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT", "3306"))
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'loggedin' in session:
        return redirect(url_for('dashboard'))
    
    else:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
                username = request.form['username']
                password = request.form['password']

                if not username or not password:
                    flash('Please enter username and password', 'warning')
                    return redirect(url_for('index'))
                
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
                user = cursor.fetchone()

                if user and check_password_hash(user['password'], password):
                    session['loggedin'] = True
                    session['userID'] = user['userID']
                    session['username'] = user['username']
                    flash('Logged in successfully', 'success')
                    return redirect(url_for('dashboard'))       
                else:
                    flash('Incorrect username or password!', 'danger')
                    return redirect(url_for('index'))
                
        return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'loggedin' not in session:
        if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form:
                username = request.form['username']
                email = request.form['email']
                password = request.form['password']

                if not username or not email or not password:
                    flash('Please fill out all fields', 'danger')
                    return redirect(url_for('register'))
                
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
                user = cursor.fetchone()

                if user:
                    flash('Username already exists', 'danger')
                    return redirect(url_for('register'))
                else:
                    hash_password = generate_password_hash(password)  # In a real application, you should hash the password before storing it'
                    cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)', (username, email, hash_password))
                    mysql.connection.commit()
                    cursor.close()
                    flash('You have successfully registered!', 'success')
                    return redirect(url_for('index'))
                
        return render_template('register.html')
    else:
        return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('userID',None)
    session.pop('username',None)
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))   

if __name__ == '__main__':
    app.run(debug=True)