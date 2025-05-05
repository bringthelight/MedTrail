from flask import render_template, request, redirect, url_for, flash, session
from flask import Blueprint
from flask_mysqldb import MySQL
from datetime import datetime

pharm_details = Blueprint('pharm_details', __name__)

mysql = MySQL()

@pharm_details.route('/pharm_details', methods=['GET','POST'])
def details():
    if request.method == "POST":
        id=request.form['id']
        service_table=request.form['service_table']
        pharmacy_name=request.form['pharmacy_name']
        pharmacy_address=request.form['pharmacy_address']
        pharmacy_city=request.form['pharmacy_city']
        pharmacy_state=request.form['pharmacy_state']
        pharmacy_pincode=request.form['pharmacy_pincode']
        pharmacy_primary_name=request.form['pharmacy_primary_name']
        pharmacy_primary_number=request.form['pharmacy_primary_number']
        pharmacy_secondary_name=request.form['pharmacy_secondary_name']
        pharmacy_secondary_number=request.form['pharmacy_secondary_number']
        pharmacy_user_count=request.form['pharmacy_user_count']
        pharmacy_email=request.form['pharmacy_email']
        pharmacy_license_number=request.form['pharmacy_license_number']
        invoice_range=request.form['invoice_range']
        
        
        cur = mysql.connection.cursor()
        cur.execute("""Select * from pharmacy_service where id,service_table,pharmacy_name,pharmacy_address,pharmacy_city,pharmacy_state,
                    pharmacy_pincode,pharmacy_primary_name,pharmacy_primary_number,pharmacy_secondary_name,pharmacy_secondary_number,
                    pharmacy_user_count,pharmacy_email,pharmacy_license_number,invoice_range VALUES(%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s)
            
        """,(id,service_table,pharmacy_name,pharmacy_address,pharmacy_city,pharmacy_state,
                    pharmacy_pincode,pharmacy_primary_name,pharmacy_primary_number,pharmacy_secondary_name,pharmacy_secondary_number,
                    pharmacy_user_count,pharmacy_email,pharmacy_license_number,invoice_range))
        cur.fetchall()
    return render_template('pharmacy_details.html')
