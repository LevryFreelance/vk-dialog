# -*- coding: utf-8 -*-
__author__ = 'CubexX'
__edited_by__ = 'Hukyl'

from flask import render_template, session, \
    request, flash, get_flashed_messages, redirect

from app import app
from app.utils import get_user_session
from app.models.users import create_user, get_all_users, get_user, auth_user

@app.route('/', methods=['GET', 'POST'])
def hello():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST' and not get_user_session():
        is_valid = valid_login(request.form['username'], request.form['password'])

        if is_valid:
            return redirect('/panel')

    return render_template('login.html', errors=get_flashed_messages())


@app.route('/logout')
def logout_page():
    try:
        session.pop('user')
    except KeyError:
        pass

    return redirect('/login')


def valid_login(username, password):
    if not username or not password:
        return False

    users = get_all_users()

    # Create admin if there is no users
    if len(users) < 1:
        create_user(username, password, 1)

    # Check user exists with username/password
    user = get_user(username, password)

    # Auth user
    if user:
        auth_user(user[0])
        return True

    flash('Ошибка входа', 'error')
    return False
