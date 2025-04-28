from flask import render_template, request, redirect, url_for, flash, session, abort, Blueprint
from flask_mysqldb import MySQL
from auth.util import hash_pass, verify_pass  

auth_bp = Blueprint('auth_bp', __name__)
mysql = MySQL()

@auth_bp.route('/', methods=['GET', 'POST'])
def dashboard():
    cur = mysql.connection.cursor()
    if request.method == "GET":
        cur.execute("SELECT * FROM master_medicine_type")
        med = cur.fetchall()
        return render_template('dashboard.html', data=med)

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
            session['user'] = user['email']
            session['user_id'] = user['id']
            return redirect(url_for('auth_bp.dashboard'))
        else:
            flash('Incorrect email or password, please enter correct details')
    return render_template('sign-in.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        mobile=request.form['mobile']
        username=request.form['username']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        user_role= request.form['user_role']

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