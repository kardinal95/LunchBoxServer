from py.exceptions import BaseLBSException
from py.lib import has_required_role
from py.models.users import PassChangeModel, NewUserModel, UserModel, RoleModel
from py.operations.users import change_current_password, add_user, get_user_with_id, get_roles, get_user_with_id_roles, \
    edit_user_with_id_roles


def change_current_password_ep(user, body):
    model = PassChangeModel(user, body)

    try:
        change_current_password(model)
        return 'Успех', 200
    except BaseLBSException as e:
        return e.response()


def add_user_ep(user, body):
    if not has_required_role(user, 'user manager'):
        return 'Not allowed for current user', 403

    model = NewUserModel(body)
    try:
        user = add_user(model)
        return UserModel(user).as_json(), 200
    except BaseLBSException as e:
        return e.response()


def get_user_with_id_ep(user, id):
    if not has_required_role(user, 'user manager'):
        return 'Not allowed for current user', 403

    try:
        user = get_user_with_id(id)
        return UserModel(user).as_json(), 200
    except BaseLBSException as e:
        return e.response()


def get_roles_ep(user):
    if not has_required_role(user, 'user manager'):
        return 'Not allowed for current user', 403

    roles = get_roles()
    return [RoleModel(role).as_json() for role in roles], 200


def get_user_with_id_roles_ep(user, id):
    if not has_required_role(user, 'user manager'):
        return 'Not allowed for current user', 403

    try:
        roles = get_user_with_id_roles(id)
        return [RoleModel(role).as_json() for role in roles], 200
    except BaseLBSException as e:
        return e.response()


def edit_user_with_id_roles_ep(user, id, body):
    if not has_required_role(user, 'user manager'):
        return 'Not allowed for current user', 403

    try:
        roles = edit_user_with_id_roles(id, body)
        return [RoleModel(role).as_json() for role in roles], 200
    except BaseLBSException as e:
        return e.response()
