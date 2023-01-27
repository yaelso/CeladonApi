from app import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    checklists = db.relationship("Checklist", back_populates="category", lazy=True)

    def to_dict(self, checklists=False):
        category = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
        }

        if checklists:
            category["checklists"] = [checklist.to_dict() for checklist in self.checklists]

        return category

    @classmethod
    def from_dict(cls, data):
        return cls(title=data["title"], description=data["description"])
