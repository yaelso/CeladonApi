from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firebase_id = db.Column(db.String, nullable=False)
    active_pokemon_id = db.Column(db.Integer, db.ForeignKey("pokemon.id"), default=None)

    def to_dict(self):
        user = {
            "id": self.id,
            "firebase_id": self.firebase_id,
            "active_pokemon_id": self.active_pokemon_id
        }

        return user

    @classmethod
    def from_dict(cls, data):
        return cls(firebase_id=data)

    def update_active_pokemon(self, request_pokemon_id):
        self.active_pokemon_id = request_pokemon_id
