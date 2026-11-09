from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from datetime import datetime
import math
import os

app = Flask(__name__)
# CHANGED: secret key comes from an environment variable instead of being hardcoded
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-only-key")

RATE_PER_HOUR = 20   # CHANGED: one named constant instead of a number hidden inside payment()


def get_db_connection():
    """Create database connection with error handling"""
    # CHANGED: password is read from the DB_PASSWORD environment variable
    password = os.environ.get("DB_PASSWORD")
    if password is None:
        print("DB_PASSWORD is not set. In PowerShell run: $env:DB_PASSWORD=\"your-password\"")
        return None
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password,
            database="parkings",
            autocommit=False
        )
        return db
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None


def calculate_fee(arrival_time, exit_time, rate=RATE_PER_HOUR):
    """
    NEW: fee logic in its own function so it can be tested without the database.
    Charges per started hour, minimum 1 hour.
    Returns (duration_in_hours, amount).
    """
    duration_hours = (exit_time - arrival_time).total_seconds() / 3600
    billable_hours = max(1, math.ceil(duration_hours))
    return duration_hours, billable_hours * rate


def format_time(value):
    """NEW: format a datetime for display only (storage keeps the real datetime)."""
    return value.strftime("%d %b %Y, %I:%M %p")


@app.route("/")
def index():
    """Home page with dashboard stats"""
    db = get_db_connection()
    if not db:
        flash("Database connection error", "danger")
        return render_template("index.html", stats=None)

    cursor = db.cursor()
    try:
        # Get statistics
        cursor.execute("SELECT COUNT(*) FROM Park")
        total_parkings = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(totalspace), SUM(freespace) FROM Park")
        spaces = cursor.fetchone()
        total_spaces = spaces[0] or 0
        free_spaces = spaces[1] or 0
        occupied_spaces = total_spaces - free_spaces

        cursor.execute("SELECT COUNT(*) FROM Vehicle WHERE departuretime IS NULL")
        active_vehicles = cursor.fetchone()[0]

        stats = {
            'total_parkings': total_parkings,
            'total_spaces': total_spaces,
            'free_spaces': free_spaces,
            'occupied_spaces': occupied_spaces,
            'active_vehicles': active_vehicles
        }

        return render_template("index.html", stats=stats)
    except Exception as e:
        print(f"index error: {e}")   # CHANGED: details go to the terminal, not to the user
        flash("Could not load statistics.", "danger")
        return render_template("index.html", stats=None)
    finally:
        cursor.close()
        db.close()


@app.route("/add_parking", methods=["GET", "POST"])
def add_parking():
    """Add new parking lot"""
    if request.method == "POST":
        db = get_db_connection()
        if not db:
            flash("Database connection error", "danger")
            return redirect(url_for("add_parking"))

        cursor = db.cursor()
        try:
            pid = int(request.form["pid"])        # CHANGED: pid is an INT in schema.sql
            pname = request.form["pname"]
            level = request.form["level"]
            total = int(request.form["total"])

            # CHANGED: validate total, and a new lot always starts empty (free = total).
            # The "free" field from the form is ignored on purpose.
            if total <= 0:
                flash("Total spaces must be greater than 0!", "danger")
                return redirect(url_for("add_parking"))
            free = total

            # Check if parking ID already exists
            cursor.execute("SELECT pid FROM Park WHERE pid=%s", (pid,))
            if cursor.fetchone():
                flash(f"Parking ID {pid} already exists!", "danger")
                return redirect(url_for("add_parking"))

            cursor.execute(
                "INSERT INTO Park (pid, pname, level, totalspace, freespace) VALUES (%s,%s,%s,%s,%s)",
                (pid, pname, level, total, free)
            )
            db.commit()
            flash(f"✅ Parking '{pname}' added successfully!", "success")
            return redirect(url_for("view_parking"))
        except ValueError:
            # NEW: non-numeric pid/total gives a clear message instead of a crash text
            db.rollback()
            flash("Parking ID and total spaces must be whole numbers.", "danger")
            return redirect(url_for("add_parking"))
        except Exception as e:
            db.rollback()
            print(f"add_parking error: {e}")
            flash("Could not add parking. Please try again.", "danger")
            return redirect(url_for("add_parking"))
        finally:
            cursor.close()
            db.close()

    return render_template("add_parking.html")


@app.route("/add_vehicle", methods=["GET", "POST"])
def add_vehicle():
    """Add vehicle to parking"""
    if request.method == "POST":
        db = get_db_connection()
        if not db:
            flash("Database connection error", "danger")
            return redirect(url_for("add_vehicle"))

        cursor = db.cursor()
        try:
            pid = request.form["pid"]
            vehicleno = request.form["vehicleno"].strip().upper()
            model = request.form["model"]
            arrival_time = datetime.now()   # CHANGED: store a real datetime (with the date)

            # Check if parking exists
            cursor.execute("SELECT pname FROM Park WHERE pid=%s", (pid,))
            result = cursor.fetchone()

            if not result:
                flash(f"❌ Invalid Parking ID: {pid}", "danger")
                return redirect(url_for("add_vehicle"))
            pname = result[0]

            # Check if vehicle already parked (no departure time)
            cursor.execute(
                "SELECT pid FROM Vehicle WHERE vehicleno=%s AND departuretime IS NULL",
                (vehicleno,)
            )
            if cursor.fetchone():
                flash(f"❌ Vehicle {vehicleno} is already parked!", "warning")
                return redirect(url_for("add_vehicle"))

            # CHANGED: check-and-reserve a space in ONE statement (fixes the race condition).
            # If no row was updated, the lot is full.
            cursor.execute(
                "UPDATE Park SET freespace = freespace - 1 WHERE pid=%s AND freespace > 0",
                (pid,)
            )
            if cursor.rowcount == 0:
                db.rollback()
                flash(f"❌ Parking '{pname}' is full!", "danger")
                return redirect(url_for("add_vehicle"))

            cursor.execute(
                "INSERT INTO Vehicle(pid, vehicleno, vehiclemodel, arrivaltime) VALUES (%s,%s,%s,%s)",
                (pid, vehicleno, model, arrival_time)
            )
            db.commit()

            flash(f"✅ Vehicle {vehicleno} parked successfully at {format_time(arrival_time)}!", "success")
            return redirect(url_for("view_vehicle"))
        except Exception as e:
            db.rollback()
            print(f"add_vehicle error: {e}")
            flash("Could not add vehicle. Please try again.", "danger")
            return redirect(url_for("add_vehicle"))
        finally:
            cursor.close()
            db.close()

    return render_template("add_vehicle.html")


@app.route("/view_parking")
def view_parking():
    """View all parking lots"""
    db = get_db_connection()
    if not db:
        flash("Database connection error", "danger")
        return render_template("view_parking.html", parks=[])

    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM Park ORDER BY pid")
        data = cursor.fetchall()
        return render_template("view_parking.html", parks=data)
    except Exception as e:
        print(f"view_parking error: {e}")
        flash("Could not load parking data.", "danger")
        return render_template("view_parking.html", parks=[])
    finally:
        cursor.close()
        db.close()


@app.route("/view_vehicle")
def view_vehicle():
    """View all vehicles"""
    db = get_db_connection()
    if not db:
        flash("Database connection error", "danger")
        return render_template("view_vehicle.html", vehicles=[])

    cursor = db.cursor()
    try:
        # Unchanged query; ORDER BY now sorts correctly because arrivaltime is a DATETIME
        cursor.execute("""
            SELECT v.pid, v.vehicleno, v.vehiclemodel, v.arrivaltime, v.departuretime, p.pname
            FROM Vehicle v
            LEFT JOIN Park p ON v.pid = p.pid
            ORDER BY v.arrivaltime DESC
        """)
        vehicles = cursor.fetchall()
        return render_template("view_vehicle.html", vehicles=vehicles)
    except Exception as e:
        print(f"view_vehicle error: {e}")
        flash("Could not load vehicle data.", "danger")
        return render_template("view_vehicle.html", vehicles=[])
    finally:
        cursor.close()
        db.close()


@app.route("/search_vehicle", methods=["GET", "POST"])
def search_vehicle():
    """Search for vehicles"""
    vehicles = []
    query = ""

    if request.method == "POST":
        query = request.form["vehicleno"].strip().upper()
        db = get_db_connection()

        if not db:
            flash("Database connection error", "danger")
            return render_template("search_vehicle.html", vehicles=[], query=query)

        cursor = db.cursor()
        try:
            cursor.execute("""
                SELECT v.pid, v.vehicleno, v.vehiclemodel, v.arrivaltime, v.departuretime, p.pname
                FROM Vehicle v
                LEFT JOIN Park p ON v.pid = p.pid
                WHERE v.vehicleno LIKE %s
                ORDER BY v.arrivaltime DESC
            """, (f"%{query}%",))
            vehicles = cursor.fetchall()

            if not vehicles:
                flash(f"No vehicles found matching '{query}'", "info")
        except Exception as e:
            print(f"search_vehicle error: {e}")
            flash("Search failed. Please try again.", "danger")
        finally:
            cursor.close()
            db.close()

    return render_template("search_vehicle.html", vehicles=vehicles, query=query)


@app.route("/payment", methods=["GET", "POST"])
def payment():
    """Process vehicle exit and payment"""
    if request.method == "POST":
        db = get_db_connection()
        if not db:
            flash("Database connection error", "danger")
            return render_template("payment.html")

        cursor = db.cursor()
        try:
            vehicleno = request.form["vehicleno"].strip().upper()
            # CHANGED: exit time is always the server's current time.
            # The "exit" field from the form is ignored, so users cannot pick their own fee.
            exit_time = datetime.now()

            # Get vehicle details
            cursor.execute("""
                SELECT v.pid, v.arrivaltime, v.vehiclemodel, p.pname
                FROM Vehicle v
                LEFT JOIN Park p ON v.pid = p.pid
                WHERE v.vehicleno=%s AND v.departuretime IS NULL
            """, (vehicleno,))
            result = cursor.fetchone()

            if not result:
                flash(f"❌ Vehicle {vehicleno} not found or already checked out!", "danger")
                return render_template("payment.html")

            # arrival_time comes back from MySQL as a datetime object (DATETIME column)
            pid, arrival_time, model, pname = result

            # CHANGED: correct for any length of stay (multi-day included)
            duration_hours, amount = calculate_fee(arrival_time, exit_time)

            # CHANGED: also save the amount, so there is a record of revenue
            cursor.execute(
                "UPDATE Vehicle SET departuretime=%s, amount=%s WHERE vehicleno=%s AND departuretime IS NULL",
                (exit_time, amount, vehicleno)
            )
            cursor.execute("UPDATE Park SET freespace=freespace+1 WHERE pid=%s", (pid,))
            db.commit()

            payment_info = {
                'vehicleno': vehicleno,
                'model': model,
                'parking': pname,
                'arrival': format_time(arrival_time),
                'departure': format_time(exit_time),
                'duration': round(duration_hours, 2),
                'amount': amount
            }

            flash(f"✅ Payment successful for {vehicleno}!", "success")
            return render_template("payment.html", payment_info=payment_info)

        except Exception as e:
            db.rollback()
            print(f"payment error: {e}")
            flash("Could not process payment. Please try again.", "danger")
            return render_template("payment.html")
        finally:
            cursor.close()
            db.close()

    return render_template("payment.html")


@app.route("/delete_parking/<int:pid>", methods=["POST"])
def delete_parking(pid):
    """Delete parking lot"""
    db = get_db_connection()
    if not db:
        flash("Database connection error", "danger")
        return redirect(url_for("view_parking"))

    cursor = db.cursor()
    try:
        # Check if there are active vehicles
        cursor.execute("SELECT COUNT(*) FROM Vehicle WHERE pid=%s AND departuretime IS NULL", (pid,))
        active_count = cursor.fetchone()[0]

        if active_count > 0:
            flash(f"Cannot delete parking with {active_count} active vehicle(s)!", "danger")
            return redirect(url_for("view_parking"))

        cursor.execute("DELETE FROM Park WHERE pid=%s", (pid,))
        db.commit()
        flash(f"✅ Parking {pid} deleted successfully!", "success")
    except Exception as e:
        db.rollback()
        print(f"delete_parking error: {e}")
        flash("Could not delete parking.", "danger")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for("view_parking"))


if __name__ == "__main__":
    # CHANGED: no host="0.0.0.0", so the debugger is only reachable from this computer
    app.run(debug=True)
