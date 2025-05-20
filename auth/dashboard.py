from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

dash = Blueprint('dash', __name__)
mysql = MySQL()

@dash.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if 'user' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('auth_bp.login'))
    
    cur = mysql.connection.cursor()

    if request.method == 'GET':
        # Updated count query with proper WHERE clause
        cur.execute("SELECT COUNT(*) FROM master_medicine")
        medicine_count = cur.fetchall()  # Get the actual count value
        print(medicine_count,"hahahaha")
        cur.close()

        return render_template('dashboard.html', medicine_count=medicine_count)
    return redirect(url_for('auth_bp.login'))