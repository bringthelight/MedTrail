from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from datetime import datetime

medstock = Blueprint('medstock', __name__)
mysql = MySQL()

@medstock.route('/medstocks', methods=['GET', 'POST'])
@medstock.route('/medstocks', methods=['GET', 'POST'])
def stock():
    cur = mysql.connection.cursor()
    if request.method=='GET':
        cur.execute("SELECT stocks.*, meds.medicine_name from pharmacy_medicine meds, pharmacy_stock stocks WHERE stocks.medicine_id=meds.id")
        items = cur.fetchall()

        cur.execute("SELECT id, medicine_name FROM master_medicine")
        med_names = cur.fetchall()

        cur.execute("SELECT id, pharmacy_name FROM pharmacy_service")
        pharm_name = cur.fetchall()

        return render_template('medicine_stocks.html', 
                             items=items,
                             med_names=med_names,
                             pharm_name=pharm_name)

    return render_template('medicine_stocks.html', items = items)
        

    
