from flask import render_template, redirect
from app import app
from app.utils import get_user_session, get_dialog_time
from app.models.dialogs import get_dialogs


@app.route('/panel')
def panel_page():
    user = get_user_session()

    # Check login
    if not user:
        return redirect('/login')

    dialogs = get_dialogs()
    dialogs_time = {}

    for d in dialogs:
        dialogs_time[d[0]] = get_dialog_time(d)

    return render_template('panel.html',
                           page='panel', user=user,
                           dialogs=dialogs,
                           dialogs_time=dialogs_time)
