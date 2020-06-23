import re
from threading import Thread
from time import sleep

import requests

import app.api as api


# session = api.do_login('79771491863', 'yjzsATgkreShU', 'urauarakuzne_mail_ru:e5b5be7d59@86.62.18.14:30009')

def do_second(rows, acc1, accs2, i):
    for row in rows:
        latency = int(row[1])
        msg = row[2]

        # If sender is main account
        session = acc1[0]
        who = accs2[i][1]

        # If sender is an addition account
        if int(row[0]) == 2:
            session = accs2[i][0]
            who = acc1[1]

        sleep(latency)

        msg, forward, photo = api.get_attachments(session, msg)

        api.send_message(session, who, msg, photo, forward)


def do_async(rows, acc1, accs2):
    acc1 = api.get_sessions(acc1)
    accs2 = api.get_sessions(accs2)

    for i in range(0, len(accs2)):
        print('Start thread ', i)
        Thread(target=do_second, args=(rows, acc1, accs2, i)).start()
        sleep(5)


command_pattern = re.compile(r"(\d)\[(\d+)\]=(.*)")

with open('dialog.txt', 'r') as f:
    rows = f.read()

with open('account1.txt', 'r') as f:
    account1 = f.read()

with open('dop_accounts.txt', 'r') as f:
    dop_accounts = f.read()


def parse_commands(data):
    commands = re.findall(r"(\d)\[(\d+)\]=(.*)", data)

    return commands


def get_attachments(msg):
    forward_pattern = re.compile(r"#forward\((.*)\)#")
    photo_pattern = re.compile(r"(.*)#photo\((.*)\)#")

    forward = forward_pattern.findall(msg)
    photo = photo_pattern.findall(msg)

    if forward:
        forward = [int(i) for i in forward[0].split(',')]
        msg = ''

    if photo:
        a = photo[0]
        photo = a[1]
        msg = a[0]

    return msg, forward, photo


# Thread(target=do_async, args=(rows, account1, dop_accounts)).start()
for row in parse_commands(rows):
    print(get_attachments(row[2]))
