from app import db

class Checklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    category = db.relationship("Category", back_populates="checklists")
    tasks = db.relationship("Task", back_populates="checklist", lazy=True)
    status_id = db.Column(db.Integer, db.ForeignKey("checklist_status.id"))

    def to_dict(self, tasks=False):
        checklist = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category_id": self.category_id,
        }

        if tasks:
            checklist["tasks"] = [task.to_dict() for task in self.tasks]

        return checklist

    @classmethod
    def from_dict(cls, data):
        return cls(title=data["title"], description=data["description"], category_id=["category_id"])
