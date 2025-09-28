import functools
import requests

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint(name='clients', import_name=__name__, url_prefix='/clients')

@bp.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@bp.route(rule='/', methods=('GET', 'POST'))
def clients():
    error = ""
    if "auth_token" not in session.keys():
        return redirect(location=url_for(endpoint='auth.login'))
    if request.method == 'POST':
        data = request.form.to_dict()
        headers = {
            "Authorization": f"Bearer {session.get("auth_token")}"
        }
        res: requests.Response = requests.post(url="http://ideacentre.local:8000/clients", data=data, headers=headers)
        if res.status_code == 201:
            flash(message='Client Added')
            return redirect(location=url_for(endpoint='clients.clients'))
        else:
            error: str = "Cannot register client."

    client_list: list[dict] = []
    headers = {
        "Authorization": f"Bearer {session.get("auth_token")}"
    }
    res: requests.Response = requests.get(url="http://ideacentre.local:8000/api/v1/clients", headers=headers)
    if res.status_code == 200:
        client_list = res.json()
    else:
        error: str = "Cannot display clients"
        return render_template(template_name_or_list='clients/client_list.html', error=error)
    return render_template(template_name_or_list='clients/client_list.html', error=error, client_list=client_list)
