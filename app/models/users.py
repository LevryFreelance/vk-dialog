from flask import session

from app import app, fetch_db, query_db
from app.utils import md5


def create_user(username, password, is_admin=0):
    query_db('INSERT INTO users (username, password, is_admin) '
             'VALUES (?, ?, ?)', (username, md5(password), is_admin))


def delete_user(uid):
    query_db('DELETE FROM users WHERE id = ?', (int(uid),))


def get_all_users():
    return fetch_db('select * from users ORDER BY id DESC')


def get_user(username, password):
    return fetch_db('select * from users where username=? and password=?',
                    (username, md5(password)))


def auth_user(user):
    session['user'] = user
    return session['user']
