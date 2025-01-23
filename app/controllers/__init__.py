from flask import Flask

from app.controllers.api_controller import ApiController
from app.controllers.client_controller import ClientController


def register_routes(app: Flask) -> None:
    ApiController.register(app)
    ClientController.register(app)
