from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound
from app.database import Invitation, db
from app.permissions import admin_permission
from flask import current_app
from flask_login import current_user
from flask_principal import  Permission, RoleNeed


admin_permission = Permission(RoleNeed('admin'))

blueprint = Blueprint('invitation', __name__,
                        template_folder='templates')

@blueprint.route('/<int:invitation_id>')
def show(invitation_id):
    try:
        invitation = current_user.invitation
        if current_user.has_role('admin') or invitation.id == invitation_id:
            invitation = invitation or Invitation.query.get(invitation_id)
            return render_template('show.html', **vars(invitation))
        else:
            return render_template('no_permissions.html')
    except TemplateNotFound:
        abort(404)

@blueprint.route('/<int:invitation_id>', methods=['POST'])
def update(invitation_id):
    invitation = current_user.invitation
    if current_user.has_role('admin') or invitation.id == invitation_id:
        invitation = invitation or Invitation.query.get(invitation_id)
    invitation.status = request.form['status']
    invitation.number_of_guests = request.form['number_of_guests']
    db.session.add(invitation)
    db.session.commit()
    return render_template('success.html')


@blueprint.route('/')
@admin_permission.require()
def show_all():
    print('HA')
    invitations = Invitation.query.all()
    total_guests = sum([invitation.number_of_guests if invitation.status == 'accepted' else 0 for invitation in invitations])
    return render_template('show_all.html', invitations=invitations, total_guests=total_guests)