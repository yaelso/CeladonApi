from app import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    checklists = db.relationship("Checklist", back_populates="category", lazy=True, cascade="delete, delete-orphan")

    def to_dict(self, checklists=False):
        category = {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
        }

        if checklists:
            category["checklists"] = [checklist.to_dict(checklist.tasks) for checklist in self.checklists]

        return category

    @classmethod
    def from_dict(cls, data):
        return cls(user_id=data["user_id"], title=data["title"], description=data["description"])
