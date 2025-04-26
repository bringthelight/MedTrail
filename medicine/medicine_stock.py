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
        cur.connection.commit()
        print(items)

    return render_template('medicine_stocks.html', items = items)
        

    
