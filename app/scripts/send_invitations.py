from app.database import Invitation
from app.email import send_email, connect


subject = 'wedding invite!'
text = 'hello {name}'

def send_invitations():
    invitations = Invitation.query.filter_by(status=None).all()
    server = connect()
    for invitation in invitations:
        print('send email to {}'.format(invitation.name))
        send_email(subject, text.format(name=invitation.name), invitation.email, server)

def main():
    send_invitations()

if __name__ == '__main__':
    main()
