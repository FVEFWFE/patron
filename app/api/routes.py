from app import db
from app.api import bp
from app.models import BTCPayClientStore, User
from datetime import datetime, timedelta
from flask import request, abort
import requests
from urllib.parse import parse_qsl


@bp.route('/v1/updatesub', methods=['GET', 'POST'])
def update_sub():
    # receives and processes pmt notifications from BTCPay
    if not request.json or 'id' not in request.json:
        return "Not a valid IPN.", 200
    btc_client_store = BTCPayClientStore.query.all()[0]
    btc_client = btc_client_store.client
    invoice = btc_client.get_invoice(request.json['id'])
    if isinstance(invoice, dict):
        if 'status' in invoice:
            if invoice['status'] == "paid" or \
               invoice['status'] == "confirmed":
                user = User.query.filter_by(
                    username=invoice['buyer']['name']).first()
                if user is None:
                    return "Payment made for unregistered user.", 200
                if user.role == 'admin':
                    return "Administrator should not make payments.", 200
                elif invoice['status'] == "confirmed":
                    if user.expiration <= datetime.today():
                        base = datetime.today()
                    else:
                        base = user.expiration
                    user.expiration = base + timedelta(days=30)
                    user.role = invoice['orderId']
                    db.session.commit()
                    return "Payment Accepted", 201
                elif invoice['status'] == "paid":
                    if user.expiration <= datetime.today():
                        base = datetime.today()
                    else:
                        base = user.expiration
                    user.expiration = base + timedelta(hours=6)
                    user.role = invoice['orderId']
                    db.session.commit()
                    return "Payment Accepted", 201
                else:
                    return "IPN Received", 200
            else:
                return "Status not paid or confirmed.", 200
        else:
            return "No payment status received.", 200
    else:
        return "Invalid transaction ID.", 400


@bp.route('/v1/updatesubpaypal', methods=['GET', 'POST'])
def update_sub_paypal():
    # TODO this was probably mooted by Square integration
    params = parse_qsl(request.form)
    params.append(('cmd', '_notify-validate'))
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Python-IPN-Verification-Script'
    }
    r = requests.post(
        VERIFY_URL,
        params=params,
        headers=headers,
        verify=True
    )
    r.raise_for_status()
    if r.text == 'VERIFIED':
        user.expiration = datetime.today() + timedelta(days=30)
        db.session.commit()
    elif r.text == 'INVALID':
        return None
