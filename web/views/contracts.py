# import functools
import requests
import json

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)

bp = Blueprint(name='contracts', import_name=__name__)

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

@bp.route(rule='/clients/<int:client_id>/contracts', methods=['GET'])
def contracts(client_id: int):
    error = ""
    if "auth_token" not in session.keys():
        return redirect(location=url_for(endpoint='auth.login'))
    
    contract_list: list[dict] = []
    headers = {
        "Authorization": f"Bearer {session.get("auth_token")}"
    }
    res: requests.Response = requests.get(url=f"http://ideacentre.local:8000/api/v1/clients/{client_id}/contracts", headers=headers)
    if res.status_code == 200:
        contract_list = res.json()
    elif res.status_code == 401:
        session.clear()
        return redirect(location=url_for(endpoint='auth.login'))
    else:
        error: str = "Cannot display contracts"
        return render_template(template_name_or_list='contracts/list.html', error=error)
    
    return render_template(template_name_or_list='contracts/list.html', error=error, contract_list=contract_list, client_id=client_id)

@bp.route(rule='/clients/<int:client_id>/contracts/add', methods=('GET','POST'))
def add(client_id: int):
    error = ""
    if "auth_token" not in session.keys():
        return redirect(location=url_for(endpoint='auth.login'))
    if request.method == 'POST':
        data = request.form.to_dict()
        headers = {
            "Authorization": f"Bearer {session.get("auth_token")}"
        }
        res: requests.Response = requests.post(url=f"http://ideacentre.local:8000/api/v1/clients/{client_id}/contracts", data=json.dumps(obj=data), headers=headers)
        # TODO: Change this once the bug on the API is fixed. It returns 200 instead of 201
        if res.status_code == 200:
            flash(message='Contract Added')
            return redirect(location=url_for(endpoint='contracts.contracts', client_id=client_id))
        elif res.status_code == 401:
            session.clear()
            return redirect(location=url_for(endpoint='auth.login'))
        else:
            error: str = "Cannot register contract."
    return render_template(template_name_or_list='contracts/new.html', error=error, client_id=client_id)

@bp.route(rule='/clients/<int:client_id>/contracts/<int:contract_id>/view', methods=['GET'])
def view(client_id: int, contract_id: int):
    error = ""
    if "auth_token" not in session.keys():
        return redirect(location=url_for(endpoint='auth.login'))

    headers = {
        "Authorization": f"Bearer {session.get("auth_token")}"
    }
    res: requests.Response = requests.get(url=f"http://ideacentre.local:8000/api/v1/clients/{client_id}/contracts/{contract_id}", headers=headers)
    if res.status_code == 200:
        client_details: dict = res.json()
        return render_template(template_name_or_list='contracts/details.html', error=error, contract=client_details, client_id=client_id)
    elif res.status_code == 401:
        session.clear()
        return redirect(location=url_for(endpoint='auth.login'))
    else:
        error: str = "Cannot display client."
    return render_template(template_name_or_list='contracts/details.html', error=error, client_id=client_id, contract_id=contract_id)

@bp.route(rule='/clients/<int:client_id>/contracts/<int:contract_id>/edit', methods=('GET','POST'))
def edit(client_id: int, contract_id: int):
    error = ""
    if "auth_token" not in session.keys():
        return redirect(location=url_for(endpoint='auth.login'))

    headers = {
        "Authorization": f"Bearer {session.get("auth_token")}"
    }
    if request.method == 'POST':
        data = request.form.to_dict()
        res: requests.Response = requests.put(url=f"http://ideacentre.local:8000/api/v1/clients/{client_id}/contracts/{contract_id}", data=json.dumps(obj=data), headers=headers)
        # TODO: Change this once the bug on the API is fixed. It returns 200 instead of 201
        if res.status_code == 200:
            flash(message="Contract updated")
            return render_template(template_name_or_list='contracts/edit.html', error=error, client_id=client_id)
        elif res.status_code == 401:
            session.clear()
            return redirect(location=url_for(endpoint='auth.login'))
        else:
            error: str = res.text
            return render_template(template_name_or_list='contractd/edit.html', error=error, client_id=client_id)
        
    res: requests.Response = requests.get(url=f"http://ideacentre.local:8000/api/v1/clients/{client_id}/contracts/{contract_id}", headers=headers)
    if res.status_code == 200:
        contract_details: dict = res.json()
        return render_template(template_name_or_list='contracts/edit.html', error=error, contract=contract_details, client_id=client_id)
    elif res.status_code == 401:
        session.clear()
        return redirect(location=url_for(endpoint='auth.login'))
    else:
        error: str = "Cannot display contract."
    return render_template(template_name_or_list='contracts/edit.html', error=error, client_id=client_id)

