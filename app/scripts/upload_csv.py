from app.database import db, Invitation, User
from csv import DictReader

def upload_csv(filename):
    fieldnames = ('name', 'number_of_guests', 'related_to', 'group', 'phone_number', None, 'email')
    f = open(filename)
    reader = DictReader(f, fieldnames=fieldnames)
    next(reader)
    next(reader)
    try:
        for row in reader:                          
            del row[None]
            user = User(email=row['email'])
            del row['email']
            invitation = Invitation(**row, user=user)
            db.session.add(user)
            db.session.add(invitation)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def main():
    filename = '/Users/leonprouger/data/wedding/invitations.csv'
    upload_csv(filename)


if __name__ == '__main__':
    main()
