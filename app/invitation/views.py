from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound
from flask.ext.principal import Permission, RoleNeed
from app.database import Invitation, db
from app.permissions import admin_permission

blueprint = Blueprint('invitation', __name__,
                        template_folder='templates')

@blueprint.route('/<uuid>')
def show(uuid):
    try:
        invitation = Invitation.query.get(uuid)
        return render_template('invitation.html', **vars(invitation))
    except TemplateNotFound:
        abort(404)

@blueprint.route('/<uuid>', methods=['POST'])
def update(uuid):
    invitation = Invitation.query.get(uuid)
    invitation.status = request.form['status']
    invitation.number_of_guests = request.form['number_of_guests']
    db.session.add(invitation)
    db.session.commit()
    return render_template('success.html')


@blueprint.route('/')
@admin_permission.require()
def show_all():
    return render_template('success.html')
