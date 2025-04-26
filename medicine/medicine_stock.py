from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from datetime import datetime

medstock = Blueprint('medstock', __name__)
mysql = MySQL()

@medstock.route('/medicine', methods=['GET', 'POST'])
def stock():
    cur = mysql.connection.cursor()
    if request.method=='POST':
        cur.execute("SELECT ")
        

    
