import os
from PIL import Image
import pytesseract

from flask import Flask, request, jsonify, make_response
from werkzeug.utils import secure_filename

from app.models.user import User
from app.models.note import Note
from app import db

class UserController:
    @staticmethod
    def register(app: Flask):
        @app.route("/api/user", methods=["POST"])
        def add_user():
            name = request.json.get("name")
            surname = request.json.get("surname")
            email = request.json.get("email")

            if not name or not surname or not email:
                return make_response(jsonify({ "success": False, "error": "Missing required fields" }), 400)

            if User.query.filter_by(email=email).first():
                return make_response(jsonify({ "success": False, "error": "Email already in use" }), 409)

            user = User(name=name, surname=surname, email=email)

            db.session.add(user)
            db.session.commit()

            response_data = {
                "success": True,
                "data": user.to_json(),
            }

            return make_response(jsonify(response_data), 201)

        @app.route("/api/user", methods=["GET"])
        def get_users():
            users = User.query.all()

            response_data = {
                "success": True,
                "data": [user.to_json() for user in users],
            }

            return make_response(jsonify(response_data), 200)

        @app.route("/api/user/<int:user_id>", methods=["GET"])
        def get_user(user_id: int):
            user = User.query.get(user_id)

            if user is None:
                return make_response(jsonify({ "success": False, "error": "User does not exist" }), 404)

            response_data = {
                "success": True,
                "data": user.to_json(),
            }

            return make_response(jsonify(response_data), 200)

        @app.route("/api/user/<int:user_id>", methods=["PUT"])
        def update_user(user_id: int):
            user = User.query.get(user_id)

            if user is None:
                return make_response(jsonify({ "success": False, "error": "User does not exist" }), 404)

            if User.query.filter(User.email == request.json.get("email"), User.id != user.id).first():
                return make_response(jsonify({ "success": False, "error": "Email already in use" }), 409)

            user.name = request.json.get("name", user.name)
            user.surname = request.json.get("surname", user.surname)
            user.email = request.json.get("email", user.email)

            db.session.commit()

            response_data = {
                "success": True,
                "data": user.to_json(),
            }

            return make_response(jsonify(response_data), 200)

        @app.route("/api/user/<int:user_id>", methods=["DELETE"])
        def delete_user(user_id: int):
            user = User.query.get(user_id)

            if user is None:
                return make_response(jsonify({ "success": False, "error": "User does not exist" }), 404)

            db.session.delete(user)
            db.session.commit()

            response_data = {
                "success": True,
                "data": {},
            }

            return make_response(jsonify(response_data), 200)

        @app.route("/api/user/<int:user_id>/note", methods=["POST"])
        def create_note(user_id: int):
            if not User.query.get(user_id):
                return make_response(jsonify({"success": False, "error": "User does not exist"}), 404)

            title = request.json.get("title")
            content = request.json.get("content")

            if not title or not content:
                return make_response(jsonify({"success": False, "error": "Missing required fields"}), 400)

            note = Note(user_id=user_id, title=title, content=content)

            db.session.add(note)
            db.session.commit()

            response_data = {
                "success": True,
                "data": note.to_json(),
            }

            return make_response(jsonify(response_data), 201)

        @app.route("/api/user/<int:user_id>/note/upload", methods=["POST"])
        def upload_note(user_id: int):
            if not User.query.get(user_id):
                return make_response(jsonify({"success": False, "error": "User does not exist"}), 404)

            if "note" not in request.files:
                return make_response(jsonify({"success": False, "error": "Missing required image file"}), 400)

            image = request.files.get("note")

            filename = secure_filename(image.filename)
            path = os.path.join(app.root_path + "/..", app.config["CACHE_FOLDER"], filename)

            image.save(path)

            image_open = Image.open(path)
            content = pytesseract.image_to_string(image_open, lang="pol")

            os.remove(path)

            note = Note(user_id=user_id, title=filename, content=content)

            db.session.add(note)
            db.session.commit()

            response_data = {
                "success": True,
                "data": note.to_json(),
            }

            return make_response(jsonify(response_data), 201)

        @app.route("/api/user/<int:user_id>/note", methods=["GET"])
        def get_notes(user_id: int):
            if not User.query.get(user_id):
                return make_response(jsonify({ "success": False, "error": "User does not exist" }), 404)

            notes = Note.query.filter(Note.user_id == user_id).all()

            response_data = {
                "success": True,
                "data": [note.to_json() for note in notes],
            }

            return make_response(jsonify(response_data), 200)

        @app.route("/api/user/<int:user_id>/note/<int:note_id>", methods=["GET"])
        def get_note(user_id: int, note_id: int):
            if not User.query.get(user_id):
                return make_response(jsonify({ "success": False, "error": "User does not exist" }), 404)

            if not Note.query.get(note_id):
                return make_response(jsonify({ "success": False, "error": "Note does not exist" }), 404)

            note = Note.query.filter(Note.user_id == user_id, Note.id == note_id).first()

            if note is None:
                return make_response(jsonify({ "success": False, "error": "Note is not accessible in the user scope" }), 401)

            response_data = {
                "success": True,
                "data": note.to_json(),
            }

            return make_response(jsonify(response_data), 200)

        @app.route("/api/user/<int:user_id>/note/<int:note_id>", methods=["PUT"])
        def update_note(user_id: int, note_id: int):
            if not User.query.get(user_id):
                return make_response(jsonify({ "success": False, "error": "User does not exist" }), 404)

            if not Note.query.get(note_id):
                return make_response(jsonify({"success": False, "error": "Note does not exist"}), 404)

            note = Note.query.filter(Note.user_id == user_id, Note.id == note_id).first()

            if note is None:
                return make_response(jsonify({"success": False, "error": "Note is not accessible in the user scope"}), 401)

            note.title = request.json.get("title", note.title)
            note.content = request.json.get("content", note.content)

            db.session.commit()

            response_data = {
                "success": True,
                "data": note.to_json(),
            }

            return make_response(jsonify(response_data), 200)

        @app.route("/api/user/<int:user_id>/note/<int:note_id>", methods=["DELETE"])
        def delete_note(user_id: int, note_id: int):
            if not User.query.get(user_id):
                return make_response(jsonify({ "success": False, "error": "User does not exist" }), 404)

            if not Note.query.get(note_id):
                return make_response(jsonify({"success": False, "error": "Note does not exist"}), 404)

            note = Note.query.filter(Note.user_id == user_id, Note.id == note_id).first()

            if note is None:
                return make_response(jsonify({"success": False, "error": "Note is not accessible in the user scope"}), 401)

            db.session.delete(note)
            db.session.commit()

            response_data = {
                "success": True,
                "data": {},
            }

            return make_response(jsonify(response_data), 200)
