from app.database import Invitation
from app.email import send_email, connect
from flask import url_for, current_app
from flask_security.passwordless import send_login_instructions
import jwt
import secret

subject = 'wedding invite!'
text = 'hello {name}, follow the url: {url}'

def send_invitations():
    with current_app.app_context():
        invitations = Invitation.query.filter_by(status=None).all()
        server = connect()
        for invitation in invitations:
            print('send email to {}'.format(invitation.name))
            send_login_instructions(invitation.user)

def main():
    send_invitations()

if __name__ == '__main__':
    main()
