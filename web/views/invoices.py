# import functools
import requests
import json

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)

bp = Blueprint(name='invoices', import_name=__name__, url_prefix='/invoices')

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

@bp.route(rule='/', methods=['GET'])
def invoices():
    error = ""
    if "auth_token" not in session.keys():
        return redirect(location=url_for(endpoint='auth.login'))
    
    invoice_list: list[dict] = []
    headers = {
        "Authorization": f"Bearer {session.get("auth_token")}"
    }
    res: requests.Response = requests.get(url="http://ideacentre.local:8000/api/v1/invoices", headers=headers)
    if res.status_code == 200:
        invoice_list = res.json()
        res: requests.Response = requests.get(url="http://ideacentre.local:8000/api/v1/clients", headers=headers)
        if res.status_code == 200:
            client_list: list[dict] = res.json()
            client_lookup = {client['id']: client['name'] for client in client_list}
            for invoice in invoice_list:
                invoice["client_name"] = client_lookup.get(invoice['client_id'], 'Unknown')
        elif res.status_code == 401:
            session.clear()
            return redirect(location=url_for(endpoint='auth.login'))
        else:
            error: str = "Cannot display invoices"
            return render_template(template_name_or_list='invoices/list.html', error=error)
    else:
        error: str = "Cannot display invoices"
        return render_template(template_name_or_list='invoices/list.html', error=error)
    
    return render_template(template_name_or_list='invoices/list.html', error=error, invoice_list=invoice_list)

@bp.route(rule='/add', methods=('GET','POST'))
def add():
    error = ""
    if "auth_token" not in session.keys():
        return redirect(location=url_for(endpoint='auth.login'))
    headers: dict = {
        "Authorization": f"Bearer {session.get("auth_token")}"
    }
    if request.method == 'POST':
        data: dict = request.form.to_dict()
        res: requests.Response = requests.post(url="http://ideacentre.local:8000/api/v1/invoices", data=json.dumps(obj=data), headers=headers)
        # TODO: Change this once the bug on the API is fixed. It returns 200 instead of 201
        if res.status_code == 200:
            flash(message='Invoice Added')
            return redirect(location=url_for(endpoint='invoices.invoices'))
        elif res.status_code == 401:
            session.clear()
            return redirect(location=url_for(endpoint='auth.login'))
        else:
            error: str = "Cannot register invoice."
    res: requests.Response = requests.get(url="http://ideacentre.local:8000/api/v1/clients", headers=headers)
    if res.status_code == 200:
        client_list: list[dict] = res.json()
    elif res.status_code == 401:
        session.clear()
        return redirect(location=url_for(endpoint='auth.login'))
    else:
        error: str = "Cannot display clients"
        return render_template(template_name_or_list='invoices/new.html', error=error)
    return render_template(template_name_or_list='invoices/new.html', error=error, client_list=client_list)

# @bp.route(rule='/<int:client_id>/view', methods=['GET'])
# def view(client_id: int):
#     client_id = client_id
#     error = ""
#     if "auth_token" not in session.keys():
#         return redirect(location=url_for(endpoint='auth.login'))

#     headers = {
#         "Authorization": f"Bearer {session.get("auth_token")}"
#     }
#     res: requests.Response = requests.get(url=f"http://ideacentre.local:8000/api/v1/clients/{client_id}", headers=headers)
#     if res.status_code == 200:
#         client_details: dict = res.json()
#         return render_template(template_name_or_list='clients/client_details.html', error=error, client_details=client_details)
#     elif res.status_code == 401:
#         session.clear()
#         return redirect(location=url_for(endpoint='auth.login'))
#     else:
#         error: str = "Cannot display client."
#     return render_template(template_name_or_list='clients/client_details.html', error=error)

# @bp.route(rule='/<int:client_id>/edit', methods=('GET','POST'))
# def edit(client_id: int):
#     client_id = client_id
#     error = ""
#     if "auth_token" not in session.keys():
#         return redirect(location=url_for(endpoint='auth.login'))

#     headers = {
#         "Authorization": f"Bearer {session.get("auth_token")}"
#     }
#     if request.method == 'POST':
#         data = request.form.to_dict()
#         res: requests.Response = requests.put(url=f"http://ideacentre.local:8000/api/v1/clients/{client_id}", data=json.dumps(obj=data), headers=headers)
#         # TODO: Change this once the bug on the API is fixed. It returns 200 instead of 201
#         if res.status_code == 200:
#             flash(message="Client updated")
#             return render_template(template_name_or_list='clients/edit_client.html', error=error)
#         elif res.status_code == 401:
#             session.clear()
#             return redirect(location=url_for(endpoint='auth.login'))
#         else:
#             error: str = res.text
#             return render_template(template_name_or_list='clients/edit_client.html', error=error)
        
#     res: requests.Response = requests.get(url=f"http://ideacentre.local:8000/api/v1/clients/{client_id}", headers=headers)
#     if res.status_code == 200:
#         client_details: dict = res.json()
#         return render_template(template_name_or_list='clients/edit_client.html', error=error, client_details=client_details)
#     elif res.status_code == 401:
#         session.clear()
#         return redirect(location=url_for(endpoint='auth.login'))
#     else:
#         error: str = "Cannot display client."
#     return render_template(template_name_or_list='clients/edit_client.html', error=error)

