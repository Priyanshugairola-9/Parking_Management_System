# Parking_Management_System
A modern, responsive web-based parking management system built with Flask and MySQL. Features a beautiful UI with real-time statistics, mobile-friendly design, and comprehensive vehicle tracking.
## ✨ Features

### Core Functionality
- 🅿️ **Parking Management**: Add, view, and delete parking lots
- 🚗 **Vehicle Management**: Register vehicle entries and exits
- 💰 **Payment Processing**: Automatic fare calculation based on duration
- 🔍 **Vehicle Search**: Quick search by vehicle number
- 📊 **Dashboard Statistics**: Real-time parking availability and occupancy
- 📱 **Mobile Responsive**: Works perfectly on all devices

### User Interface
- 🎨 Modern gradient designs
- 🌈 Color-coded status indicators
- 📈 Visual progress bars for capacity
- ⚡ Smooth animations and transitions
- 🔔 Interactive alerts and notifications
- 💳 Professional payment receipts

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Design**: Custom CSS with gradients and animations
- **No external dependencies** for frontend (self-contained)

## 📋 Prerequisites

Before running the application, ensure you have:

- Python 3.7 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

## 🚀 Installation & Setup

### Step 1: Clone or Download the Project

```bash
# If you have the files, navigate to the project directory
cd smart-parking-system
```

### Step 2: Install Python Dependencies

```bash
pip install flask mysql-connector-python
```

Or install from requirements file:

```bash
pip install -r requirements.txt
```

### Step 3: Setup MySQL Database

1. **Start MySQL Server**
   ```bash
   # On Windows
   net start mysql
   
   # On Linux/Mac
   sudo systemctl start mysql
   # or
   sudo service mysql start
   ```

2. **Login to MySQL**
   ```bash
   mysql -u root -p
   ```

3. **Run the Database Setup Script**
   ```sql
   source database_setup.sql;
   ```
   
   Or manually execute the SQL commands from `database_setup.sql`

4. **Verify Database Creation**
   ```sql
   USE parkings;
   SHOW TABLES;
   SELECT * FROM Park;
   ```

### Step 4: Configure Database Connection

Edit `app.py` and update the database credentials if needed:

```python
db = mysql.connector.connect(
    host="localhost",
    user="root",           # Change if different
    password="",      # Change to your MySQL password
    database="parkings"
)
```

### Step 5: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## 📱 Accessing the Application

### On Your Computer
- Open browser and go to: `http://localhost:5000`

### On Mobile (Same WiFi Network)
1. Find your computer's IP address:
   ```bash
   # Windows
   ipconfig
   
   # Linux/Mac
   ifconfig
   ```

2. On your mobile browser, visit:
   ```
   http://YOUR_IP_ADDRESS:5000
   ```
   Example: `http://192.168.1.100:5000`

### On Any Device (Using Tunneling)
For accessing from anywhere, use ngrok:
```bash
# Install ngrok from https://ngrok.com/
ngrok http 5000
```
## 🔧 Troubleshooting

### Database Connection Error
```
Error: Access denied for user 'root'@'localhost'
```
**Solution**: Update MySQL password in `app.py`

### Port Already in Use
```
Error: Address already in use
```
**Solution**: Change port in `app.py`:
```python
app.run(debug=True, host="0.0.0.0", port=5001)
```

### Module Not Found Error
```
ModuleNotFoundError: No module named 'flask'
```
**Solution**: Install required packages:
```bash
pip install flask mysql-connector-python
```

### Cannot Access on Mobile
**Solution**: 
1. Ensure mobile and computer are on same WiFi
2. Disable firewall temporarily
3. Use correct IP address (not 127.0.0.1)

## 📂 Project Structure

```
smart-parking-system/
├── app.py                      # Main Flask application
├── database_setup.sql          # Database creation script
├── README.md                   # This file
├── requirements.txt            # Python dependencies
└── templates/                  # HTML templates
    ├── index.html             # Homepage with dashboard
    ├── add_parking.html       # Add parking lot form
    ├── add_vehicle.html       # Park vehicle form
    ├── view_parking.html      # View all parking lots
    ├── view_vehicle.html      # View all vehicles
    ├── search_vehicle.html    # Search vehicles
    └── payment.html           # Payment processing
```
**Note**: This system is designed to work on desktop, laptop, tablet, and mobile browsers without requiring any downloads. All styling and functionality is self-contained with no external CSS/JS frameworks required.
