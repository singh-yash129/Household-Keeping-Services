# Household Services Application

## Overview  
This application serves as a platform for **comprehensive home servicing and solutions**, connecting **service professionals** with **customers** under the supervision of an **admin**. It is a **multi-user app** designed for efficient service request handling, professional management, and customer support.

The application is built with the following frameworks and tools:  
- **Flask**: Backend application framework  
- **Jinja2 Templates + Bootstrap**: HTML generation and styling  
- **SQLite**: Database for storing application data  

### **Key Roles**
1. **Admin (Superuser)**:  
   - Has root access to the platform.  
   - Responsible for monitoring and managing both service professionals and customers.  

2. **Service Professional**:  
   - Provides specific services like plumbing, AC repair, cleaning, etc.  
   - Manages service requests assigned to them.  

3. **Customer**:  
   - Requests household services and provides feedback.  

---

## Features  

### **Core Functionalities**

#### 1. User Authentication  
- Login/Register for **customers** and **service professionals**.  
- Admin has a pre-defined superuser account (no registration required).  
- Different forms for each user type.  
- User differentiation via a suitable data model.

#### 2. Admin Dashboard  
- Monitor and manage all users (customers and service professionals).  
- Approve service professionals after verifying their profiles.  
- Block/unblock users based on fraudulent activity or poor reviews.  
- Search professionals for review or action.  

#### 3. Service Management  
- Admin can:  
  - Create a new service with attributes like name, price, time required, and description.  
  - Update existing service details.  
  - Delete services when needed.  

#### 4. Service Requests (Customer)  
- Customers can:  
  - Search available services by name, location, or pin code.  
  - Create a new service request.  
  - Edit service requests (date, status, remarks).  
  - Close a service request upon completion.  

#### 5. Service Requests (Service Professional)  
- Service professionals can:  
  - View all service requests assigned to them.  
  - Accept or reject requests.  
  - Mark requests as completed once done.  

---

### **Recommended Functionalities**  
- API resources for interacting with users, services, and service requests.  
  - Example: Use **Flask-RESTful** for creating RESTful APIs.  
- Charts and visualizations using libraries like **ChartJS** (e.g., for user analytics or request trends).  
- Validation:  
  - Frontend: HTML5/JavaScript form validation.  
  - Backend: Controllers enforce validations.  

---

### **Optional Functionalities**  
- **Frontend Styling**:  
  - Responsive and aesthetic design using CSS and Bootstrap.  
- **Enhanced Security**:  
  - Use Flask extensions like **flask_login** or **flask_security** for secure authentication.  
- **Payment Gateway**:  
  - Integrate a dummy payment portal for ad sponsorships or booking payments.  
- Additional Features:  
  - Email/SMS notifications for service status updates.  
  - Dynamic reviews and ratings displayed for service professionals.

---

## Database Design  

### **Users Table**  
- **ID**: Primary Key  
- **Name**: User's name  
- **Role**: (Admin/Service Professional/Customer)  
- **Username**: Login credential  
- **Password**: Encrypted password  

### **Services Table**  
- **ID**: Primary Key  
- **Name**: Name of the service  
- **Base Price**: Starting cost of the service  
- **Time Required**: Approximate service time  
- **Description**: Details about the service  

### **Service Requests Table**  
- **ID**: Primary Key  
- **Service ID**: Foreign Key (references Services table)  
- **Customer ID**: Foreign Key (references Users table)  
- **Professional ID**: Foreign Key (references Users table)  
- **Date of Request**: Timestamp of request creation  
- **Date of Completion**: Timestamp of request completion  
- **Service Status**: (`requested`, `assigned`, `closed`)  
- **Remarks**: Optional comments or feedback  

---

## Getting Started  

### Prerequisites  
- Python (>= 3.7)  
- Flask (`pip install flask`)  
- SQLite  
- Bootstrap (included via CDN) 
