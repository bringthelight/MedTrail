from flask import render_template, request, redirect, url_for, flash, session
from flask import Blueprint
from flask_mysqldb import MySQL
from datetime import datetime
import hashlib

users_bp = Blueprint('users', __name__)

mysql = MySQL()

@users_bp.route('/users', methods=['GET', 'POST'])
def users():
    cur = mysql.connection.cursor()

    if request.method == "GET":
       
        cur.execute("SELECT u.*, p.pharmacy_name as pharmacy_name FROM pharmacy_users u , pharmacy_service p WHERE u.pharmacy_service_id = p.id")
        users = cur.fetchall()
        
        
        cur.execute("SELECT id, pharmacy_name FROM pharmacy_service")
        pharmacies = cur.fetchall()
        
        return render_template('pharmacy_users.html', data=users, pharmacies=pharmacies)
    
    elif request.method == "POST":
        
        pharmacy_id = request.form['pharmacy_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        role = request.form['role']
        
        password = "healtrail@123"
        

        added_by = session.get('user_id', 1) 
        current_time = datetime.now()
        
        # Insert into database
        cur.execute("""
            INSERT INTO pharmacy_users 
            (pharmacy_id, first_name, last_name, username, password_hash, email, phone, role, added_date, added_by) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, 
            (pharmacy_id, first_name, last_name, username, password, email, phone, role, current_time, added_by))
        mysql.connection.commit()
        
        flash('User added successfully', 'success')
        return redirect(url_for('users.users'))

@users_bp.route('/edit-user/<int:id>', methods=['POST'])
def edit_user(id):
    cur = mysql.connection.cursor()
    
    if request.method == "POST":
        # Get form data
        pharmacy_id = request.form['pharmacy_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        role = request.form['role']
        
        # Get current user ID from session
        updated_by = session.get('user_id', 1)  # Default to 1 if not available
        current_time = datetime.now()
        
        # We'll never update the password from the form anymore
        # Always using the static password for now
        # Update database without changing password
        cur.execute("""
            UPDATE pharmacy_users 
            SET pharmacy_id = %s, first_name = %s, last_name = %s, username = %s, 
                email = %s, phone = %s, role = %s,
                updated_date = %s, updated_by = %s 
            WHERE id = %s
            """, 
            (pharmacy_id, first_name, last_name, username, 
                email, phone, role, current_time, updated_by, id))
        
        mysql.connection.commit()
        
        flash('User updated successfully', 'success')
        return redirect(url_for('users.users'))

@users_bp.route('/delete-user/<int:id>')
def delete_user(id):
    cur = mysql.connection.cursor()
    
    # Delete from database
    cur.execute("DELETE FROM pharmacy_users WHERE id = %s", (id,))
    mysql.connection.commit()
    
    flash('User deleted successfully', 'success')
    return redirect(url_for('users.users'))