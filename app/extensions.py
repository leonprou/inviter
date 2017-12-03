from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask.ext.principal import Principal

db = SQLAlchemy()
migrate = Migrate()
principal = Principal()
