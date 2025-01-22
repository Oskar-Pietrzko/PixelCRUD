from flask import Flask, Response, render_template, make_response


class UserController:
    @staticmethod
    def register(app: Flask) -> None:
        @app.route("/user", methods=["GET"])
        def get_users() -> Response:
            return make_response(render_template("get_users.html"), 200)

        @app.route("/user/<int:user_id>", methods=["GET"])
        def get_user(user_id: int) -> Response:
            return make_response(render_template("get_user.html", user_id=user_id), 200)
