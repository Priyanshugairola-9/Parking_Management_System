# 🚗 Parking Management System

A web-based **Parking Management System** built using **Python, Flask, MySQL, HTML, CSS, and JavaScript**.

The system provides a simple interface for managing parking facilities, recording vehicle entries and exits, monitoring parking availability, searching vehicle records, and handling parking-payment calculations.

---

## 📌 Overview

Managing parking manually can be inefficient and error-prone, especially when tracking vehicle entries, available spaces, parking duration, and payments.

This project provides a centralized web application to simplify these operations.

The system follows a basic parking workflow:

```text
Vehicle Entry
      ↓
Check Parking Availability
      ↓
Register Vehicle
      ↓
Update Available Spaces
      ↓
Vehicle Exit
      ↓
Calculate Parking Duration
      ↓
Calculate Parking Fee
      ↓
Update Parking Availability
```

The backend is developed using **Flask**, while **MySQL** is used for persistent data storage.

---

## ✨ Features

### 🅿️ Parking Management

* Add parking facilities.
* Store parking capacity information.
* Monitor available parking spaces.
* Track occupied parking spaces.
* View existing parking information.

### 🚘 Vehicle Management

* Register vehicle entry.
* Store vehicle information.
* View vehicle records.
* Search for vehicles.
* Process vehicle exits.
* Track currently active parking records.

### 💰 Payment & Fare Calculation

* Calculate parking duration.
* Calculate parking charges according to the implemented billing logic.
* Process vehicle exit.
* Update parking availability after vehicle departure.

### 📊 Dashboard

The dashboard provides an overview of the current parking situation, including:

* Total parking spaces
* Available spaces
* Occupied spaces
* Active vehicles
* Parking-related statistics

### 🗄️ MySQL Database

The application uses MySQL to persist parking and vehicle-related information.

Flask communicates with the MySQL database through the MySQL connector.

---

## 🛠️ Technology Stack

| Technology | Usage                     |
| ---------- | ------------------------- |
| 🐍 Python  | Backend programming       |
| 🌐 Flask   | Web application framework |
| 🗄️ MySQL  | Relational database       |
| HTML5      | Frontend structure        |
| CSS3       | Styling and layout        |
| JavaScript | Client-side functionality |
| Git        | Version control           |
| GitHub     | Source-code hosting       |

---

## 📂 Project Structure

```text
Parking_Management_System/
│
├── app.py                  # Main Flask application and backend logic
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
├── templates/              # HTML/Jinja2 templates
│   ├── index.html          # Dashboard / homepage
│   ├── add_parking.html    # Add parking lot
│   ├── add_vehicle.html    # Register vehicle entry
│   ├── view_parking.html   # View parking information
│   ├── view_vehicle.html   # View vehicle records
│   ├── search_vehicle.html # Search vehicle records
│   └── payment.html        # Payment/fare page
│
└── static/                 # Static frontend resources
    ├── style.css           # Application styling
    └── script.js           # Client-side JavaScript
```

---

## 🔄 Application Workflow

### 1. Add Parking

The administrator can add parking information and define the available parking capacity.

```text
Parking Information
        ↓
Parking Capacity
        ↓
Database
```

### 2. Vehicle Entry

When a vehicle enters the parking facility, the system checks whether parking space is available.

```text
Vehicle Details
      ↓
Check Availability
      ↓
Space Available?
   ↙           ↘
 Yes            No
 ↓               ↓
Register       Reject Entry
Vehicle
 ↓
Update Space
```

### 3. Vehicle Tracking

The application stores active vehicle records so that currently parked vehicles can be viewed and searched.

### 4. Vehicle Exit

When a vehicle leaves:

```text
Vehicle Record
      ↓
Exit Time
      ↓
Parking Duration
      ↓
Fare Calculation
      ↓
Payment
      ↓
Update Available Space
```

### 5. Dashboard

The dashboard retrieves current information from the database and presents the parking status to the user.

---

## 🗃️ Database Integration

The application uses **MySQL** as its relational database.

The database is responsible for maintaining information related to:

* Parking facilities
* Parking capacity
* Vehicle records
* Parking transactions
* Payment-related information

The general architecture is:

```text
                 ┌────────────────────┐
                 │     Web Browser    │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │   Flask Backend    │
                 │      app.py        │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │  MySQL Connector   │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │   MySQL Database   │
                 └────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

Install the following before running the project:

* Python 3.x
* MySQL Server
* Git
* Modern web browser

---

### 1. Clone the Repository

```bash
git clone https://github.com/Priyanshugairola-9/Parking_Management_System.git
```

Navigate into the project:

```bash
cd Parking_Management_System
```

---

### 2. Create a Virtual Environment

For Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

For macOS/Linux:

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure MySQL

Make sure your MySQL server is running.

Create/configure the required database and tables according to the database connection and queries used by the application.

Then configure the MySQL credentials in the Flask application.

> **Important:** Do not commit real database passwords or secret keys to GitHub. For production use, credentials should be stored using environment variables.

---

### 5. Run the Application

Start the Flask server:

```bash
python app.py
```

After the server starts, open the local address shown in the terminal.

Typically:

```text
http://127.0.0.1:5000/
```

---

## 🖥️ Main Application Pages

| Page           | Purpose                               |
| -------------- | ------------------------------------- |
| Dashboard      | Displays parking statistics           |
| Add Parking    | Adds parking facility information     |
| Add Vehicle    | Registers vehicle entry               |
| View Parking   | Displays parking information          |
| View Vehicle   | Displays vehicle records              |
| Search Vehicle | Searches vehicle information          |
| Payment        | Handles parking fare/payment workflow |

---

## 🧮 Parking Fee Calculation

The system calculates the parking fee when a vehicle exits.

The basic process is:

```text
Entry Time
     +
Exit Time
     ↓
Parking Duration
     ↓
Applicable Rate
     ↓
Parking Fee
```

This reduces the need for manual calculation and provides a consistent billing process.

---

## 🔍 Vehicle Search

The vehicle-search functionality allows users to locate vehicle records using the information supported by the application.

This is useful for quickly finding an existing vehicle instead of manually checking every parking record.

---

## 🔐 Security Considerations

This project is primarily intended for **educational and demonstration purposes**.

For production deployment, the following improvements should be implemented:

* Store database credentials in environment variables.
* Use a strong Flask secret key.
* Implement user authentication.
* Hash passwords using a secure password-hashing algorithm.
* Add role-based access control.
* Validate all user input.
* Add CSRF protection where required.
* Use HTTPS in production.
* Add proper database transaction handling.
* Avoid exposing sensitive configuration in source control.

---

## 🧪 Testing

The current project is primarily designed as a functional Flask application.

For a production-ready version, automated testing can be added for:

```text
tests/
│
├── test_parking.py
├── test_vehicle.py
└── test_payment.py
```

Potential test cases include:

* Adding a valid parking facility
* Rejecting invalid parking data
* Registering a vehicle
* Preventing parking when no space is available
* Searching for vehicles
* Calculating parking duration
* Calculating parking charges
* Processing vehicle exit
* Updating available parking spaces

---

## 🔮 Future Enhancements

The system can be extended with:

* 🔐 Admin and staff authentication
* 👥 Role-based access control
* 🅿️ Individual parking-slot management
* 📱 QR-code based vehicle entry
* 📷 Automatic number-plate recognition
* 📊 Advanced parking analytics
* 💰 Revenue reports
* 🧾 Digital receipts
* 🔔 Parking availability notifications
* 📈 Peak-hour analysis
* ☁️ Cloud deployment
* 🧪 Automated unit and integration testing
* 📱 Progressive Web App/mobile support

---

## 🎯 Project Objectives

The main objectives of the project are:

1. Digitize basic parking-management operations.
2. Maintain vehicle records in a centralized database.
3. Monitor parking-space availability.
4. Simplify vehicle entry and exit management.
5. Automate parking-fee calculation.
6. Reduce manual record-keeping.
7. Provide a simple web-based interface.
8. Demonstrate practical use of Flask and MySQL.

---

## 📚 Learning Outcomes

This project demonstrates practical experience with:

* Python
* Flask
* Routing
* HTTP requests
* HTML templates
* CSS
* JavaScript
* MySQL
* SQL queries
* CRUD operations
* Database connectivity
* Form handling
* Server-side processing
* Basic web application architecture
* Git and GitHub

---

## 🧠 Key Concepts Demonstrated

### Backend

```text
Flask
  ↓
Routes
  ↓
Request Handling
  ↓
Business Logic
  ↓
MySQL Queries
  ↓
Database
```

### Frontend

```text
HTML
 +
CSS
 +
JavaScript
 ↓
User Interface
```

### Full Application

```text
        FRONTEND
           │
           ▼
      Flask Routes
           │
           ▼
     Application Logic
           │
           ▼
       MySQL Database
```

---

## ⚠️ Current Project Scope

This project focuses on the core functionality required for a basic parking-management application.

It is suitable for:

* Academic projects
* Flask/MySQL learning
* Database-management demonstrations
* Web-development practice
* College project presentations

It should not be considered a production-ready parking platform without implementing additional security, authentication, testing, deployment, and scalability measures.

---

## 👨‍💻 Author

### Priyanshu Gairola

Computer Science & Engineering

GitHub:
https://github.com/Priyanshugairola-9

---

## 📄 License

This project is currently intended for educational and learning purposes.

If you plan to distribute or modify the project publicly, consider adding an appropriate open-source license such as the **MIT License**.

---

<p align="center">
  <b>🚗 Parking Management System</b>
  <br>
  Built with Python • Flask • MySQL
</p>
│
└── static/                 # Static frontend assets
    ├── style.css           # Application styling
    └── script.js           # Client-side JavaScript

---

⚙️ How It Works

1. Parking Availability

The system maintains information about parking capacity and available spaces.

When a vehicle enters:

Available Space
      ↓
Vehicle Registration
      ↓
Parking Record Created
      ↓
Available Space Decreases

When the vehicle exits:

Vehicle Found
      ↓
Parking Duration Calculated
      ↓
Parking Fee Calculated
      ↓
Parking Record Updated
      ↓
Available Space Increases

---

🧮 Parking Fee Calculation

When a vehicle exits, the application calculates the parking duration and determines the applicable parking fee according to the implemented billing logic.

This removes the need for manual calculation and reduces billing errors.

---

🗃️ Database

The application uses MySQL as its relational database.

The database stores information required for parking operations, including parking facilities, vehicle records, and parking transactions.

Basic Data Flow

Flask Application
       │
       ▼
   MySQL Connector
       │
       ▼
      MySQL
       │
       ├── Parking Data
       ├── Vehicle Data
       └── Transaction Data

---

🚀 Getting Started

Prerequisites

Make sure the following are installed:

- Python 3.x
- MySQL Server
- Git
- A web browser

---

1. Clone the Repository

git clone https://github.com/Priyanshugairola-9/Parking_Management_System.git

Move into the project directory:

cd Parking_Management_System

---

2. Create a Virtual Environment

Windows:

python -m venv venv

Activate it:

venv\Scripts\activate

For macOS/Linux:

python3 -m venv venv
source venv/bin/activate

---

3. Install Dependencies

pip install -r requirements.txt

---

4. Configure MySQL

Create the required MySQL database and configure the database connection used by the Flask application.

Make sure your MySQL server is running before starting the application.

«Security note: Never commit real database passwords, API keys, or secret keys to GitHub. Use environment variables for production deployments.»

---

5. Run the Application

python app.py

The Flask development server will start locally.

Open the application in your browser using the local address displayed by Flask, typically:

http://127.0.0.1:5000/

---

🖥️ Application Workflow

                 ┌──────────────────┐
                 │     Dashboard     │
                 └────────┬─────────┘
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
        Parking        Vehicle       Search
        Management     Entry/Exit    Vehicle
             │            │
             └──────┬─────┘
                    ▼
             Parking Database
                    │
                    ▼
             Fare Calculation
                    │
                    ▼
               Vehicle Exit

---

🔍 Example Use Case

Consider a parking facility with 100 spaces.

Initially:

Total Spaces    : 100
Available       : 100
Occupied        : 0

When a vehicle enters:

Total Spaces    : 100
Available       : 99
Occupied        : 1

When the vehicle exits, the system calculates the parking duration and fee, records the transaction, and updates the parking availability:

Total Spaces    : 100
Available       : 100
Occupied        : 0

This keeps the parking status synchronized with vehicle activity.

---

🔐 Security Considerations

For production deployment, the following improvements are recommended:

- Store database credentials in environment variables
- Use a strong Flask secret key
- Hash user passwords
- Implement authentication and authorization
- Validate and sanitize user input
- Use secure session configuration
- Add CSRF protection where appropriate
- Use HTTPS in production

The current project is primarily intended for learning, academic use, and demonstration purposes.

---

🧪 Future Improvements

The project can be extended with additional functionality such as:

- 🔐 Admin and staff authentication
- 👤 Role-based access control
- 🅿️ Individual parking-slot allocation
- 📱 QR-code based vehicle entry
- 📈 Advanced revenue analytics
- 📊 Parking usage reports
- 🔔 Notifications for parking availability
- 🧾 Digital receipts
- 📷 Automatic number-plate recognition
- ☁️ Cloud deployment
- 📱 Mobile-friendly/PWA interface
- 🧪 Automated unit and integration testing

---

🎯 Project Objectives

The primary objectives of this project are:

1. Automate basic parking-management operations.
2. Maintain vehicle and parking records digitally.
3. Monitor parking-space availability.
4. Reduce manual errors in parking management.
5. Automate parking-fee calculation.
6. Provide a simple and accessible web interface.
7. Demonstrate practical implementation of Flask and MySQL.

---

📚 Learning Outcomes

Through this project, the following concepts are demonstrated:

- Python programming
- Flask web development
- Routing and HTTP requests
- HTML/CSS/JavaScript integration
- MySQL database management
- SQL queries
- CRUD operations
- Database connectivity
- Form handling
- Server-side application logic
- Basic web application architecture
- Git and GitHub workflow

---

👨‍💻 Author

Priyanshu Gairola

Computer Science & Engineering

GitHub:
https://github.com/Priyanshugairola-9

---

⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

<p align="center">
  <b>Parking Management System</b><br>
  Built with Python • Flask • MySQL
</p>
