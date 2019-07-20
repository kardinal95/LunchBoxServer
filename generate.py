import os

import sqlalchemy as db

from py.db.models.role import Role
from py.db.models.user import User


def connect():
    mode = os.getenv('FLASK_ENV')
    if mode == 'Development':
        return db.create_engine(os.getenv('DB_DEFAULT_URI'))
    else:
        return db.create_engine(os.getenv('DB_PROD_URI'))


def fill(engine):
    user = User(id=1, login='admin')
    user.set_password('admin')

    role = Role(id=1, name='superrole')



    connection = engine.connect('')