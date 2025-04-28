from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from datetime import datetime

medstock = Blueprint('medstock', __name__)
mysql = MySQL()

@medstock.route('/medstocks', methods=['GET', 'POST'])
def stock():
    cur = mysql.connection.cursor()
    if request.method=='GET':
        cur.execute(
            """SELECT pharmacy_stock.*, master_medicine.medicine_name, pharmacy_service.pharmacy_name 
            FROM pharmacy_stock 
            JOIN master_medicine ON pharmacy_stock.medicine_id = master_medicine.id 
            JOIN pharmacy_service ON pharmacy_stock.pharmacy_id = pharmacy_service.id"""
            )
        items = cur.fetchall()
        print(items)

        cur.execute("SELECT id, medicine_name FROM master_medicine")
        med_names = cur.fetchall()

        cur.execute("SELECT id, pharmacy_name FROM pharmacy_service")
        pharm_name = cur.fetchall()

        return render_template('medicine_stocks.html', 
                             items=items,
                             med_names=med_names,
                             pharm_name=pharm_name)

    return render_template('medicine_stocks.html', items = items)

@medstock.route('/addmedstock', methods=['POST'])
def addmedstock():
    cur = mysql.connection.cursor()

    if request.method=='POST':
        pharmacy_id = request.form['pharmacy_id']
        medicine_id  = request.form['medicine_id']
        quantity = request.form['quantity']
        batch_number = request.form['batch_number']
        expiry_date = request.form['expiry_date']
        purchase_price = request.form['purchase_price']
        selling_price = request.form['selling_price']

        cur.execute("INSERT INTO pharmacy_stock (pharmacy_id, medicine_id, quantity, batch_number, expiry_date, purchase_price, selling_price) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                    (pharmacy_id, medicine_id, quantity, batch_number, expiry_date, purchase_price, selling_price))
        
        mysql.connection.commit()
        flash('Stock added successfully....','success')
        return redirect(url_for('medstock.stock'))

        

    
