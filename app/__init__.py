# -*- coding: utf-8 -*-
import sqlite3

__author__ = 'CubexX'
__edited_by__ = 'Hukyl'

# from werkzeug.contrib.fixers import ProxyFix

from flask import Flask, g, session

app = Flask(__name__, static_folder='../static')
# app.wsgi_app = ProxyFix(app.wsgi_app)
app.secret_key = 'salt123FF'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('db.sqlite3')
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def fetch_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def query_db(query, args=()):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    cur.close()
    return cur


from app.views import login, panel, dialog, users

# if __name__ == '__main__':
#     app.run()
