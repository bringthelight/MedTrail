from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

edit_bp = Blueprint('edit_bp', __name__)
mysql = MySQL()

@edit_bp.route('/edit', methods=['POST'])
def edit():
    id = request.args.get('id')
    type_name=request.args.get('type_name')
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        type = request.form['type']
        description = request.form['description']

        cur.execute("""
            UPDATE master_medicine_type
            SET type_name=%s, description=%s
            WHERE id= %s """, (type, description, id))

        mysql.connection.commit()
        flash(f'{type_name} updated successfully!', category='success')
        return redirect(url_for('meds.meds'))
    
