from flask import Flask

from app.controllers.api_controller import ApiController
from app.controllers.user_controller import UserController


def register_routes(app: Flask) -> None:
    ApiController.register(app)
    UserController.register(app)
