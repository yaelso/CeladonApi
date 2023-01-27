from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey("list.id"))
    list = db.relationship("List", back_populates="tasks")
    # completion
    # due date
