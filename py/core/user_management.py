from py.db.models.user import User

from py.db.endpoint import DatabaseEndpoint as de
from py.lib import has_required_role


def change_password(user, body):
    # TODO Verification
    password = body['password']
    user = User.query.filter_by(id=user).first()
    user.set_password(password)

    de.db.session.add(user)
    de.db.session.commit()


def add_user(user, body):
    if not has_required_role(user, 'user manager'):
        return 'Not allowed for current user', 403

    existing = User.query.filter_by(login=body['login']).first()
    if existing is not None:
        return 'User with this login already exists', 400

    new_user = User(
        name='' if 'name' not in body.keys() else body['name'],
        phone='' if 'phone' not in body.keys() else body['phone'],
        login=body['login']
    )
    new_user.set_password(body['password'])

    de.db.session.add(new_user)
    de.db.session.commit()

    return 'User successfully added', 200
