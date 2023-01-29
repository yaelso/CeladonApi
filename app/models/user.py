from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # firebase_id = db.Column(db.String)
