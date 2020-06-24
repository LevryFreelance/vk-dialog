import random
from threading import Thread
from time import sleep

from flask import render_template, redirect, request, flash, get_flashed_messages, current_app
from app import app, api
from app.utils import get_user_session, parse_commands, parse_accounts
from app.models.dialogs import create_dialog, disable_dialog, update_dialog_step, get_dialog_by_id


@app.route('/dialog', methods=['GET', 'POST'])
def dialog_create_page():
    user = get_user_session()

    # Check login
    if not user:
        return redirect('/login')

    if request.method == 'POST':
        d = request.form

        if not d['main_account'] or not d['add_accounts'] \
                or not d['commands'] or not d['latency_from'] or not d['latency_to']:
            flash('Неверные данные', 'error')

        data = (d['main_account'],
                d['add_accounts'],
                d['commands'],
                d['latency_from'],
                d['latency_to'])

        if not get_flashed_messages(category_filter='error'):
            res = create_dialog(*data)

            if res:
                Thread(target=start_dialog_threads,
                       args=(*data, res)).start()
                return redirect('/panel')

    return render_template('dialog_create.html',
                           user=user,
                           errors=get_flashed_messages(category_filter='error'))


@app.route('/dialog/stop/<int:dialog_id>')
def dialog_stop(dialog_id):
    disable_dialog(dialog_id)
    return redirect('/panel')


def start_dialog_threads(main_account, add_accounts, commands, l_from, l_to, dialog_id):
    with app.app_context():

        commands = parse_commands(commands)
        x = parse_accounts(add_accounts)

        print(x, len(x))

        for i in range(0, len(x)):
            print('Start thread ', i)
            t = Thread(target=run_dialog, args=(commands, main_account, add_accounts, i, dialog_id))
            t.start()

            latency = random.randint(int(l_from), int(l_to))
            print('Wait {}s ...'.format(str(latency)))
            sleep(latency)

            if i == len(x) - 1:
                t.join()
                disable_dialog(dialog_id)
                print('DIALOG END')


def run_dialog(commands, main, add, i, dialog_id):
    with app.app_context():
        main_account = api.get_sessions(main)
        add_accounts = api.get_sessions(add)

        for step, row in enumerate(commands):
            d = get_dialog_by_id(dialog_id)[0]

            if not d[7]:
                print('STOP')
                return False

            latency = int(row[1])
            msg = row[2]
            sleep(latency)

            # If sender is main account
            session = main_account[0]
            who = add_accounts[i][1]

            # If sender is an addition account
            if int(row[0]) == 2:
                session = add_accounts[i][0]
                who = main_account[1]

            msg, forward, photo = api.get_attachments(session, msg)

            update_dialog_step(dialog_id, step)

            print(who, msg, photo, forward)
            api.send_message(session, who, msg, photo, forward)
