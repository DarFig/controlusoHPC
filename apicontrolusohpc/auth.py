# -*- coding: utf-8 -*-

import functools

from werkzeug.security import check_password_hash, generate_password_hash

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)

from apicontrolusohpc.utils import authentication, search_group

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


#/auth/login
@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        error = None
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            error = "Se requiere usuario y contraseña"
        else:
            user_data = authentication(username, password)
            if user_data == "error":
                error = "fallo de autenticación"
            else:
                group = search_group(user_data)

        if error is None:
            session.clear()
            session["username"] = username
            session["group"] = group
            #print(group)
            return redirect(url_for('index'))
        
        #print(error) 
    return render_template("_views/login.html")



@auth_bp.before_app_request
def load_logged_in_user():
    username = session.get('username')
    group = session.get('group')

    if username is None:
        g.user = None
    else:
        g.user = username


#/auth/logout
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
