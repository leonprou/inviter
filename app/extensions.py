from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_principal import Principal
from flask_jwt import JWT
from flask_security import Security, SQLAlchemyUserDatastore
from flask_mail import Mail, Connection
from .database import db
import smtplib

def configure_host(self):
    if self.mail.use_ssl:
        host = smtplib.SMTP_SSL(self.mail.server, self.mail.port)
    else:
        host = smtplib.SMTP(self.mail.server, self.mail.port)
    
    host.ehlo()
    host.starttls()
    host.set_debuglevel(int(self.mail.debug))

    if self.mail.use_tls:
        host.starttls()
    if self.mail.username and self.mail.password:
        host.login(self.mail.username, self.mail.password)

    return host
    
migrate = Migrate()
principal = Principal()
jwt = JWT()
security = Security()
mail = Mail()

Connection.configure_host = configure_host
