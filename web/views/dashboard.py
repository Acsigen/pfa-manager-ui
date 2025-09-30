from flask import (
    Blueprint, redirect, render_template, session, url_for
)

bp = Blueprint(name='dashboard', import_name=__name__, url_prefix='/dashboard')

@bp.after_request
def add_header(r):
    """
    Add headers for browser cache disabling
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