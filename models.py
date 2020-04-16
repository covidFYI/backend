from extensions import db

class Entries(db.Document):
    id = db.StringField(required=True, primary_key=True)
    state = db.StringField(required=True)
    area = db.StringField()
    category = db.StringField(required=True)
    subCategory = db.StringField()
    name = db.StringField()
    pointOfContact = db.StringField()
    address = db.StringField()
    email_1 = db.StringField()
    email_2 = db.StringField()
    phone_1 = db.StringField()
    phone_2 = db.StringField()
    sourceURL = db.StringField()
    source = db.StringField()
    description = db.StringField()


