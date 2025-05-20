from flask import render_template, request, redirect, url_for, flash, session, abort, Blueprint
from extensions import mysql
from auth.util import hash_pass, verify_pass  

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def dashboard():
    cur = mysql.connection.cursor()
    if request.method == "GET":
        cur.execute("SELECT COUNT(*) AS count FROM master_medicine")
        result = cur.fetchone()
        
        try:
            if isinstance(result, dict):
                medicine_count = result['count']
            else:
                medicine_count = result[0]
        except (KeyError, IndexError):
            medicine_count = 0
            
        cur.close()
        return render_template('dashboard.html', medicine_count=medicine_count)



@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM pharmacy_users WHERE email = %s", (email,))
        user = cur.fetchone()

        if user and verify_pass(password, user['password']):  
            session['loggedin'] = True
            session['user'] = user
            session['user_id'] = user['id']

            cur.execute("SELECT * FROM pharmacy_service WHERE id = %s", (user['pharmacy_service_id'],))
            pharmacy = cur.fetchone()
            session['pharmacy'] = pharmacy

            flash(f"'{ session['pharmacy']['pharmacy_name'] }' successfully logged in", 'success')
            return redirect(url_for('auth_bp.dashboard'))
        else:
            flash('Incorrect email or password, please enter correct details','warning')
    return render_template('sign-in.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        mobile=request.form['mobile']
        username=request.form['username']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form.get('user_type')
        user_role = request.form.get('user_role')
        
        print(user_type)
        print(user_role,"price")

        password = hash_pass(password)  

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO pharmacy_users (full_name,mobile, username, email, password, user_type, user_role) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                    (full_name, mobile, username, email, password, user_type, user_role))
        mysql.connection.commit()

        return redirect(url_for("auth_bp.login"))
    return render_template('sign-up.html')  


@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash('You are successfully logged out.....','success')
    return redirect(url_for('auth_bp.login'))