import hashlib
import re

from flask import session


def md5(string):
    return hashlib.md5(str(string).encode()).hexdigest()


def get_user_session():
    try:
        return session['user']
    except KeyError:
        return None


def parse_accounts(data):
    rows = data.split('\n')
    accounts = []

    for row in rows:
        row = re.sub('\r', '', row)
        row = row.split(';')

        login, password = row[0].split(':')
        proxy = row[1]

        accounts.append((login, password, proxy))

    return accounts


def parse_commands(data):
    commands = re.findall(r"(\d)\[(\d+)\]=(.*)", data)

    return commands
