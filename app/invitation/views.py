from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound
from app.database import Invitation, db
from app.permissions import admin_permission
from flask import current_app
import secret
import jwt

blueprint = Blueprint('invitation', __name__,
                        template_folder='templates')

@blueprint.route('/<uuid>')
def show(uuid):
    try:
        current_app.logger.info(uuid)
        payload = jwt.decode(uuid, secret.SECRET_KEY, algorithms=['HS256'])
        current_app.logger.info(payload)
        invitation = Invitation.query.get(payload['id'])
        return render_template('invitation.html', **vars(invitation))
    except TemplateNotFound:
        abort(404)

@blueprint.route('/<uuid>', methods=['POST'])
def update(uuid):
    payload = jwt.decode(uuid, secret.SECRET_KEY, algorithms=['HS256'])
    invitation = Invitation.query.get(payload['id'])
    invitation.status = request.form['status']
    invitation.number_of_guests = request.form['number_of_guests']
    db.session.add(invitation)
    db.session.commit()
    return render_template('success.html')


@blueprint.route('/')
@admin_permission.require()
def show_all():
    return render_template('success.html')
