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
    if request.method == 'POST':
        data = request.form
        res: requests.Response = requests.post(url="http://ideacentre.local:8000/signup", data=json.dumps(obj=data))
        if res.status_code == 201:
            flash(message='User registered')
            return redirect(location=url_for(endpoint='auth.signup'))
        else:
            error: str = "Cannot create user."
    return render_template(template_name_or_list='auth/signup.html', error=error)
    #     username = request.form['username']
    #     password = request.form['password']
    #     error = None

        # if not username:
        #     error = 'Username is required.'
        # elif not password:
        #     error = 'Password is required.'

        # if error is None:
        #     try:
        #         db.execute(
        #             "INSERT INTO user (username, password) VALUES (?, ?)",
        #             (username, generate_password_hash(password)),
        #         )
        #         db.commit()
        #     except db.IntegrityError:
        #         error = f"User {username} is already registered."
        #     else:
        #         return redirect(url_for("auth.login"))

        # flash(error)

    return render_template(template_name_or_list='auth/signup.html')

@bp.route(rule='/login', methods=('GET', 'POST'))
def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         db = get_db()
#         error = None
#         user = db.execute(
#             'SELECT * FROM user WHERE username = ?', (username,)
#         ).fetchone()

#         if user is None:
#             error = 'Incorrect username.'
#         elif not check_password_hash(user['password'], password):
#             error = 'Incorrect password.'

#         if error is None:
#             session.clear()
#             session['user_id'] = user['id']
#             return redirect(url_for('index'))

#         flash(error)

    return render_template(template_name_or_list='auth/login.html')

# @bp.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('index'))


# def login_required(view):
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return redirect(url_for('auth.login'))

#         return view(**kwargs)

#     return wrapped_view