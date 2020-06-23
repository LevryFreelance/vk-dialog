import sqlite3

from flask import render_template, redirect, request, flash, get_flashed_messages
from app import app
from app.models.users import get_all_users, create_user, delete_user
from app.utils import get_user_session


@app.route('/users', methods=['GET', 'POST'])
def users_page():
    user = get_user_session()

    # Check login
    if not user:
        return redirect('/login')

    # Check is user admin
    if not user[3]:
        return redirect('/panel')

    if request.method == 'POST':
        try:
            if not request.form['password']:
                flash('Введите пароль', 'error')

            if not request.form['username']:
                flash('Введите юзернейм', 'error')

            if not get_flashed_messages(category_filter='error'):
                create_user(request.form['username'], request.form['password'])
        except sqlite3.IntegrityError:
            flash('Пользователь с таким юзернеймом уже существует', 'error')

    users = get_all_users()

    return render_template('users.html',
                           page='users', user=user,
                           users_list=users)


@app.route('/users/del/<int:id>')
def user_delete(id):
    user = get_user_session()

    # Check login
    if not user:
        return redirect('/login')

    # Check is user admin
    if not user[3]:
        return redirect('/panel')

    if id:
        delete_user(id)
        return redirect('/users')

    return redirect('/panel')
