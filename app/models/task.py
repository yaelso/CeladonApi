from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    checklist_id = db.Column(db.Integer, db.ForeignKey("checklist.id"))
    checklist = db.relationship("Checklist", back_populates="tasks")
    # completion
    # due date

    def to_dict(self):
        task = {
            "id": self.id,
            "title": self.title,
            "checklist_id": self.checklist_id
        }

        return task

    @classmethod
    def from_dict(cls, data):
        return cls(title=data["title"], checklist_id=["checklist_id"])
