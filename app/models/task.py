from app import db
from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    checklist_id = db.Column(db.Integer, db.ForeignKey("checklist.id"))
    checklist = db.relationship("Checklist", back_populates="tasks")
    in_progress = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, default=None)
    due_date = db.Column(db.DateTime, default=None)

    def to_dict(self):
        task = {
            "id": self.id,
            "title": self.title,
            "checklist_id": self.checklist_id,
            "is_complete": bool(self.completed_at),
            "in_progress": self.in_progress,
            "due_date": self.due_date
        }

        return task

    @classmethod
    def from_dict(cls, data):
        return cls(title=data["title"], checklist_id=data["checklist_id"])

    def update_completed_at(self, completion_status=True):
        if not completion_status == False:
            self.completed_at = datetime.utcnow()
            if self.in_progress == True:
                self.in_progress = False
        else:
            self.completed_at = None

    def update_in_progress(self, progress_status=True):
        if not progress_status == False:
            self.in_progress = True
        else:
            self.in_progress = False

    def update_due_date(self, request_due_date):
        if request_due_date:
            self.due_date = request_due_date
        else:
            self.due_date = None
