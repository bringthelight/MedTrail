from flask import render_template, request, redirect, url_for, flash, session
from flask import Blueprint
from flask_mysqldb import MySQL

auth_bp = Blueprint('auth_bp', __name__)

mysql = MySQL()

@auth_bp.route('/', methods=['GET','POST'])
def dashboard():
    cur = mysql.connection.cursor()

    if request.method == "GET":
        cur.execute("SELECT * FROM master_medicine_type")
        med = cur.fetchall()
        return render_template('dashboard.html', data = med)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM pharmacy_users WHERE email = %s", (email,))
        user = cur.fetchone()

        if user:
            session['loggedin']=True
            session['user'] = user['email']
            session['user_id'] = user['id']
        return redirect(url_for('auth_bp.dashboard'))
    else:
        flash('Incorrect email or password, please enter correct details')
    return render_template('sign-in.html')

@auth_bp.route('/signup', methods = ['GET','POST'])
def signup():

    cur = mysql.connection.cursor()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        cur.execute("INSERT INTO master_medicine_type (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        mysql.connection.commit()


    return render_template('sign-up.html')