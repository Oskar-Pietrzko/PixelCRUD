from PIL import Image
from PIL.ImageFile import ImageFile
from flask import Flask, request, jsonify, make_response, Response
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.models.client import Client
from app.models.note import Note
from app import db

import pytesseract
import os


class ApiController:
    @staticmethod
    def register(app: Flask) -> None:
        @app.route("/api/client", methods=["POST"])
        def api_add_client() -> Response:
            if request.is_json:
                data = request.json
            else:
                data = request.form

            name: str = data.get("name", "")
            surname: str = data.get("surname", "")
            email: str = data.get("email", "")

            if not name or not surname or not email:
                return make_response(jsonify({ "success": False, "error": "Missing required fields" }), 400)

            if Client.query.filter_by(email=email).first():
                return make_response(jsonify({ "success": False, "error": "Email already in use" }), 409)

            client: Client = Client(name=name, surname=surname, email=email)

            db.session.add(client)
            db.session.commit()

            return make_response(
                jsonify(
                    {
                        "success": True,
                        "data": client.to_json()
                    }
                ),
                201
            )

        @app.route("/api/client", methods=["GET"])
        def api_get_clients() -> Response:

            clients: list[Client] = Client.query.all()

            return make_response(
                jsonify(
                    {
                        "success": True,
                        "data": [client.to_json() for client in clients]
                    }
                ),
                200
            )

        @app.route("/api/client/<int:client_id>", methods=["GET"])
        def api_get_client(client_id: int) -> Response:
            client: Client|None = Client.query.get(client_id)

            if not client:
                return make_response(jsonify({ "success": False, "error": "Client does not exist" }), 404)

            return make_response(
                jsonify(
                    {
                        "success": True,
                        "data": client.to_json()
                    }
                ),
                200
            )

        @app.route("/api/client/<int:client_id>", methods=["PUT"])
        def api_update_client(client_id: int) -> Response:
            if request.is_json:
                data = request.json
            else:
                data = request.form
            client: Client|None = Client.query.get(client_id)

            if not client:
                return make_response(jsonify({ "success": False, "error": "Client does not exist" }), 404)

            if Client.query.filter(Client.email == request.json.get("email"), Client.id != client.id).first():
                return make_response(jsonify({ "success": False, "error": "Email already in use" }), 409)

            client.name = data.get("name", client.name)
            client.surname = data.get("surname", client.surname)
            client.email = data.get("email", client.email)

            db.session.commit()

            return make_response(
                jsonify(
                    {
                        "success": True,
                        "data": client.to_json()
                    }
                ),
                200
            )

        @app.route("/api/client/<int:client_id>", methods=["DELETE"])
        def api_delete_client(client_id: int) -> Response:
            client: Client|None = Client.query.get(client_id)

            if not client:
                return make_response(jsonify({ "success": False, "error": "Client does not exist" }), 404)

            db.session.delete(client)
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

        @app.route("/api/client/<int:client_id>/note", methods=["POST"])
        def api_create_note(client_id: int) -> Response:
            if request.is_json:
                data = request.json
            else:
                data = request.form
            if not Client.query.get(client_id):
                return make_response(jsonify({"success": False, "error": "Client does not exist"}), 404)

            title: str = data.get("title", "")
            content: str = data.get("content", "")

            if not title:
                return make_response(jsonify({"success": False, "error": "Missing required fields"}), 400)

            note: Note = Note(client_id=client_id, title=title, content=content)

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

        @app.route("/api/client/<int:client_id>/note/upload", methods=["POST"])
        def api_upload_note(client_id: int) -> Response:
            if not Client.query.get(client_id):
                return make_response(jsonify({"success": False, "error": "Client does not exist"}), 404)

            note_image: FileStorage|None = request.files.get("note")

            if not note_image:
                return make_response(jsonify({"success": False, "error": "Missing required image file"}), 400)

            filename: str = secure_filename(note_image.filename)
            extension: str = filename.split(".")[-1]

            if extension not in ["jpg", "jpeg", "png"]:
                return make_response(jsonify({"success": False, "error": "Invalid file extension"}), 400)

            path: str = os.path.join(app.config["CACHE_DIRECTORY"], filename)

            note_image.save(path)

            image: ImageFile = Image.open(path)
            content: str = pytesseract.image_to_string(image, lang="pol")

            os.remove(path)

            note: Note = Note(client_id=client_id, title=filename, content=content)

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

        @app.route("/api/client/<int:client_id>/note", methods=["GET"])
        def api_get_notes(client_id: int) -> Response:
            if not Client.query.get(client_id):
                return make_response(jsonify({ "success": False, "error": "Client does not exist" }), 404)

            notes: list[Note] = Note.query.filter(Note.client_id == client_id).all()

            return make_response(
                jsonify(
                    {
                        "success": True,
                        "data": [note.to_json() for note in notes]
                    }
                ),
                200
            )

        @app.route("/api/client/<int:client_id>/note/<int:note_id>", methods=["GET"])
        def api_get_note(client_id: int, note_id: int) -> Response:
            if not Client.query.get(client_id):
                return make_response(jsonify({ "success": False, "error": "Client does not exist" }), 404)

            if not Note.query.get(note_id):
                return make_response(jsonify({ "success": False, "error": "Note does not exist" }), 404)

            note: Note|None = Note.query.filter(Note.client_id == client_id, Note.id == note_id).first()

            if not note:
                return make_response(jsonify({ "success": False, "error": "Note is not accessible in the client scope" }), 401)

            return make_response(
                jsonify(
                    {
                        "success": True,
                        "data": note.to_json()
                    }
                ),
                200
            )

        @app.route("/api/client/<int:client_id>/note/<int:note_id>", methods=["PUT"])
        def api_update_note(client_id: int, note_id: int) -> Response:
            if not Client.query.get(client_id):
                return make_response(jsonify({ "success": False, "error": "Client does not exist" }), 404)

            if not Note.query.get(note_id):
                return make_response(jsonify({"success": False, "error": "Note does not exist"}), 404)

            note: Note|None = Note.query.filter(Note.client_id == client_id, Note.id == note_id).first()

            if not note:
                return make_response(jsonify({"success": False, "error": "Note is not accessible in the client scope"}), 401)

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

        @app.route("/api/client/<int:client_id>/note/<int:note_id>", methods=["DELETE"])
        def api_delete_note(client_id: int, note_id: int) -> Response:
            if not Client.query.get(client_id):
                return make_response(jsonify({ "success": False, "error": "Client does not exist" }), 404)

            if not Note.query.get(note_id):
                return make_response(jsonify({"success": False, "error": "Note does not exist"}), 404)

            note: Note|None = Note.query.filter(Note.client_id == client_id, Note.id == note_id).first()

            if not note:
                return make_response(jsonify({"success": False, "error": "Note is not accessible in the client scope"}), 401)

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
