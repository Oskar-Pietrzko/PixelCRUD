from sqlalchemy.orm import Mapped

from app import db

class Note(db.Model):
    __tablename__: str = "notes"

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    client_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False, index=True)
    title: Mapped[str] = db.Column(db.String(100), nullable=False)
    content: Mapped[str] = db.Column(db.Text, nullable=False)

    def to_json(self) -> dict[str, str|int]:
        return {
            "id": self.id,
            "client_id": self.client_id,
            "title": self.title,
            "content": self.content,
        }
