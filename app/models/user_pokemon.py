from app import db

class UserPokemon(db.Model):
    __tablename__ = "user_pokemon"
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True, nullabe=False)
    pokemon_id = db.Column(db.Integer, db.ForeignKey("pokemon.id"), primary_key=True, nullable=False)
    exp = db.Column(db.Integer, default=0)

    def to_dict(self):
        user = {
            "user_id": self.user_id,
            "pokemon_id": self.pokemon_id,
            "exp": self.exp
        }

        return user

    @classmethod
    def from_dict(cls, data):
        return cls(user_id=data["user_id"], pokemon_id=data["pokemon_id"])

    def update_exp(self, request_exp):
        self.exp += request_exp

    def reset_exp(self):
        self.exp = 0
