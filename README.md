# 🚗 Parking Management System

A web application for managing parking lots — vehicle entry and exit, live space availability, vehicle search, and automatic fee calculation.

Built with **Python (Flask)** and **MySQL**.

---

## Features

- **Parking lots** — add, view and delete lots; a lot with parked vehicles cannot be deleted
- **Vehicle entry** — registers a vehicle and reserves a space; rejects entry when the lot is full or the vehicle is already parked
- **Vehicle exit & billing** — calculates duration and fee at checkout and frees the space
- **Search** — find vehicles by full or partial number plate
- **Dashboard** — total, free and occupied spaces, and currently parked vehicles
- **History** — past visits are kept with their arrival time, departure time and amount charged

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | MySQL (`mysql-connector-python`) |
| Frontend | HTML (Jinja2 templates), CSS, JavaScript |

---

## Getting Started

### Prerequisites
- Python 3.x
- MySQL Server

### 1. Clone and install

```bash
git clone https://github.com/Priyanshugairola-9/Parking_Management_System.git
cd Parking_Management_System
python -m venv venv
venv\Scripts\activate          # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

### 2. Create the database

Open **MySQL Command Line Client** and run:

```sql
SOURCE D:/path/to/Parking_Management_System/schema.sql;
```

This creates the `parkings` database with the `Park` and `Vehicle` tables.

### 3. Set your MySQL password

The app reads the password from an environment variable — it is never stored in the code.

```powershell
# PowerShell (Windows)
$env:DB_PASSWORD="your-mysql-password"
```
```bash
# macOS/Linux
export DB_PASSWORD="your-mysql-password"
```

### 4. Run

```bash
python app.py
```

Open **http://127.0.0.1:5000/** in your browser.

---

## Fee Calculation

Rate: **₹20 per hour**, charged per started hour, minimum 1 hour.

| Stay | Charged hours | Fee |
|---|---|---|
| 10 minutes | 1 | ₹20 |
| 2 h 00 min | 2 | ₹40 |
| 2 h 01 min | 3 | ₹60 |
| 11:00 PM → 1:00 AM next day | 2 | ₹40 |
| Monday 10:00 AM → Wednesday 11:00 AM | 49 | ₹980 |

The exit time is always taken from the server clock, so the fee cannot be changed from the browser.

---

## Database Design

```
Park                          Vehicle
─────────────                 ──────────────────────
pid (PK)                      id (PK)
pname                         pid
level                         vehicleno
totalspace                    vehiclemodel
freespace                     arrivaltime    DATETIME
                              departuretime  DATETIME  (NULL = still parked)
                              amount         DECIMAL
```

Each row in `Vehicle` is one parking visit, so the same vehicle can have many past visits but only one active one.

---

## Key Design Decisions

- **Real `DATETIME` columns** — arrival and departure store the full date and time, so fees are correct for multi-day stays and records sort correctly.
- **Atomic space reservation** — entry uses `UPDATE ... SET freespace = freespace - 1 WHERE freespace > 0` and checks the affected row count. Checking and reserving happen in one statement, so two vehicles cannot take the last space at the same time.
- **Transactions** — related writes (e.g. adding a vehicle and reserving its space) are committed together and rolled back on error, so the space count stays consistent.
- **Parameterized SQL** — all queries use placeholders, which prevents SQL injection.
- **Credentials from environment variables** — no passwords in the source code.

---

## Project Structure

```
Parking_Management_System/
├── app.py              # Flask routes and application logic
├── schema.sql          # Database and table definitions
├── requirements.txt    # Python dependencies
├── templates/          # Jinja2 HTML pages
├── static/             # CSS and JavaScript
└── docs/               # Screenshots
```

---

## Known Limitations

- No login or user roles — anyone with access to the app can use every page
- A single fixed hourly rate for all lots and vehicle types
- No automated tests yet
- Payment is a checkout record only; no real payment gateway

---

## Author

**Priyanshu Gairola** — B.Tech CSE (AI & ML)
[GitHub](https://github.com/Priyanshugairola-9)
