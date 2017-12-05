import smtplib
from email.mime.text import MIMEText
import logging
from flask.helpers import get_debug_flag
import secret

logger = logging.getLogger(__name__)

class config:
    EMAIL_SERVER = 'smtp.gmail.com:587'
    EMAIL_PASSWORD = secret.EMAIL_PASSWORD
    EMAIL_SENDER = 'deeptrade1@gmail.com'
    EMAIL_RECEPIENT = 'deeptrade1@gmail.com'

def connect():
    server = smtplib.SMTP(config.EMAIL_SERVER)
    server.ehlo()
    server.starttls()
    server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
    return server


def send_email(subject, text, recepient, debug_mode=False, server=None):
    logger.info('Sending email in {mode} mode. {subject}. body: {text}'.format(
        mode='DEV' if debug_mode else 'PROD', subject=subject, text=text))
    if not debug_mode:
        if not server:
            server = connect()
        msg = MIMEText(text)
        msg['Subject'] = subject
        msg['From'] = config.EMAIL_SENDER
        msg['To'] = recepient
        server.send_message(msg)
