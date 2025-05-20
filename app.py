from flask import Flask
import sys
import os
from config import Config, DevelopmentConfig
from extensions import mysql

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__, 
                template_folder='package/templates/',
                static_folder='package/static/', 
                static_url_path='/')

    # Apply configuration
    app.config.from_object(config_class)
    
    # Initialize extensions
    mysql.init_app(app)

    # Register blueprints
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
    from reports.expiry_report import expiry_report
    from action.api import api_bp
    from action.todo import todo

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
    app.register_blueprint(expiry_report)

    return app



if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000)