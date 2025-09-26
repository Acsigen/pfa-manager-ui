import functools
import requests
import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint(name='dashboard', import_name=__name__, url_prefix='/dashboard')

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

@bp.route(rule='/home', methods=['GET'])
def dashboard():
    if "auth_token" not in session.keys():
        return redirect(location=url_for(endpoint='auth.login'))
    return render_template(template_name_or_list='dashboard/index.html')