from .celery import app
from .services import (
    increase_debt,
    decrease_debt,
    make_debt_zero,
    populate_db_with_data,
    send_qr_email,
    send_api_key
)


@app.task
def increase_amount():
    increase_debt()


@app.task
def decrease_amount():
    decrease_debt()


@app.task
def clear_debt_celery(entities_id):
    return make_debt_zero(entities_id)


@app.task
def populate_db_with_celery():
    return populate_db_with_data()


@app.task
def send_email_qr(email, new_data, entity_name):
    send_qr_email(email, new_data, entity_name)


@app.task
def send_mail_api_key(email, key):
    send_api_key(email, key)
