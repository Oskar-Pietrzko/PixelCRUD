import os


class Config:
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    BASE_DIRECTORY: str = os.path.abspath(os.path.dirname(__file__))
    CACHE_DIRECTORY: str = os.path.join(BASE_DIRECTORY, "instance")
