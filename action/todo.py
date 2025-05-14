from flask import Blueprint, render_template, redirect, url_for, session, flash
from package.db import mysql

todo = Blueprint('todo', __name__)

@todo.route('/todo_tasks', methods=['GET'])
def todo_tasks():
    if 'user' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('auth_bp.login'))
        
    return render_template('Todo_tasks.html')