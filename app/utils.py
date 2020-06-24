import hashlib
import re
from datetime import datetime

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


def get_dialog_time(dialog):
    commands = dialog[2]
    latency_min, latency_max = int(dialog[5]), int(dialog[6])
    time_start = dialog[9]
    _time = 0

    for x in parse_commands(commands):
        _time += int(x[1])

    time_min = datetime.fromtimestamp(time_start + _time + latency_min).strftime('%H:%M, %d.%m')
    time_max = datetime.fromtimestamp(time_start + _time + latency_max).strftime('%H:%M, %d.%m')

    return time_min, time_max
