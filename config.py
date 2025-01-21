class Config:
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    CACHE_FOLDER: str = "cache/"
