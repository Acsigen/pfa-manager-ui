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
    headers: dict = {
        "Authorization": f"Bearer {session.get("auth_token")}"
    }
    res: requests.Response = requests.get(url="http://ideacentre.local:8000/api/v1/invoices", headers=headers)
    if res.status_code == 200:
        invoice_list = res.json()
        res: requests.Response = requests.get(url="http://ideacentre.local:8000/api/v1/clients", headers=headers)
        if res.status_code == 200:
            client_list: list[dict] = res.json()
            client_lookup: dict = {client['id']: client['name'] for client in client_list}
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

# TODO: Implement the post method
@bp.route(rule='/<int:invoice_id>/items', methods=('GET','POST'))
def add_invoice_items(invoice_id: int):
    error = ""
    if "auth_token" not in session.keys():
        return redirect(location=url_for(endpoint='auth.login'))
    headers: dict = {
        "Authorization": f"Bearer {session.get("auth_token")}"
    }
    if request.method == 'POST':
        data: dict = request.form.to_dict()
        for ar in data.values():
            req_data: dict = {
                "invoice_id": invoice_id,
                "ar_id": ar
            }
            res: requests.Response = requests.post(url=f"http://ideacentre.local:8000/api/v1/invoices/{invoice_id}/items", json=req_data, headers=headers)
            # TODO: Change this once the bug on the API is fixed. It returns 200 instead of 201
            if res.status_code == 200:
                flash(message='Item Added')
                return redirect(location=url_for(endpoint='invoices.add_invoice_items'))
            elif res.status_code == 401:
                session.clear()
                return redirect(location=url_for(endpoint='auth.login'))
            else:
                error: str = "Cannot register items."
    res: requests.Response = requests.get(url=f"http://ideacentre.local:8000/api/v1/invoices/{invoice_id}", headers=headers)
    if res.status_code == 200:
        invoice: dict = res.json()
        invoice.pop("user_id")
        res: requests.Response = requests.post(url=f"http://ideacentre.local:8000/api/v1/invoices/{invoice_id}/available_items", headers=headers, data=json.dumps(obj=invoice))
        if res.status_code == 200:
            available_items: list = res.json()
        elif res.status_code == 401:
            session.clear()
            return redirect(location=url_for(endpoint='auth.login'))
        else:
            error: str = "Cannot display available items"
            return render_template(template_name_or_list='invoices/add_items.html', error=error)
    elif res.status_code == 401:
        session.clear()
        return redirect(location=url_for(endpoint='auth.login'))
    else:
        error: str = "Cannot display invoices"
        return render_template(template_name_or_list='invoices/add_items.html', error=error, invoice_id=invoice_id)
    return render_template(template_name_or_list='invoices/add_items.html', error=error, available_items=available_items, invoice_id=invoice_id)

@bp.route(rule='/invoices/<int:invoice_id>/view', methods=['GET'])
def view(invoice_id: int):
    error = ""
    if "auth_token" not in session.keys():
        return redirect(location=url_for(endpoint='auth.login'))

    headers: dict = {
        "Authorization": f"Bearer {session.get("auth_token")}"
    }
    res: requests.Response = requests.get(url=f"http://ideacentre.local:8000/api/v1/invoices/{invoice_id}", headers=headers)
    if res.status_code == 200:
        invoice_details: dict = res.json()
        res: requests.Response = requests.get(url=f"http://ideacentre.local:8000/api/v1/clients/{invoice_details.get("client_id")}", headers=headers)
        if res.status_code == 200:
            invoice_details["client_data"] = res.json()
            return render_template(template_name_or_list='invoices/details.html', error=error, invoice_details=invoice_details)
            # TODO: also grab invoice items
        elif res.status_code == 401:
            session.clear()
            return redirect(location=url_for(endpoint='auth.login'))
        else:
            error: str = "Cannot display invoice client."
        return render_template(template_name_or_list='invoices/details.html', error=error)
    elif res.status_code == 401:
        session.clear()
        return redirect(location=url_for(endpoint='auth.login'))
    else:
        error: str = "Cannot display invoice."
    return render_template(template_name_or_list='invoices/details.html', error=error)

@bp.route(rule='/<int:invoice_id>/edit', methods=('GET','POST'))
def edit(invoice_id: int):
    error = ""
    if "auth_token" not in session.keys():
        return redirect(location=url_for(endpoint='auth.login'))

    headers: dict = {
        "Authorization": f"Bearer {session.get("auth_token")}"
    }
    if request.method == 'POST':
        data: dict = request.form.to_dict()
        res: requests.Response = requests.put(url=f"http://ideacentre.local:8000/api/v1/invoices/{invoice_id}", data=json.dumps(obj=data), headers=headers)
        # TODO: Change this once the bug on the API is fixed. It returns 200 instead of 201
        if res.status_code == 200 or res.status_code == 201:
            flash(message="Invoice updated")
            return render_template(template_name_or_list='invoices/edit.html', error=error)
        elif res.status_code == 401:
            session.clear()
            return redirect(location=url_for(endpoint='auth.login'))
        else:
            error: str = res.text
            return render_template(template_name_or_list='invoices/edit.html', error=error)
    res: requests.Response = requests.get(url=f"http://ideacentre.local:8000/api/v1/invoices/{invoice_id}", headers=headers)
    if res.status_code == 200:
        invoice_details: dict = res.json()
        res: requests.Response = requests.get(url="http://ideacentre.local:8000/api/v1/clients", headers=headers)
        if res.status_code == 200:
            client_list: list[dict] = res.json()
        elif res.status_code == 401:
            session.clear()
            return redirect(location=url_for(endpoint='auth.login'))
        else:
            error: str = "Cannot display clients"
            return render_template(template_name_or_list='invoices/edit.html', error=error)
        return render_template(template_name_or_list='invoices/edit.html', error=error, invoice_id=invoice_id, invoice=invoice_details, client_list=client_list)
    elif res.status_code == 401:
        session.clear()
        return redirect(location=url_for(endpoint='auth.login'))
    else:
        error: str = "Cannot display invoice."
    return render_template(template_name_or_list='invoices/edit.html', error=error)

