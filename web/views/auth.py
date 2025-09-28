import functools
import requests
import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('auth', __name__, url_prefix='/auth')

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

@bp.route(rule='/signup', methods=('GET', 'POST'))
def signup():
    error = ""
    if "auth_token" not in session.keys():
        if request.method == 'POST':
            data = request.form
            res: requests.Response = requests.post(url="http://ideacentre.local:8000/signup", data=json.dumps(obj=data))
            if res.status_code == 201:
                flash(message='User registered')
                return redirect(location=url_for(endpoint='auth.signup'))
            else:
                error: str = "Cannot create user."
        return render_template(template_name_or_list='auth/signup.html', error=error)
    return redirect(location=url_for(endpoint='auth.login'))

@bp.route(rule='/login', methods=('GET', 'POST'))
def login():
    error = ""
    # TODO: Check token validity before redirect. We might have an expired token. We will need an endpoint from the API to validate our token externally not only internally
    if "auth_token" not in session.keys():
        if request.method == 'POST':
            data = request.form.to_dict()
            data["grant_type"] = "password"
            headers = {
                "accept": "application/json"
            }
            res: requests.Response = requests.post(url="http://ideacentre.local:8000/auth", data=data, headers=headers)
            if res.status_code == 200:
                session["auth_token"] = res.json()["access_token"]
                return redirect(location=url_for(endpoint='dashboard.dashboard'))
            else:
                error: str = "Invalid Credentials"
        return render_template(template_name_or_list='auth/login.html', error=error)
    return redirect(location=url_for(endpoint='dashboard.dashboard'))


@bp.route(rule='/logout', methods=["GET"])
def logout():
    session.clear()
    return redirect(location=url_for(endpoint='auth.login'))


# def login_required(view):
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return redirect(url_for('auth.login'))

#         return view(**kwargs)

#     return wrapped_view