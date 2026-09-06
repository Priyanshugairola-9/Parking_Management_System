from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import mysql.connector
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

def get_db_connection():
    """Create database connection with error handling"""
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="tiger",   # put your own password of sql
            database="parkings",
            autocommit=False
        )
        return db
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

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
        flash(f"Error loading statistics: {str(e)}", "danger")
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
            pid = request.form["pid"]
            pname = request.form["pname"]
            level = request.form["level"]
            total = int(request.form["total"])
            free = int(request.form["free"])
            
            # Validation
            if free > total:
                flash("Free spaces cannot exceed total spaces!", "danger")
                return redirect(url_for("add_parking"))
            
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
        except Exception as e:
            db.rollback()
            flash(f"Error adding parking: {str(e)}", "danger")
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
            vehicleno = request.form["vehicleno"].upper()
            model = request.form["model"]
            time = datetime.now().strftime("%I:%M:%S %p")

            # Check if parking exists and has space
            cursor.execute("SELECT freespace, pname FROM Park WHERE pid=%s", (pid,))
            result = cursor.fetchone()
            
            if not result:
                flash(f"❌ Invalid Parking ID: {pid}", "danger")
                return redirect(url_for("add_vehicle"))
            
            if result[0] <= 0:
                flash(f"❌ Parking '{result[1]}' is full!", "danger")
                return redirect(url_for("add_vehicle"))
            
            # Check if vehicle already parked (no departure time)
            cursor.execute(
                "SELECT pid FROM Vehicle WHERE vehicleno=%s AND departuretime IS NULL", 
                (vehicleno,)
            )
            if cursor.fetchone():
                flash(f"❌ Vehicle {vehicleno} is already parked!", "warning")
                return redirect(url_for("add_vehicle"))

            cursor.execute(
                "INSERT INTO Vehicle(pid, vehicleno, vehiclemodel, arrivaltime) VALUES (%s,%s,%s,%s)",
                (pid, vehicleno, model, time)
            )
            cursor.execute("UPDATE Park SET freespace=freespace-1 WHERE pid=%s", (pid,))
            db.commit()
            
            flash(f"✅ Vehicle {vehicleno} parked successfully at {time}!", "success")
            return redirect(url_for("view_vehicle"))
        except Exception as e:
            db.rollback()
            flash(f"Error adding vehicle: {str(e)}", "danger")
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
        flash(f"Error loading parking data: {str(e)}", "danger")
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
        cursor.execute("""
            SELECT v.pid, v.vehicleno, v.vehiclemodel, v.arrivaltime, v.departuretime, p.pname 
            FROM Vehicle v 
            LEFT JOIN Park p ON v.pid = p.pid 
            ORDER BY v.arrivaltime DESC
        """)
        vehicles = cursor.fetchall()
        return render_template("view_vehicle.html", vehicles=vehicles)
    except Exception as e:
        flash(f"Error loading vehicle data: {str(e)}", "danger")
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
        query = request.form["vehicleno"].upper()
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
            flash(f"Error searching vehicles: {str(e)}", "danger")
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
            vehicleno = request.form["vehicleno"].upper()
            exit_time_str = request.form.get("exit") or datetime.now().strftime("%I:%M:%S %p")
            rate = 20  # Rate per hour

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
            
            pid, arrival_str, model, pname = result
            
            # Calculate duration and amount
            enter_time = datetime.strptime(arrival_str, "%I:%M:%S %p")
            exit_time = datetime.strptime(exit_time_str, "%I:%M:%S %p")
            
            if exit_time < enter_time:
                exit_time += timedelta(days=1)
            
            duration = (exit_time - enter_time).total_seconds() / 3600
            amount = max(duration * rate, rate)  # Minimum 1 hour charge

            # Update database
            cursor.execute(
                "UPDATE Vehicle SET departuretime=%s WHERE vehicleno=%s AND departuretime IS NULL", 
                (exit_time_str, vehicleno)
            )
            cursor.execute("UPDATE Park SET freespace=freespace+1 WHERE pid=%s", (pid,))
            db.commit()
            
            payment_info = {
                'vehicleno': vehicleno,
                'model': model,
                'parking': pname,
                'arrival': arrival_str,
                'departure': exit_time_str,
                'duration': duration,
                'amount': amount
            }
            
            flash(f"✅ Payment successful for {vehicleno}!", "success")
            return render_template("payment.html", payment_info=payment_info)
            
        except Exception as e:
            db.rollback()
            flash(f"Error processing payment: {str(e)}", "danger")
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
        flash(f"Error deleting parking: {str(e)}", "danger")
    finally:
        cursor.close()
        db.close()
    
    return redirect(url_for("view_parking"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
