# import functools
import requests
import json
from datetime import datetime

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)

bp = Blueprint(name='activity_reports', import_name=__name__)

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

@bp.route(rule='/clients/<int:client_id>/contracts/<int:contract_id>/wo/<int:wo_id>/ar', methods=['GET'])
def activity_reports(client_id: int, contract_id: int, wo_id: int):
    error = ""
    if "auth_token" not in session.keys():
        return redirect(location=url_for(endpoint='auth.login'))
    
    ar_list: list[dict] = []
    headers = {
        "Authorization": f"Bearer {session.get("auth_token")}"
    }
    res: requests.Response = requests.get(url=f"http://ideacentre.local:8000/api/v1/clients/{client_id}/contracts/{contract_id}/wo/{wo_id}/ar", headers=headers)
    if res.status_code == 200:
        ar_list = res.json()
        return render_template(template_name_or_list='activity_reports/list.html', error=error, ar_list=ar_list, client_id=client_id, contract_id=contract_id, wo_id=wo_id)
    elif res.status_code == 401:
        session.clear()
        return redirect(location=url_for(endpoint='auth.login'))
    else:
        error: str = "Cannot display activity reports"
        return render_template(template_name_or_list='activity_reports/list.html', error=error, client_id=client_id, contract_id=contract_id, wo_id=wo_id)

@bp.route(rule='/clients/<int:client_id>/contracts/<int:contract_id>/wo/<int:wo_id>/ar/add', methods=('GET','POST'))
def add(client_id: int, contract_id: int, wo_id: int):
    error = ""
    if "auth_token" not in session.keys():
        return redirect(location=url_for(endpoint='auth.login'))
    if request.method == 'POST':
        data: dict = request.form.to_dict()

        headers = {
            "Authorization": f"Bearer {session.get("auth_token")}"
        }
        res: requests.Response = requests.post(url=f"http://ideacentre.local:8000/api/v1/clients/{client_id}/contracts/{contract_id}/wo/{wo_id}/ar", data=json.dumps(obj=data), headers=headers)
        # TODO: Change this once the bug on the API is fixed. It returns 200 instead of 201
        if res.status_code == 200:
            flash(message='Activity Report Added')
            return redirect(location=url_for(endpoint='activity_reports.activity_reports', client_id=client_id, contract_id=contract_id, wo_id=wo_id))
        elif res.status_code == 401:
            session.clear()
            return redirect(location=url_for(endpoint='auth.login'))
        else:
            error: str = "Cannot register activity report."
    return render_template(template_name_or_list='activity_reports/new.html', error=error, client_id=client_id, contract_id=contract_id, wo_id=wo_id)

# @bp.route(rule='/clients/<int:client_id>/contracts/<int:contract_id>/wo/<int:wo_id>/view', methods=['GET'])
# def view(client_id: int, contract_id: int, wo_id: int):
#     error = ""
#     if "auth_token" not in session.keys():
#         return redirect(location=url_for(endpoint='auth.login'))

#     headers = {
#         "Authorization": f"Bearer {session.get("auth_token")}"
#     }
#     res: requests.Response = requests.get(url=f"http://ideacentre.local:8000/api/v1/clients/{client_id}/contracts/{contract_id}/wo/{wo_id}", headers=headers)
#     if res.status_code == 200:
#         wo_details: dict = res.json()
#         return render_template(template_name_or_list='work_orders/details.html', error=error, wo=wo_details, client_id=client_id,contract_id=contract_id, wo_id=wo_id)
#     elif res.status_code == 401:
#         session.clear()
#         return redirect(location=url_for(endpoint='auth.login'))
#     else:
#         error: str = "Cannot display work order."
#     return render_template(template_name_or_list='work_orders/details.html', error=error, client_id=client_id, contract_id=contract_id, wo_id=wo_id)

@bp.route(rule='/clients/<int:client_id>/contracts/<int:contract_id>/wo/<int:wo_id>/ar/<int:ar_id>/edit', methods=('GET','POST'))
def edit(client_id: int, contract_id: int, wo_id: int, ar_id: int):
    error = ""
    if "auth_token" not in session.keys():
        return redirect(location=url_for(endpoint='auth.login'))

    headers = {
        "Authorization": f"Bearer {session.get("auth_token")}"
    }
    if request.method == 'POST':
        data = request.form.to_dict()
        res: requests.Response = requests.put(url=f"http://ideacentre.local:8000/api/v1/clients/{client_id}/contracts/{contract_id}/wo/{wo_id}/ar/{ar_id}", data=json.dumps(obj=data), headers=headers)
        # TODO: Change this once the bug on the API is fixed. It returns 200 instead of 201
        if res.status_code == 200:
            flash(message="Activity Report updated")
            return render_template(template_name_or_list='activity_reports/edit.html', error=error, client_id=client_id, contract_id=contract_id, ar_id=ar_id)
        elif res.status_code == 401:
            session.clear()
            return redirect(location=url_for(endpoint='auth.login'))
        else:
            error: str = res.text
            return render_template(template_name_or_list='activity_reports/edit.html', error=error, client_id=client_id, contract_id=contract_id, ar_id=ar_id)
        
    res: requests.Response = requests.get(url=f"http://ideacentre.local:8000/api/v1/clients/{client_id}/contracts/{contract_id}/wo/{wo_id}/ar/{ar_id}", headers=headers)
    if res.status_code == 200:
        ar_details: dict = res.json()
        return render_template(template_name_or_list='activity_reports/edit.html', error=error, ar=ar_details, client_id=client_id, contract_id=contract_id, wo_id=wo_id)
    elif res.status_code == 401:
        session.clear()
        return redirect(location=url_for(endpoint='auth.login'))
    else:
        error: str = "Cannot display work order."
    return render_template(template_name_or_list='activity_reports/edit.html', error=error, client_id=client_id, contract_id=contract_id, wo_id=wo_id)

