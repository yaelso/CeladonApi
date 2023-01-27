from app import db

class Checklist_Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
