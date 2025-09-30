# import functools
import requests
import json
from datetime import datetime

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)

bp = Blueprint(name='work_orders', import_name=__name__)

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

@bp.route(rule='/clients/<int:client_id>/contracts/<int:contract_id>/wo', methods=['GET'])
def work_orders(client_id: int, contract_id: int):
    error = ""
    if "auth_token" not in session.keys():
        return redirect(location=url_for(endpoint='auth.login'))
    
    wo_list: list[dict] = []
    headers = {
        "Authorization": f"Bearer {session.get("auth_token")}"
    }
    res: requests.Response = requests.get(url=f"http://ideacentre.local:8000/api/v1/clients/{client_id}/contracts/{contract_id}/wo", headers=headers)
    if res.status_code == 200:
        wo_list = res.json()
    elif res.status_code == 401:
        session.clear()
        return redirect(location=url_for(endpoint='auth.login'))
    else:
        error: str = "Cannot display work orders"
        return render_template(template_name_or_list='work_orders/list.html', error=error, client_id=client_id, contract_id=contract_id)
    
    return render_template(template_name_or_list='work_orders/list.html', error=error, wo_list=wo_list, client_id=client_id, contract_id=contract_id)

@bp.route(rule='/clients/<int:client_id>/contracts/<int:contract_id>/wo/add', methods=('GET','POST'))
def add(client_id: int, contract_id: int):
    error = ""
    if "auth_token" not in session.keys():
        return redirect(location=url_for(endpoint='auth.login'))
    if request.method == 'POST':
        data: dict = request.form.to_dict()

        if datetime.now() > datetime.strptime(data["end_date"], "%Y-%m-%d"):
            data["status"] = "Expired"
        else:
            data["status"] = "Active"
        headers = {
            "Authorization": f"Bearer {session.get("auth_token")}"
        }
        res: requests.Response = requests.post(url=f"http://ideacentre.local:8000/api/v1/clients/{client_id}/contracts/{contract_id}/wo", data=json.dumps(obj=data), headers=headers)
        # TODO: Change this once the bug on the API is fixed. It returns 200 instead of 201
        if res.status_code == 200:
            flash(message='Work Order Added')
            return redirect(location=url_for(endpoint='work_orders.work_orders', client_id=client_id, contract_id=contract_id))
        elif res.status_code == 401:
            session.clear()
            return redirect(location=url_for(endpoint='auth.login'))
        else:
            error: str = "Cannot register work order."
    return render_template(template_name_or_list='work_orders/new.html', error=error, client_id=client_id, contract_id=contract_id)

@bp.route(rule='/clients/<int:client_id>/contracts/<int:contract_id>/wo/<int:wo_id>/view', methods=['GET'])
def view(client_id: int, contract_id: int, wo_id: int):
    error = ""
    if "auth_token" not in session.keys():
        return redirect(location=url_for(endpoint='auth.login'))

    headers = {
        "Authorization": f"Bearer {session.get("auth_token")}"
    }
    res: requests.Response = requests.get(url=f"http://ideacentre.local:8000/api/v1/clients/{client_id}/contracts/{contract_id}/wo/{wo_id}", headers=headers)
    if res.status_code == 200:
        wo_details: dict = res.json()
        return render_template(template_name_or_list='work_orders/details.html', error=error, wo=wo_details, client_id=client_id,contract_id=contract_id, wo_id=wo_id)
    elif res.status_code == 401:
        session.clear()
        return redirect(location=url_for(endpoint='auth.login'))
    else:
        error: str = "Cannot display work order."
    return render_template(template_name_or_list='work_orders/details.html', error=error, client_id=client_id, contract_id=contract_id, wo_id=wo_id)

@bp.route(rule='/clients/<int:client_id>/contracts/<int:contract_id>/wo/<int:wo_id>/edit', methods=('GET','POST'))
def edit(client_id: int, contract_id: int, wo_id: int):
    error = ""
    if "auth_token" not in session.keys():
        return redirect(location=url_for(endpoint='auth.login'))

    headers = {
        "Authorization": f"Bearer {session.get("auth_token")}"
    }
    if request.method == 'POST':
        data = request.form.to_dict()
        if datetime.now() > datetime.strptime(data["end_date"], "%Y-%m-%d"):
            data["status"] = "Expired"
        else:
            data["status"] = "Active"
        res: requests.Response = requests.put(url=f"http://ideacentre.local:8000/api/v1/clients/{client_id}/contracts/{contract_id}/wo/{wo_id}", data=json.dumps(obj=data), headers=headers)
        # TODO: Change this once the bug on the API is fixed. It returns 200 instead of 201
        if res.status_code == 200:
            flash(message="Work Order updated")
            return render_template(template_name_or_list='work_orders/edit.html', error=error, client_id=client_id, contract_id=contract_id)
        elif res.status_code == 401:
            session.clear()
            return redirect(location=url_for(endpoint='auth.login'))
        else:
            error: str = res.text
            return render_template(template_name_or_list='contractd/edit.html', error=error, client_id=client_id, contract_id=contract_id)
        
    res: requests.Response = requests.get(url=f"http://ideacentre.local:8000/api/v1/clients/{client_id}/contracts/{contract_id}/wo/{wo_id}", headers=headers)
    if res.status_code == 200:
        wo_details: dict = res.json()
        return render_template(template_name_or_list='work_orders/edit.html', error=error, wo=wo_details, client_id=client_id, contract_id=contract_id)
    elif res.status_code == 401:
        session.clear()
        return redirect(location=url_for(endpoint='auth.login'))
    else:
        error: str = "Cannot display work order."
    return render_template(template_name_or_list='work_orders/edit.html', error=error, client_id=client_id, contract_id=contract_id)

