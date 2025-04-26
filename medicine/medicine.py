from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from datetime import datetime

medicine_bp = Blueprint('medicine_bp', __name__)
mysql = MySQL()

@medicine_bp.route('/medicine', methods=['GET', 'POST'])
def medicine():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        type = request.form['type']
        description = request.form['description']
        
        cur.execute("""
                INSERT INTO master_medicine_type 
                (type_name, description)
                VALUES (%s, %s)
            """, (type, description))
            
        mysql.connection.commit()
            
        flash('Medicine Type added successfully!', 'success')
        return redirect(url_for('meds.meds'))

    
