import smtplib
from email.mime.text import MIMEText
from email.message import Message
from email.mime.multipart import MIMEMultipart
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


def send_email(subject, html, recepient, server=None):
    logger.info('Sending email {subject}. body: {text}'.format(
        subject=subject, text=text))
    if get_debug_flag():
        if not server:
            server = connect()
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = config.EMAIL_SENDER
        msg['To'] = recepient

        text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
        html = """\
		<html>
  		<head></head>
  		<body>
    		<p>Hi!<br>
 		 </body>
		</html>
	    """
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)

        server.sendmail(config.EMAIL_SENDER, recepient, msg.as_string())
