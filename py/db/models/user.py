from passlib.apps import custom_app_context as pwd_context

from py.db.endpoint import DatabaseEndpoint as de


class User(de.db.Model):
    __tablename__ = 'users'
    __title__ = 'пользователь'
    id = de.db.Column(de.db.Integer, primary_key=True)
    name = de.db.Column(de.db.String(80), nullable=True)
    phone = de.db.Column(de.db.String(80), nullable=True)
    login = de.db.Column(de.db.String(80), nullable=False, unique=True)
    passhash = de.db.Column(de.db.String(128), nullable=False)

    def set_password(self, password):
        self.passhash = pwd_context.hash(password)

    def check_password(self, password):
        return pwd_context.verify(password, self.passhash)
