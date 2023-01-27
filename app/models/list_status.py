from app import db

class List_Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
