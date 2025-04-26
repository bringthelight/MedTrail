from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

med_name = Blueprint('med_name', __name__)
mysql = MySQL()

@med_name.route('/mednames', methods = ['GET','POST'])
def mednames():
    cur = mysql.connection.cursor()

    if request.method == "GET":
        cur.execute("SELECT med.*, type.type_name FROM master_medicine med JOIN master_medicine_type type WHERE med.type_id = type.id")
        names = cur.fetchall()

        cur.execute("SELECT id, type_name FROM master_medicine_type")
        med_types = cur.fetchall()
        
        # Fetch medicine units for dropdown
        cur.execute("SELECT id, unit_short_name FROM master_unit")
        med_units = cur.fetchall()
        
        return render_template('meds_name.html', 
                                data=names,
                                med_types=med_types,
                                med_units=med_units)
    return render_template('meds_name.html' )



@med_name.route('/med_details', methods=['POST'])
def med_details():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        medsname = request.form['medsname']
        genericname = request.form['genericname']
        medscode = request.form['medscode']
        type_id = request.form['type_id']
        unit_id = request.form['unit_id']
        strenght = request.form['strenght']
        menufecturer = request.form['menufecturer']

        cur.execute("INSERT INTO master_medicine (medicine_name, generic_name, medicine_code, type_id, unit_id, strength, manufacturer) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (medsname, genericname, medscode, type_id, unit_id, strenght, menufecturer))
        
        mysql.connection.commit()
        flash('Medicine Name added successfully!', 'success')
        return redirect(url_for('med_name.mednames'))
    
