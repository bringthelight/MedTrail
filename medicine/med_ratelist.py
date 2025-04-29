from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from datetime import datetime

ratelist= Blueprint('ratelist', __name__)
mysql = MySQL()

@ratelist.route('/med_ratelist', methods=['GET', 'POST'])
def medratelist():
    cur = mysql.connection.cursor()
    if request.method=='GET':
        cur.execute(
            """SELECT pharmacy_ratelist.*, pharmacy_service.pharmacy_name, pharmacy_medicine.medicine_name
            FROM pharmacy_ratelist 
            LEFT JOIN pharmacy_medicine ON pharmacy_ratelist.pharmacy_medicine_id = pharmacy_medicine.id
            LEFT JOIN pharmacy_service ON pharmacy_ratelist.pharmacy_id = pharmacy_service.id"""
            )
        items = cur.fetchall()
        # print(items)
        
        cur.execute("SELECT id, medicine_name FROM pharmacy_medicine")
        med_names = cur.fetchall()
        
        cur.execute("SELECT id, pharmacy_name FROM pharmacy_service")
        pharm_name = cur.fetchall()

        return render_template('med_ratelist.html', 
                             items=items,
                             med_names=med_names,
                             pharm_name=pharm_name)

    return render_template('med_ratelist.html', items = items)

@ratelist.route('/addmed_ratelist', methods=['POST'])
def addratelist():
    try:
        cur = mysql.connection.cursor()

        # Fetch data from form
        pharmacy_id = request.form.get('pharmacy_id')
        medicine_data = request.form.get('medicine_id')
        amount = request.form.get('amount')
        discount = request.form.get('discount')

        print("Raw medicine_data:", medicine_data)  # Debug

        # Validate all fields are received
        if not all([pharmacy_id, medicine_data, amount, discount]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('ratelist.medratelist'))

        # Split medicine_data: should be in format "id_name"
        medicine_parts = medicine_data.split('_', 1)  # split only on first _
        if len(medicine_parts) != 2:
            flash('Invalid medicine data format. Please select a valid medicine.', 'danger')
            return redirect(url_for('ratelist.medratelist'))

        pharmacy_medicine_id = medicine_parts[0]
        ratelist_name = medicine_parts[1]

        # Insert into DB
        cur.execute(
            """
            INSERT INTO pharmacy_ratelist 
            (pharmacy_id, pharmacy_medicine_id, ratelist_name, amount, discount) 
            VALUES (%s, %s, %s, %s, %s)
            """,
            (pharmacy_id, pharmacy_medicine_id, ratelist_name, amount, discount)
        )

        mysql.connection.commit()
        flash('Ratelist added successfully.', 'success')

    except Exception as e:
        mysql.connection.rollback()
        print("Error:", str(e))  # Print for terminal logs
        flash(f'Error adding ratelist: {str(e)}', 'danger')

    finally:
        cur.close()

    return redirect(url_for('ratelist.medratelist'))


    

@ratelist.route('/editratelist/<int:id>', methods=['POST'])
def editratelist(id):
    try:
        cur = mysql.connection.cursor()

        pharmacy_id = request.form.get('pharmacy_id')
        medicine_data = request.form.get('medicine_id')  # e.g. "1_Paracetamol"
        amount = request.form.get('amount')
        discount = request.form.get('discount')

        # Split the medicine data
        medicine_parts = medicine_data.split('_', 1)
        if len(medicine_parts) != 2:
            flash('Invalid medicine data format.', 'danger')
            return redirect(url_for('ratelist.medratelist'))

        pharmacy_medicine_id = medicine_parts[0]
        ratelist_name = medicine_parts[1]

        # Perform the update
        cur.execute("""
            UPDATE pharmacy_ratelist 
            SET pharmacy_id=%s, pharmacy_medicine_id=%s, ratelist_name=%s, amount=%s, discount=%s 
            WHERE id=%s
        """, (pharmacy_id, pharmacy_medicine_id, ratelist_name, amount, discount, id))

        mysql.connection.commit()
        flash('Ratelist updated successfully.', 'success')

    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error updating ratelist: {str(e)}', 'danger')

    finally:
        cur.close()

    return redirect(url_for('ratelist.medratelist'))



@ratelist.route('/ratedelete/<int:id>', methods=['GET'])
def ratedelete(id):
    cur=mysql.connection.cursor()

    # id = request.form.get('id')
    cur.execute("DELETE FROM pharmacy_ratelist WHERE id=%s", (id,))
    mysql.connection.commit()

    flash('Ratelist Deleted Successfully...','success')
    return redirect(url_for('ratelist.medratelist'))
    
