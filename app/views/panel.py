from flask import render_template, redirect
from app import app
from app.utils import get_user_session
from app.models.dialogs import get_dialogs


@app.route('/panel')
def panel_page():
    user = get_user_session()

    # Check login
    if not user:
        return redirect('/login')

    dialogs = get_dialogs()

    return render_template('panel.html',
                           page='panel', user=user,
                           dialogs=dialogs)
