from sqlalchemy.orm import Mapped

from app.models.note import Note
from app import db

class User(db.Model):
    __tablename__: str = "users"

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(100), nullable=False)
    surname: Mapped[str] = db.Column(db.String(100), nullable=False)
    email: Mapped[str] = db.Column(db.String(120), unique=True, nullable=False)

    notes: Mapped[list[Note]] = db.relationship("Note", backref="users", cascade="all, delete-orphan")

    def to_json(self) -> dict[str, str|int]:
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
        }
