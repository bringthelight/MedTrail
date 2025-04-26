from flask import Flask, render_template, request, redirect, url_for
from flask import Blueprint
from flask_mysqldb import MySQLdb,MySQL

mysql=MySQL()
data_fetch= Blueprint('data_fetch',__name__)

@data_fetch.route('/fetch',methods=['GET','POST'])
def fetch():
    cur= mysql.connection.cursor()
    
    
    cur.execute("SELECT * FROM master_unit")
    data = cur.fetchall()
    return render_template('medicine_unit.html', data=data)


# add medicines


@data_fetch.route('/add',methods=['GET','POST'])
def add():
    cur=mysql.connection.cursor()
    if request.method=='POST':
        unitname=request.form['medname']
        shname=request.form['shortname']
        cur=cur.execute("INSERT INTO master_unit (unit_name,unit_short_name) VALUES (%s, %s)", (unitname, shname,))
        
        mysql.connection.commit()
        
        return redirect(url_for('data_fetch.fetch'))
        