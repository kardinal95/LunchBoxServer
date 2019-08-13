from py.db.models.role import Role
from py.db.models.user import User


class AuthModel:
    def __init__(self, params):
        self.login = params['login']
        self.password = params['password']


class PassChangeModel:
    def __init__(self, user_id, params):
        self.user_id = user_id
        self.old = params['old']
        self.new = params['new']


class NewUserModel:
    def __init__(self, params):
        self.login = params['login']
        self.password = params['password']
        self.name = None if 'name' not in params.keys() else params['name']
        self.phone = None if 'phone' not in params.keys() else params['phone']


class UserModel:
    def __init__(self, user: User):
        self.id = user.id
        self.login = user.login
        self.name = user.name
        self.phone = user.phone

    def as_json(self):
        return {
            'id': self.id,
            'login': self.login,
            'name': self.name,
            'phone': self.phone
        }


class RoleModel:
    def __init__(self, role: Role):
        self.id = role.id
        self.name = role.name

    def as_json(self):
        return {
            'id': self.id,
            'name': self.name
        }
