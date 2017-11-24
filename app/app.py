from flask import Flask
from app.settings import ProdConfig
from app.extensions import db, migrate
from .exceptions import register_errorhandlers
#from app.invitation.views import blueprint
from app import invitation

def create_app(config_object=ProdConfig):
    app = Flask(__name__.split('.')[0])
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)

def register_blueprints(app):
    app.register_blueprint(invitation.views.blueprint, url_prefix='/invitations')
