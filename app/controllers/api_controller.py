from PIL import Image
from PIL.ImageFile import ImageFile
from flask import Flask, request, jsonify, make_response, Response
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.models.user import User
from app.models.note import Note
from app import db

import pytesseract
import os


class ApiController:
    @staticmethod
    def register(app: Flask) -> None:
        @app.route("/api/user", methods=["POST"])
        def api_add_user() -> Response:
            if request.is_json:
                data = request.json
            else:
                data = request.form

            name: str = data.get("name", "")
            surname: str = data.get("surname", "")
            email: str = data.get("email", "")

            if not name or not surname or not email:
                return make_response(jsonify({ "success": False, "error": "Missing required fields" }), 400)

            if User.query.filter_by(email=email).first():
                return make_response(jsonify({ "success": False, "error": "Email already in use" }), 409)

            user: User = User(name=name, surname=surname, email=email)

            db.session.add(user)
            db.session.commit()

            return make_response(
                jsonify(
                    {
                        "success": True,
                        "data": user.to_json()
                    }
                ),
                201
            )

        @app.route("/api/user", methods=["GET"])
        def api_get_users() -> Response:

            users: list[User] = User.query.all()

            return make_response(
                jsonify(
                    {
                        "success": True,
                        "data": [user.to_json() for user in users]
                    }
                ),
                200
            )

        @app.route("/api/user/<int:user_id>", methods=["GET"])
        def api_get_user(user_id: int) -> Response:
            user: User|None = User.query.get(user_id)

            if not user:
                return make_response(jsonify({ "success": False, "error": "User does not exist" }), 404)

            return make_response(
                jsonify(
                    {
                        "success": True,
                        "data": user.to_json()
                    }
                ),
                200
            )

        @app.route("/api/user/<int:user_id>", methods=["PUT"])
        def api_update_user(user_id: int) -> Response:
            if request.is_json:
                data = request.json
            else:
                data = request.form
            user: User|None = User.query.get(user_id)

            if not user:
                return make_response(jsonify({ "success": False, "error": "User does not exist" }), 404)

            if User.query.filter(User.email == request.json.get("email"), User.id != user.id).first():
                return make_response(jsonify({ "success": False, "error": "Email already in use" }), 409)

            user.name = data.get("name", user.name)
            user.surname = data.get("surname", user.surname)
            user.email = data.get("email", user.email)

            db.session.commit()

            return make_response(
                jsonify(
                    {
                        "success": True,
                        "data": user.to_json()
                    }
                ),
                200
            )

        @app.route("/api/user/<int:user_id>", methods=["DELETE"])
        def api_delete_user(user_id: int) -> Response:
            user: User|None = User.query.get(user_id)

            if not user:
                return make_response(jsonify({ "success": False, "error": "User does not exist" }), 404)

            db.session.delete(user)
            db.session.commit()

            return make_response(
                jsonify(
                    {
                        "success": True,
                        "data": {}
                    }
                ),
                200
            )

        @app.route("/api/user/<int:user_id>/note", methods=["POST"])
        def api_create_note(user_id: int) -> Response:
            if request.is_json:
                data = request.json
            else:
                data = request.form
            if not User.query.get(user_id):
                return make_response(jsonify({"success": False, "error": "User does not exist"}), 404)

            title: str = data.get("title", "")
            content: str = data.get("content", "")

            if not title or not content:
                return make_response(jsonify({"success": False, "error": "Missing required fields"}), 400)

            note: Note = Note(user_id=user_id, title=title, content=content)

            db.session.add(note)
            db.session.commit()

            return make_response(
                jsonify(
                    {
                        "success": True,
                        "data": note.to_json()
                    }
                ),
                201
            )

        @app.route("/api/user/<int:user_id>/note/upload", methods=["POST"])
        def api_upload_note(user_id: int) -> Response:
            if not User.query.get(user_id):
                return make_response(jsonify({"success": False, "error": "User does not exist"}), 404)

            note_image: FileStorage|None = request.files.get("note")

            if not note_image:
                return make_response(jsonify({"success": False, "error": "Missing required image file"}), 400)

            filename: str = secure_filename(note_image.filename)
            path: str = os.path.join(app.config["CACHE_DIRECTORY"], filename)

            note_image.save(path)

            image: ImageFile = Image.open(path)
            content: str = pytesseract.image_to_string(image, lang="pol")

            os.remove(path)

            note: Note = Note(user_id=user_id, title=filename, content=content)

            db.session.add(note)
            db.session.commit()

            return make_response(
                jsonify(
                    {
                        "success": True,
                        "data": note.to_json(),
                        "test": path
                    }
                ),
                201
            )

        @app.route("/api/user/<int:user_id>/note", methods=["GET"])
        def api_get_notes(user_id: int) -> Response:
            if not User.query.get(user_id):
                return make_response(jsonify({ "success": False, "error": "User does not exist" }), 404)

            notes: list[Note] = Note.query.filter(Note.user_id == user_id).all()

            return make_response(
                jsonify(
                    {
                        "success": True,
                        "data": [note.to_json() for note in notes]
                    }
                ),
                200
            )

        @app.route("/api/user/<int:user_id>/note/<int:note_id>", methods=["GET"])
        def api_get_note(user_id: int, note_id: int) -> Response:
            if not User.query.get(user_id):
                return make_response(jsonify({ "success": False, "error": "User does not exist" }), 404)

            if not Note.query.get(note_id):
                return make_response(jsonify({ "success": False, "error": "Note does not exist" }), 404)

            note: Note|None = Note.query.filter(Note.user_id == user_id, Note.id == note_id).first()

            if not note:
                return make_response(jsonify({ "success": False, "error": "Note is not accessible in the user scope" }), 401)

            return make_response(
                jsonify(
                    {
                        "success": True,
                        "data": note.to_json()
                    }
                ),
                200
            )

        @app.route("/api/user/<int:user_id>/note/<int:note_id>", methods=["PUT"])
        def api_update_note(user_id: int, note_id: int) -> Response:
            if not User.query.get(user_id):
                return make_response(jsonify({ "success": False, "error": "User does not exist" }), 404)

            if not Note.query.get(note_id):
                return make_response(jsonify({"success": False, "error": "Note does not exist"}), 404)

            note: Note|None = Note.query.filter(Note.user_id == user_id, Note.id == note_id).first()

            if not note:
                return make_response(jsonify({"success": False, "error": "Note is not accessible in the user scope"}), 401)

            note.title = request.json.get("title", note.title)
            note.content = request.json.get("content", note.content)

            db.session.commit()

            return make_response(
                jsonify(
                    {
                        "success": True,
                        "data": note.to_json()
                    }
                ),
                200
            )

        @app.route("/api/user/<int:user_id>/note/<int:note_id>", methods=["DELETE"])
        def api_delete_note(user_id: int, note_id: int) -> Response:
            if not User.query.get(user_id):
                return make_response(jsonify({ "success": False, "error": "User does not exist" }), 404)

            if not Note.query.get(note_id):
                return make_response(jsonify({"success": False, "error": "Note does not exist"}), 404)

            note: Note|None = Note.query.filter(Note.user_id == user_id, Note.id == note_id).first()

            if not note:
                return make_response(jsonify({"success": False, "error": "Note is not accessible in the user scope"}), 401)

            db.session.delete(note)
            db.session.commit()

            return make_response(
                jsonify(
                    {
                        "success": True,
                        "data": {}
                    }
                ),
                200
            )
