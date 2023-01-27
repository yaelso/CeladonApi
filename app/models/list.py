from app import db

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    category = db.relationship("Category", back_populates="lists")
    tasks = db.relationship("Task", back_populates="list", lazy=True)
    status_id = db.Column(db.Integer, db.ForeignKey("list_status.id"))
