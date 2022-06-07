# -*- coding: utf-8 -*-

from werkzeug.security import check_password_hash, generate_password_hash

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)

from apicontrolusohpc.utils import authentication, search_group

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        error = None
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            error = "Se requiere usuario y contraseña"
        
        if error is None:
            session.clear()
            session[username] = username
            session[password] = password
            return redirect(url_for('index'))
        
    
    return render_template('_views/login.html')



@auth_bp.before_app_request
def load_logged_in_user():
    username = session.get('username')
    password = session.get('password')



@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view