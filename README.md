# Van Cik Lin Invoicing System v1.0
A web based invoicing and payment tracking system built using Python Flask and MySQL for a small school van service.

This project was developed as a personal learning project to explore web development with Python while solving a real-world problem for my mom's school van service business.

By the way, this is the version 1.0 of Van Cik Lin Invoicing System

## Project Overview

This project helps manage:
- Customer information
- Invoice records
- Payment tracking
- Generate invoice in PDF
- Basic business insight through a visualization dashboard
  
Previously, all records were manage manually. This system aims to improve ogranization, reduce errors, and provide clearer visibility of monthly payments and outstanding balances.

## ERD Diagram

```mermaid
erDiagram
	direction LR
	USER {
		int id  ""  
		string username  ""  
		string email  ""  
		string password  ""  
	}

	CUSTOMERS {
		int custID  ""  
		string custName  ""  
		string custPhone  ""    
	}

	SERVICES {
		int serviceID  ""  
		string serviceName  ""  
		string serviceDesc  ""  
		float serviceFee  ""  
	}

	INVOICE {
		int invID  ""  
		date invDate  ""  
		date invDue  ""  
		id serviceID  ""  
		string invDesc  ""  
		float invAmt  ""  
		float invPaid  ""  
		float invTotal  ""  
		string invStatus  ""   
	}

	ITEMS {
		int itemID  ""  
		float itemPrice  ""  
		int itemQty  ""  
		float itemAmt  ""  
	}

	PAYMENT {
		int paymentID  ""  
		string paymentMethod  ""  
		int userID  ""  
		int invoiceID  ""  
	}

	USER||--o{INVOICE:"creates"
	INVOICE||--o{ITEMS:"has"
	INVOICE||--o{SERVICES:"has"
	INVOICE||--o{CUSTOMERS:"has"
	PAYMENT||--o{INVOICE:"has"
	CUSTOMERS||--o{PAYMENT:"pay"
```

## Tech Stack
- Backend: Python Flask
- Database: MySQL (mysqldb)
- Frontend: HTML, CSS, JavaScript
- Charting: Chart.js

## Key Features
- User Authentication: Secure login and registration
- Invoice Management: Create, view, and manage invoices
- Payment Tracking: Track payments and outstanding balances
- Dashboard: Visualize key metrics and trends
