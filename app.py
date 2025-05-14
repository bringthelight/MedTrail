from flask import Flask
from auth.auth import auth_bp
from medicine.medicine import medicine_bp
from delete_edit.delete import delete_bp
from delete_edit.edit import edit_bp
from medicine.med_type import med_bp
from MedNames.med_names import med_name
from data_fetch.route import data_fetch
from action.edit import edit
from login.pharmacy_users import users_bp
from medicine.medicine_brand import brand_bp
from medicine.pharmacy_med import pharm_name
from medicine.medicine_stock import medstock
from medicine.med_ratelist import ratelist
from Billing.billing_route import billing
from Billing.stock_report import lowstock
from Billing.business_report import report_bp
from medicine.pharmacy_details import pharm_details
from action.api import api_bp
from action.todo import todo
from flask_mysqldb import MySQL
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, template_folder='package/templates/', static_folder='package/static/', static_url_path='/')


mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  
app.config['MYSQL_PASSWORD'] = ''  
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_DB'] = 'healtrail_pharmacy'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = 'sdfsdfsdgsdewt4ww345gert34'

app.register_blueprint(auth_bp)
app.register_blueprint(data_fetch)
app.register_blueprint(edit)
app.register_blueprint(medicine_bp)
app.register_blueprint(delete_bp)
app.register_blueprint(edit_bp)
app.register_blueprint(med_bp)
app.register_blueprint(med_name)
app.register_blueprint(pharm_name)
app.register_blueprint(users_bp)
app.register_blueprint(brand_bp)
app.register_blueprint(medstock)
app.register_blueprint(ratelist)
app.register_blueprint(billing)
app.register_blueprint(pharm_details)
app.register_blueprint(lowstock)
app.register_blueprint(report_bp)
app.register_blueprint(api_bp)
app.register_blueprint(todo)



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,debug=True)