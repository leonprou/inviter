from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound
from app.database import Invitation, db
from app.permissions import admin_permission
from flask import current_app
from flask_login import current_user
from flask_principal import  Permission, RoleNeed
from flask_security.passwordless import send_login_instructions

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
    if invitation.status == 'accepted':
        return render_template('going.html')
    else:
        return render_template('not_going.html')


@blueprint.route('/')
@admin_permission.require()
def show_all():
    invitations = Invitation.query.all()
    replied_invitations = [invitation for invitation in invitations if invitation.status is not None]
    total_guests = sum([invitation.number_of_guests for invitation in invitations if invitation.status == 'accepted'])
    return render_template('show_all.html', invitations=invitations, total_replied_invitations=len(replied_invitations), total_guests=total_guests)



@blueprint.route('/invite')
@admin_permission.require()
def invite():
    invitations = Invitation.query.filter_by(status=None).all()
    for invitation in invitations:
        print('send email to {}'.format(invitation.name))
        send_login_instructions(invitation.user)
    return render_template('success.html')
