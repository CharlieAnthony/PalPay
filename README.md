# Online Payment Service

An online payment service designed as a simplified version of PayPal, implemented with Django. This multi-user web application allows users to send and request payments from other registered users. Administrators can view all transactions and user accounts, while security measures ensure only authorized access to sensitive data. 

## Project Features

### User Features
- **Registration and Authentication**: Users can sign up with their personal information, choose a currency (GBP, USD, or EUR), and start with a default balance.
- **Account Management**: Users can:
  - View their transaction history (sent, received payments, and requests).
  - Check account balance.
- **Payments and Requests**: Users can:
  - Send direct payments to other users.
  - Request payments from other users, who can then accept or decline.
- **Notifications**: Users receive notifications for incoming payments and requests.

### Administrator Features
- **Admin Dashboard**: Administrators can:
  - View all user accounts and balances.
  - Monitor all payment transactions across the platform.
  - Register new administrators.

### Currency Conversion
A separate RESTful service provides currency conversion rates for user transactions. This service:
- Responds to GET requests for converting between supported currencies.
- Uses statically assigned exchange rates for simplicity.

### Security
- **Access Control**: Only registered users can access user pages; admin-only pages are restricted to administrators.
- **Authentication**: Full registration, login, and logout functionality.
- **HTTPS and Security Protections**: The application uses HTTPS and is protected against common web vulnerabilities, including:
  - Cross-Site Scripting (XSS)
  - Cross-Site Request Forgery (CSRF)
  - SQL Injection
  - Clickjacking
- **Initial Admin Setup**: An initial admin user is set up upon deployment, allowing for easy administration setup.

## System Architecture

This project follows a layered approach, separating presentation, business logic, data access, security, and web services. Each layer handles specific responsibilities to promote modularity and maintainability.

### 1. Presentation Layer
- Built using Django templates, Bootstrap, and crispy forms for a clean, user-friendly interface.
- Provides templates for:
  - Viewing transactions and account balances.
  - Sending and requesting payments.
  - Admin dashboard for user and transaction management.

### 2. Business Logic Layer
- Uses Django views to implement core functionalities, including:
  - Payment transactions and requests between users.
  - Admin features for account and transaction management.
- Ensures transaction integrity and compliance with ACID properties.

### 3. Data Access Layer
- Utilizes Django models and SQLite as the RDBMS.
- Models capture essential fields and relationships, ensuring data is handled through Django’s ORM.

### 4. Security Layer
- Implements user authentication, access control, and HTTPS.
- Secures the application against major security threats, enabling a safe multi-user environment.

### 5. Web Services
- RESTful API for currency conversion.
- Accessible via `GET` requests in the format: `/conversion/{currency1}/{currency2}/{amount_of_currency1}`.

## Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/username/online-payment-service.git
   cd online-payment-service
   ```
2. **Setup a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```
3. **Create Superuser(Admin)**:
   ```bash
   python manage.py createsuperuser
   ```
3. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

 Access the appilcation at `http://localhost:8000`

 ## License

This project is for educational purposes only and is not intended for commercial use. 
