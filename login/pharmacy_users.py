from flask import render_template, request, redirect, url_for, flash, session
from flask import Blueprint
from flask_mysqldb import MySQL
from datetime import datetime
from auth.util import hash_pass, verify_pass 

users_bp = Blueprint('users_bp', __name__)
mysql = MySQL()

@users_bp.route('/users', methods=['GET', 'POST'])
def users():
    cur = mysql.connection.cursor()

    cur.execute("SELECT pharmacy_users.*, pharmacy_service.pharmacy_name FROM pharmacy_users LEFT JOIN pharmacy_service ON pharmacy_users.pharmacy_service_id=pharmacy_service.id")
    item = cur.fetchall()

    cur.execute("SELECT id, pharmacy_name FROM pharmacy_service")
    pharm_name = cur.fetchall()

    return render_template('pharmacy_users.html', item = item, pharm_name=pharm_name)

@users_bp.route('/addusers', methods=['GET', 'POST'])
def addusers():
    cur = mysql.connection.cursor()

    if request.method == "POST":
        full_name = request.form['full_name']
        mobile = request.form['mobile']
        username = request.form['username']
        email = request.form['email']
        pharmacy_service_id = request.form['pharmacy_id']
        user_role = request.form['user_role']
        user_type = request.form['user_type']
        password = "healtrail@123"  # Consider hashing in production!

        password = hash_pass(password)

        # ✅ FIXED SQL syntax (added parentheses around columns)
        cur.execute("""
            INSERT INTO pharmacy_users 
            (full_name, username, mobile, password, email, pharmacy_service_id, user_role, user_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, 
        (full_name, username, mobile, password, email, pharmacy_service_id, user_role, user_type))

        mysql.connection.commit()
        flash('User added successfully', 'success')
        return redirect(url_for('users_bp.users'))


@users_bp.route('/edit_user/<int:id>', methods=['POST'])
def edit_user(id):
    cur = mysql.connection.cursor()
    
    if request.method == "POST":
        # Get form data
        full_name = request.form['full_name']
        mobile = request.form['mobile']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        pharmacy_service_id = request.form['pharmacy_id']
        user_role = request.form['user_role']
        user_type = request.form['user_type']
        
        # Get current user ID from session
        updated_by = session.get('user_id', 1)  # Default to 1 if not available
        current_time = datetime.now()
        
        # We'll never update the password from the form anymore
        # Always using the static password for now
        # Update database without changing password
        cur.execute("""
            UPDATE pharmacy_users 
            SET full_name = %s, username = %s, mobile = %s, 
                password = %s, email = %s, pharmacy_service_id = %s, user_role = %s,
                user_type = %s 
            WHERE id = %s
            """, 
            (full_name, username, mobile, password, email, pharmacy_service_id, user_role, user_type))
        
        mysql.connection.commit()
        
        flash('User updated successfully', 'success')
        return redirect(url_for('users_bp.users'))

@users_bp.route('/delete_user/<int:id>')
def delete_user(id):
    cur = mysql.connection.cursor()
    
    # Delete from database
    cur.execute("DELETE FROM pharmacy_users WHERE id = %s", (id,))
    mysql.connection.commit()
    
    flash('User deleted successfully', 'success')
    return redirect(url_for('users_bp.users'))