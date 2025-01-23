from flask import Flask, Response, render_template, make_response


class ClientController:
    @staticmethod
    def register(app: Flask) -> None:
        @app.route("/client", methods=["GET"])
        def get_users() -> Response:
            return make_response(render_template("get_clients.html"), 200)

        @app.route("/client/<int:client_id>", methods=["GET"])
        def get_user(client_id: int) -> Response:
            return make_response(render_template("get_client.html", client_id=client_id), 200)
