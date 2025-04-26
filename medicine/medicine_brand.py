from flask import render_template, request, redirect, url_for, flash, session
from flask import Blueprint
from flask_mysqldb import MySQL
from datetime import datetime

brand_bp = Blueprint('brands', __name__)

mysql = MySQL()

@brand_bp.route('/brands', methods=['GET', 'POST'])
def brands():
    cur = mysql.connection.cursor()

    if request.method == "GET":
        cur.execute("SELECT * FROM medicine_brand")
        brands = cur.fetchall()
        return render_template('medicine_brand.html', data=brands)
    
    elif request.method == "POST":
       
        brand_name = request.form['brand_name']
        company = request.form['company']
        composition = request.form['composition']
        description = request.form['description']
        
        
        added_by = session.get('user_id', 1)  
        current_time = datetime.now()
        
       
        cur.execute("""
            INSERT INTO medicine_brand 
            (brand_name, company, composition, description, added_date, added_by) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """, 
            (brand_name, company, composition, description, current_time, added_by))
        mysql.connection.commit()
        
        flash('Medicine brand added successfully', 'success')
        return redirect(url_for('brands.brands'))

@brand_bp.route('/edit-brand/<int:id>', methods=['POST'])
def edit_brand(id):
    cur = mysql.connection.cursor()
    
    if request.method == "POST":
        
        brand_name = request.form['brand_name']
        company = request.form['company']
        composition = request.form['composition']
        description = request.form['description']
        
       
        updated_by = session.get('user_id', 1)  
        current_time = datetime.now()
        
        # Update database
        cur.execute("""
            UPDATE medicine_brand 
            SET brand_name = %s, company = %s, composition = %s, description = %s, 
                updated_date = %s, updated_by = %s 
            WHERE id = %s
            """, 
            (brand_name, company, composition, description, current_time, updated_by, id))
        mysql.connection.commit()
        
        flash('Medicine brand updated successfully', 'success')
        return redirect(url_for('brands.brands'))

@brand_bp.route('/delete-brand/<int:id>')
def delete_brand(id):
    cur = mysql.connection.cursor()
    
   
    cur.execute("DELETE FROM medicine_brand WHERE id = %s", (id,))
    mysql.connection.commit()
    
    flash('Medicine brand deleted successfully', 'success')
    return redirect(url_for('brands.brands'))