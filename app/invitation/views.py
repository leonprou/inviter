from flask import Blueprint, render_template, abort, request, current_app, redirect, url_for
from jinja2 import TemplateNotFound
from flask_login import current_user
from flask_principal import  Permission, RoleNeed
from flask_security.passwordless import send_login_instructions
from werkzeug.utils import secure_filename
from app.database import Invitation, User, db
from app.permissions import admin_permission
from csv import DictReader
from werkzeug.wsgi import make_line_iter
import io
import codecs

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
    if int(request.form['number_of_guests']) > invitation.max_number_of_guests:
        return render_template('failed.html')
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
    total_invitations= len([invitation for invitation in invitations])
    total_invitations_accepted = len([invitation for invitation in invitations if invitation.status == 'accepted'])
    total_guests = sum([invitation.number_of_guests for invitation in invitations])
    total_guests_accepted = sum([invitation.number_of_guests for invitation in invitations if invitation.status == 'accepted'])
    return render_template('show_all.html', invitations=invitations, total_invitations=total_invitations, total_invitations_accepted=total_invitations_accepted, total_guests=total_guests, total_guests_accepted=total_guests_accepted)



@blueprint.route('/invite', methods=['GET', 'POST'])
@admin_permission.require()
def invite():
    if request.method == 'GET':
        invitations = Invitation.query.filter_by(status=None).all()
    else:
        emails = list(request.form.keys())
        users = User.query.filter(User.email.in_(emails)).all()
        invitations = [u.invitation for u in users]
    for invitation in invitations:
        send_login_instructions(invitation.user)
    return render_template('success.html')


@blueprint.route('/upload', methods=['GET', 'POST'])
@admin_permission.require()
def upload():
    if request.method == 'POST':
        file = request.files['file']
        upload_csv(codecs.getreader("utf-8")(file.stream))
        return redirect(url_for('invitation.show_all'))
    else:
        return render_template('upload.html')


def upload_csv(stream):
    fieldnames = ('name', 'number_of_guests', 'related_to', 'group', 'phone_number', None, 'email')
    reader = DictReader(stream, fieldnames=fieldnames)
    next(reader)
    next(reader)
    try:
        for row in reader:
            if not row.get('email'):
                continue
            del row[None]
            user = User(email=row['email'])
            del row['email']
            invitation = Invitation(**row, user=user)
            db.session.add(user)
            db.session.add(invitation)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

