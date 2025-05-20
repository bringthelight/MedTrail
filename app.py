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

    # Register all blueprints
    from blueprints import register_blueprints
    register_blueprints(app)

    return app



if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000)