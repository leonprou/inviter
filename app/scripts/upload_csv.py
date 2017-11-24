from app.database import db, Invitation
from csv import DictReader

def upload_csv(filename):
    fieldnames = ('name', 'number_of_guests', 'related_to', 'group', 'phone_number', None, 'email')
    f = open(filename)
    reader = DictReader(f, fieldnames=fieldnames)
    next(reader)
    next(reader)
    for row in reader:                          
        del row[None]
        invitation = Invitation(**row)
        db.session.add(invitation)
    db.session.commit()

def main():
    filename = '/Users/leonprouger/data/wedding/invitations.csv'
    upload_csv(filename)


if __name__ == '__main__':
    main()
