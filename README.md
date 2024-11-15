## Credit Approval System 

# Django Loan Management System

A RESTful application built using Django that manages customers, evaluates loan eligibility, and processes loans efficiently. This system provides APIs for CRUD operations, eligibility checks, and detailed loan data retrieval.

## Features

### **Customer Management**
- Add, retrieve, and manage customer details.
- Fields include first name, last name, age, monthly income, and phone number.

### **Loan Processing**
- Assess loan eligibility with dynamic interest rate adjustments.
- Approve or reject loans based on eligibility criteria.
- Store loan details, including EMIs, tenure, and repayment status.

### **Loan Data Retrieval**
- Fetch loan details by loan ID or customer ID.
- Includes repayment status and remaining installments.

---

## API Endpoints

### **Customer APIs**
- `POST /customers/`: Create a new customer.
- `GET /customers/`: Retrieve all customers.
- `GET /customers/<id>/`: Retrieve customer details by ID.

### **Loan APIs**
- `POST /check-eligibility/`: Check loan eligibility.
- `POST /process-new-loan/`: Process a new loan for an eligible customer.
- `GET /view-loan-details/<loan_id>/`: Retrieve loan details by loan ID.
- `GET /view-loan-details-by-customer-id/<customer_id>/`: Retrieve loans by customer ID.

---

## Technologies Used
- **Framework**: Django, Django REST Framework (DRF)
- **Database**: PostgreSQL
- **Language**: Python
- **Tools**: Django ORM, Decimal for precise calculations

---

## Installation

### **Prerequisites**
- Python 3.10+
- PostgreSQL
- pip (Python package manager)

### **Setup**
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-folder>

### How to setup database

-use the .env.example for refrences

### requirements and library

-Django==5.1.3
-djangorestframework==3.15.2
-psycopg2-binary==2.9.10
-python-decouple==3.8

### How to run Locally

- python manage.py runserver

### How to build a docker file

# Build a Project
-docker build -it <image_name>:<tag>

# Run the docker images

- docker run -it -p 8000:8000 <image-name>:<tag>


