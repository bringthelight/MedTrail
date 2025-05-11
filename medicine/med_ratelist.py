from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from datetime import datetime

ratelist= Blueprint('ratelist', __name__)
mysql = MySQL()


@ratelist.route('/med_ratelist', methods=['GET', 'POST'])
def medratelist():
    if 'user' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('auth_bp.login'))
    
    pharmacy_id = session['user'].get('pharmacy_service_id')
    cur = mysql.connection.cursor()
    if request.method=='GET':
        # Get ratelist with medicine details
        cur.execute(
            """SELECT pharmacy_ratelist.*, pharmacy_medicine.medicine_name
            FROM pharmacy_ratelist 
            LEFT JOIN pharmacy_medicine ON pharmacy_ratelist.pharmacy_medicine_id = pharmacy_medicine.id
            WHERE pharmacy_ratelist.pharmacy_id=%s
            """
            ,(pharmacy_id,))
        items = cur.fetchall()
        print(items, 'hahahahaha')
        
        # Get medicines specific to the pharmacy

        cur.execute("""
            SELECT id, medicine_name 
            FROM pharmacy_medicine 
            WHERE pharmacy_id=%s
        """, (pharmacy_id,))
        med_names = cur.fetchall()
        print(med_names, 'ihihihihihihihi')

        return render_template('med_ratelist.html', 
                             items=items,
                             med_names=med_names)

    return render_template('med_ratelist.html', items=items)

@ratelist.route('/addmed_ratelist', methods=['POST'])
def addratelist():
    try:
        cur = mysql.connection.cursor()

        pharmacy_id = session['user'].get('pharmacy_service_id')
        pharmacy_medicine_id = request.form.get('medicine_id')
        amount = request.form.get('amount')
        discount = request.form.get('discount')

        if not all([pharmacy_medicine_id, amount, discount]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('ratelist.medratelist'))

        # Get medicine name from pharmacy_medicine
        cur.execute("""
            SELECT medicine_name 
            FROM pharmacy_medicine 
            WHERE id=%s AND pharmacy_id=%s
        """, (pharmacy_medicine_id, pharmacy_id))
        
        medicine = cur.fetchone()
        if not medicine:
            flash('Invalid medicine selected.', 'danger')
            return redirect(url_for('ratelist.medratelist'))

        ratelist_name = medicine['medicine_name']

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
        print("Error:", str(e))
        flash(f'Error adding ratelist: {str(e)}', 'danger')

    finally:
        cur.close()

    return redirect(url_for('ratelist.medratelist'))


    

@ratelist.route('/editratelist/<int:id>', methods=['POST'])
def editratelist(id):
    try:
        cur = mysql.connection.cursor()
        pharmacy_id = session['user'].get('pharmacy_service_id')
        pharmacy_medicine_id = request.form.get('medicine_id')
        amount = request.form.get('amount')
        discount = request.form.get('discount')

        # Get medicine name
        cur.execute("""
            SELECT medicine_name 
            FROM pharmacy_medicine 
            WHERE id = %s AND pharmacy_id = %s
        """, (pharmacy_medicine_id, pharmacy_id))
        
        medicine = cur.fetchone()
        if not medicine:
            flash('Invalid medicine selected.', 'danger')
            return redirect(url_for('ratelist.medratelist'))

        ratelist_name = medicine['medicine_name']

        # Update ratelist
        cur.execute("""
            UPDATE pharmacy_ratelist 
            SET pharmacy_medicine_id = %s, 
                ratelist_name = %s,
                amount = %s, 
                discount = %s 
            WHERE id = %s AND pharmacy_id = %s
        """, (pharmacy_medicine_id, ratelist_name, amount, discount, id, pharmacy_id))

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
    
