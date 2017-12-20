from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound
from app.database import Invitation, db
from app.permissions import admin_permission
from flask import current_app, render_template, url_for, redirect
from flask_login import current_user
from flask_security import login_required

blueprint = Blueprint('user', __name__,
                        template_folder='templates')

@blueprint.route('/')
@login_required
def index():
    if current_user.has_role('admin'):
        return redirect(url_for('invitation.show_all'))
    else:
        return redirect(url_for('invitation.show', invitation_id=current_user.invitation.id))
