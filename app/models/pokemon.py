from app import db

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    img_href = db.Column(db.String, nullable=False)

    def to_dict(self):
        pokemon = {
            "id": self.id,
            "name": self.name,
            "img_href": self.img_href,
        }

        return pokemon

    @classmethod
    def from_dict(cls, data):
        return cls(name=data["name"], img_href=data["img_href"])
