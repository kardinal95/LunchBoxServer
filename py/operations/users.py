from typing import List

from py.db.endpoint import DatabaseEndpoint as de
from py.db.models.role import Role
from py.db.models.user import User
from py.db.models.user_role import UserRole
from py.exceptions import IncorrectPassword, TargetAlreadyExists, TargetNotExists
from py.models.users import PassChangeModel, NewUserModel


def change_current_password(model: PassChangeModel) -> None:
    user = User.query.filter_by(id=model.user_id).first()

    if not user.check_password(model.old):
        raise IncorrectPassword()

    user.set_password(model.new)

    de.db.session.add(user)
    de.db.session.commit()


def add_user(model: NewUserModel) -> User:
    existing = User.query.filter_by(login=model.login).first()
    if existing is not None:
        raise TargetAlreadyExists(User)

    user = User(
        login=model.login,
        name=model.name,
        phone=model.phone
    )
    user.set_password(model.password)

    de.db.session.add(user)
    de.db.session.commit()

    return user


def get_user_with_id(index: int) -> User:
    user = User.query.filter_by(id=index).first()
    if user is None:
        raise TargetNotExists(User, [index])

    return user


def get_roles() -> List[Role]:
    roles = Role.query.all()
    return roles


def get_user_with_id_roles(index: int) -> List[Role]:
    if User.query.filter_by(id=index).first() is None:
        raise TargetNotExists(User, [index])

    user_roles = UserRole.query.filter_by(user_id=index).all()
    indexes = [x.role_id for x in user_roles]
    roles = Role.query.filter(Role.id.in_(indexes)).all()

    return roles


def edit_user_with_id_roles(index, roles: List[int]) -> List[Role]:
    if User.query.filter_by(id=index).first() is None:
        raise TargetNotExists(User, [index])

    target = set(roles)
    available = set([x.id for x in Role.query.all()])

    if not target <= available:
        raise TargetNotExists(Role, list(target - available)[0])

    user_roles = UserRole.query.filter_by(user_id=index)
    existing = set([x.role_id for x in user_roles.all()])
    leftover = existing - target
    target = target - existing

    for item in user_roles.filter(UserRole.role_id.in_(leftover)).all():
        de.db.session.delete(item)

    for role_id in target:
        ur = UserRole(user_id=index, role_id=role_id)
        de.db.session.add(ur)
    de.db.session.commit()

    return get_user_with_id_roles(index)
