from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound
from app.database import Invitation, db
from app.permissions import admin_permission

blueprint = Blueprint('user', __name__,
                        template_folder='templates')

@blueprint.route('/login')
def login():
    return render_template('login.html')

