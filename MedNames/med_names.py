from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

med_name = Blueprint('med_name', __name__)
mysql = MySQL()

@med_name.route('/mednames', methods = ['GET','POST'])
def mednames():
    cur = mysql.connection.cursor()

    if request.method == "GET":
        cur.execute("""
            SELECT 
                m.*,
                t.type_name,
                u.unit_short_name,
                mf.manufacturer_name
            FROM master_medicine m
            JOIN master_medicine_type t ON m.type_id = t.id
            JOIN master_medicine_unit u ON m.unit_id = u.id
            JOIN master_medicine_manufacturer mf ON m.manufacturer_id = mf.id
        """)
        data = cur.fetchall()

        cur.execute("SELECT id, type_name FROM master_medicine_type")
        med_types = cur.fetchall()
        
        cur.execute("SELECT id, unit_short_name FROM master_medicine_unit")
        med_units = cur.fetchall()

        cur.execute("SELECT id, manufacturer_name FROM master_medicine_manufacturer")
        manu=cur.fetchall()
        print(manu)
        
        return render_template('meds_name.html', 
                                data=data,
                                med_types=med_types,
                                med_units=med_units,
                                manu=manu)
    return render_template('meds_name.html' )



@med_name.route('/med_details', methods=['POST'])
def med_details():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        medsname = request.form['medsname']
        genericname = request.form['genericname']
        composition = request.form['composition']
        unit_id = request.form['unit_id']
        type_id = request.form['type_id']
        strenght = request.form['strenght']
        manufacturer_id = request.form['manufacturer_id']

        cur.execute("INSERT INTO master_medicine (medicine_name, generic_name, composition, unit_id, type_id, strength, manufacturer_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (medsname, genericname, composition, unit_id, type_id, strenght, manufacturer_id))
        
        mysql.connection.commit()
        flash('Medicine Name added successfully!', 'success')
        return redirect(url_for('med_name.mednames'))
    

@med_name.route('/edit_mednames', methods=['POST'])
def edit_mednames():

    id = request.args.get('id')
    medicine_name=request.args.get('medicine_name')
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        medicine_name = request.form['medicine_name']
        genericname = request.form['genericname']
        composition = request.form['composition']
        unit_id = request.form['unit_id']
        type_id = request.form['type_id']
        strenght = request.form['strenght']
        manufacturer_id = request.form['manufacturer_id']

        cur.execute("UPDATE master_medicine SET medicine_name=%s, generic_name=%s, composition=%s, unit_id=%s, type_id=%s, strength=%s, manufacturer_id=%s WHERE id=%s",(medicine_name, genericname, composition, unit_id, type_id, strenght, manufacturer_id, id,))
        mysql.connection.commit()

    flash(f'{medicine_name} updates successfuly......','success')
    return redirect(url_for('med_name.mednames'))
    

@med_name.route('/delete_mednames/<id>', methods=['GET','POST'])
def delete_mednames(id):
    cur = mysql.connection.cursor()

    medicine_name=request.args.get('medicine_name')


    cur.execute("DELETE FROM master_medicine WHERE id=%s", (id,))
    mysql.connection.commit()

    flash(f'{medicine_name} Deleted successfuly......','success')
    return redirect(url_for('med_name.mednames'))