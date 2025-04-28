from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from datetime import datetime

medicine_bp = Blueprint('medicine_bp', __name__)
mysql = MySQL()

@medicine_bp.route('/medicine', methods=['GET', 'POST'])
def medicine():
    cur = mysql.connection.cursor()

    if 'user' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('auth_bp.login')) 

    if request.method == 'POST':
        type = request.form['type']
        description = request.form['description']
        added_by = session['user']['full_name']
        updated_by = session['user']['full_name']
        
        cur.execute("""
                INSERT INTO master_medicine_type 
                (type_name, description, added_by, updated_by)
                VALUES (%s, %s, %s, %s)
            """, (type, description, added_by, updated_by))
            
        mysql.connection.commit()
            
        flash('Medicine Type added successfully!', 'success')
        return redirect(url_for('meds.meds'))

    
