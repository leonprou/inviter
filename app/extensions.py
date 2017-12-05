from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_principal import Principal

db = SQLAlchemy()
migrate = Migrate()
principal = Principal()
