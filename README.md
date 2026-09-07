🚗 Parking Management System

A web-based Parking Management System built with Python Flask and MySQL to simplify parking operations, vehicle tracking, parking-space management, and fare calculation.

The system provides a centralized dashboard where parking administrators can monitor parking availability, manage vehicle entry and exit, search vehicle records, and calculate parking charges.

---

📌 Overview

Managing parking manually can lead to inefficient space utilization, difficult vehicle tracking, and errors in billing.

This project provides a simple web-based solution that helps manage the complete parking workflow:

Vehicle Entry
      ↓
Check Parking Availability
      ↓
Assign Parking
      ↓
Track Vehicle
      ↓
Vehicle Exit
      ↓
Calculate Parking Fee
      ↓
Update Parking Availability

The application uses Flask for the backend, MySQL for persistent data storage, and HTML/CSS/JavaScript for the frontend.

---

✨ Features

🅿️ Parking Management

- View available parking facilities
- Monitor total and available parking spaces
- Track occupied spaces
- Manage parking information

🚘 Vehicle Management

- Register vehicle entry
- Record vehicle information
- Search vehicles
- Track currently parked vehicles
- Process vehicle exit

💰 Fare Calculation

- Calculate parking charges based on parking duration
- Process vehicle exit and billing
- Maintain parking/payment information

📊 Dashboard

The dashboard provides an overview of:

- Total parking spaces
- Available spaces
- Occupied spaces
- Active vehicles
- Parking statistics

🗄️ Database Integration

The system uses MySQL for storing and managing:

- Parking information
- Vehicle records
- Parking transactions
- Payment-related information

---

🛠️ Technology Stack

Technology| Purpose
🐍 Python| Backend programming
🌐 Flask| Web framework
🗄️ MySQL| Database
🎨 HTML| Page structure
🎨 CSS| Styling and responsive UI
⚡ JavaScript| Client-side functionality
🔧 Git & GitHub| Version control

---

📂 Project Structure

Parking_Management_System/
│
├── app.py                  # Flask application and backend logic
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
├── templates/              # HTML templates
│   ├── ...
│   └── ...
│
└── static/                 # Static frontend assets
    ├── css/
    ├── js/
    └── ...

«The exact files inside "templates/" and "static/" may vary as the project evolves.»

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