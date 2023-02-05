from app import db

class Checklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    category = db.relationship("Category", back_populates="checklists")
    tasks = db.relationship("Task", back_populates="checklist", lazy=True)
    is_archived = db.Column(db.Boolean, default=False)
    is_favorited = db.Column(db.Boolean, default=False)

    def to_dict(self, tasks=False):
        checklist = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category_id": self.category_id,
            "is_archived": self.is_archived,
            "is_favorited": self.is_favorited,
        }

        if tasks:
            checklist["tasks"] = [task.to_dict() for task in self.tasks]

        return checklist

    @classmethod
    def from_dict(cls, data):
        return cls(title=data["title"], description=data["description"], category_id=data["category_id"])

    def update_is_archived(self, archival_status=True):
        if not archival_status == False:
            self.is_archived = True
        else:
            self.is_archived = False

    def update_is_favorited(self, favorite_status=True):
        if not favorite_status == False:
            self.is_favorited = True
        else:
            self.is_favorited = False
