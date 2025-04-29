from flask import render_template, request, redirect, url_for, flash, session
from flask import Blueprint
from flask_mysqldb import MySQL
from datetime import datetime

pharm_name = Blueprint('pharm_name', __name__)

mysql = MySQL()

@pharm_name.route('/medicines', methods=['GET'])
def med_details():
    if request.method == "GET":
        # Get medicine data with joins to related tables
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT m.id, m.medicine_name, m.generic_name, m.composition, m.strength, 
                   t.type_name, u.unit_short_name, man.manufacturer_name, m.type_id, 
                   m.unit_id, m.manufacturer_id
            FROM pharmacy_medicine m
            LEFT JOIN master_medicine_type t ON m.type_id = t.id
            LEFT JOIN master_medicine_unit u ON m.unit_id = u.id
            LEFT JOIN master_medicine_manufacturer man ON m.manufacturer_id = man.id
            ORDER BY m.id DESC
        """)
        data = cur.fetchall()
        
        # Get medicine types for dropdown
        cur.execute("SELECT * FROM master_medicine_type")
        med_types = cur.fetchall()
        
        # Get medicine units for dropdown
        cur.execute("SELECT * FROM master_medicine_unit")
        med_units = cur.fetchall()
        
        # Get manufacturers for dropdown
        cur.execute("SELECT * FROM master_medicine_manufacturer")
        manufacturers = cur.fetchall()
        
        return render_template('pharmacy_medicine.html', data=data, med_types=med_types, 
                              med_units=med_units, manu=manufacturers)

@pharm_name.route('/medicines', methods=['POST'])
def add_medicine():
    # Add new medicine
    if request.method == "POST":
        medicine_name = request.form['medsname']
        generic_name = request.form['genericname']
        composition = request.form['composition']
        strength = request.form['strenght']  # Note: keeping the typo as it exists in the form
        type_id = request.form['type_id']
        unit_id = request.form['unit_id']
        manufacturer_id = request.form['manufacturer_id']
        
        # Get user ID from session
        added_by = session.get('user_id', 1)  # Default to 1 if not in session
        current_time = datetime.now()
        
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO pharmacy_medicine 
            (medicine_name, generic_name, composition, strength, type_id, unit_id, manufacturer_id, added_by, added_date) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, 
            (medicine_name, generic_name, composition, strength, type_id, unit_id, manufacturer_id, added_by, current_time))
        mysql.connection.commit()
        
        flash('Medicine added successfully', 'success')
        return redirect(url_for('pharm_name.med_details'))

@pharm_name.route('/edit-medicine/<int:id>', methods=['POST'])
def edit_mednames(id):
    if request.method == "POST":
        medicine_name = request.form['medicine_name']
        generic_name = request.form['genericname']
        composition = request.form['composition']
        strength = request.form['strenght']  # Note: keeping the typo as it exists in the form
        type_id = request.form['type_id']
        unit_id = request.form['unit_id']
        manufacturer_id = request.form['manufacturer_id']
        
        # Get user ID from session
        updated_by = session.get('user_id', 1)  # Default to 1 if not in session
        current_time = datetime.now()
        
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE pharmacy_medicine 
            SET medicine_name = %s, generic_name = %s, composition = %s, strength = %s,
                type_id = %s, unit_id = %s, manufacturer_id = %s, 
                updated_by = %s, updated_date = %s 
            WHERE id = %s
            """, 
            (medicine_name, generic_name, composition, strength, type_id, unit_id, 
             manufacturer_id, updated_by, current_time, id))
        mysql.connection.commit()
        
        flash('Medicine updated successfully', 'success')
        return redirect(url_for('pharm_name.med_details'))

@pharm_name.route('/delete-medicine/<int:id>/<string:medicine_name>')
def delete_mednames(id, medicine_name):
    cur = mysql.connection.cursor()
    
    # Delete the medicine
    cur.execute("DELETE FROM pharmacy_medicine WHERE id = %s", (id,))
    mysql.connection.commit()
    
    flash(f'Medicine "{medicine_name}" deleted successfully', 'success')
    return redirect(url_for('pharm_name.med_details'))



# Add these routes to your pharm_name Blueprint

@pharm_name.route('/select-master-medicines', methods=['GET'])
def select_master_medicines():
    """
    Display master medicines for selection with all fields but show only medicine_name
    """
    cur = mysql.connection.cursor()
    
    # Get all fields but we'll only display medicine_name in template
    cur.execute("""
        SELECT m.*, t.type_name, u.unit_short_name, man.manufacturer_name
        FROM master_medicine m
        LEFT JOIN master_medicine_type t ON m.type_id = t.id
        LEFT JOIN master_medicine_unit u ON m.unit_id = u.id
        LEFT JOIN master_medicine_manufacturer man ON m.manufacturer_id = man.id
        ORDER BY m.medicine_name ASC
    """)
    master_medicines = cur.fetchall()
    
    return render_template('master_medicine_select.html', 
                          master_medicines=master_medicines)

@pharm_name.route('/add-from-master', methods=['POST'])
def add_from_master():
    """
    Add selected medicines with all their fields to pharmacy_medicine
    """
    if request.method == "POST":
        selected_medicines = request.form.getlist('selected_medicines')
        
        if not selected_medicines:
            flash('Please select at least one medicine',    'warning')
            return redirect(url_for('pharm_name.select_master_medicines'))
        
        cur = mysql.connection.cursor()
        success_count = 0
        already_exists = 0
        added_by = session.get('user_id', 1)
        current_time = datetime.now()
        
        for med_id in selected_medicines:
            cur.execute("SELECT id FROM pharmacy_medicine WHERE medicine_name = (SELECT medicine_name FROM master_medicine WHERE id = %s)", (med_id,))
            if cur.fetchone():
                already_exists += 1
                continue
            
            cur.execute("""
                INSERT INTO pharmacy_medicine 
                (medicine_name, generic_name, composition, strength,
                 type_id, unit_id, manufacturer_id, added_by, added_date)
                SELECT 
                    medicine_name, generic_name, composition, strength,
                    type_id, unit_id, manufacturer_id, %s, %s
                FROM master_medicine 
                WHERE id = %s
            """, (added_by, current_time, med_id))
            
            success_count += 1
        
        mysql.connection.commit()
        
        if success_count > 0:
            flash('medicine(s) added successfully', 'success')
        if already_exists > 0:
            flash('medicine(s) already exist in your list', 'warning')
            
        return redirect(url_for('pharm_name.med_details'))