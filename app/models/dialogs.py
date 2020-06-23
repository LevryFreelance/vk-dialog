from flask import session

from app import app, fetch_db, query_db


def create_dialog(main, add, commands, latency_from, latency_to):
    if session['user']:
        q = query_db('INSERT INTO dialogs '
                     '(owner, commands, main_account, add_accounts, '
                     'latency_from, latency_to, current_step, is_running) '
                     'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                     (session['user'][0], commands, main, add, latency_from, latency_to, 0, 1))

        return q.lastrowid


def update_dialog_running(dialog_id):
    q = query_db('UPDATE dialogs SET is_running = 0 WHERE id = ?', (dialog_id,))
    return q.rowcount


def update_dialog_step(dialog_id, step):
    q = query_db('UPDATE dialogs SET current_step = ? WHERE id = ?', (step, dialog_id))
    return q.rowcount


def get_dialogs():
    if session['user']:
        q = fetch_db('SELECT * FROM dialogs WHERE owner = ? and is_running = ? ORDER BY id DESC',
                     (session['user'][0], 1))
        return q
