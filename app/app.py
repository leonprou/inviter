from flask import Flask
from app.settings import ProdConfig, LOGGING
from app.extensions import migrate, principal, security, mail
from app.database import db, user_datastore
from .exceptions import register_errorhandlers
from .permissions import setup_permissions
from app import invitation, user
import logging.config

def create_app(config_object=ProdConfig):
    app = Flask(__name__.split('.')[0])
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    setup_permissions(app)
    logging.config.dictConfig(LOGGING)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    principal.init_app(app)
    security.init_app(app, datastore=user_datastore)
    mail.init_app(app)

def register_blueprints(app):
    app.register_blueprint(invitation.views.blueprint, url_prefix='/invitations')
    app.register_blueprint(user.views.blueprint)
