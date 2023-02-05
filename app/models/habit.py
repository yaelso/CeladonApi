from app import db

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String, nullable=False)
    reps = db.Column(db.Integer, default=0)

    def to_dict(self):
        habit = {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "reps": self.reps,
        }

        return habit

    @classmethod
    def from_dict(cls, data):
        return cls(user_id=data["user_id"], title=data["title"])

    def update_reps(self, request_reps):
        self.reps += request_reps

    def reset_reps(self):
        self.reps = 0
