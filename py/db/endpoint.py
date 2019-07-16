from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


class DatabaseEndpoint:
    db = SQLAlchemy()
    migrate = None

    @staticmethod
    def init_app(app):
        DatabaseEndpoint.db.init_app(app)
        DatabaseEndpoint.migrate = Migrate(app, DatabaseEndpoint.db)