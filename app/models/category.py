from app import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    lists = db.relationship("List", back_populates="category", lazy=True)
