import os
import time
from datetime import datetime

import six
from jose import jwt, JWTError
from werkzeug.exceptions import Unauthorized

from py.db.models.user import User
from py.exceptions import IncorrectLogin
from py.models.users import AuthModel


def _current_timestamp() -> int:
    return int(time.time())


def _generate_token(user: User) -> str:
    timestamp = _current_timestamp()
    payload = {
        'iss': os.getenv('JWT_ISSUER'),
        'iat': int(timestamp),
        'exp': int(timestamp + int(os.getenv('JWT_LIFETIME_SECONDS'))),
        'sub': str(user.id)
    }

    return jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm=os.getenv('JWT_ALGORITHM'))


def authorize(model: AuthModel) -> str:
    user = User.query.filter_by(login=model.login).first()

    if user is None or not user.check_password(model.password):
        raise IncorrectLogin()

    return _generate_token(user)


def refresh(user: int) -> str:
    return _generate_token(User.query.filter_by(id=user).first())


def validate(token_info: dict) -> str:
    result = 'Корректный токен. '
    result += 'Конец срока действия: {} по серверному времени. ' \
        .format(datetime.fromtimestamp(token_info['exp'])
                .strftime('%Y-%m-%d %H:%M:%S'))
    result += 'Текущее серверное время: {}.' \
        .format(datetime.fromtimestamp(_current_timestamp())
                .strftime('%Y-%m-%d %H:%M:%S'))
    return result


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=[os.getenv('JWT_ALGORITHM')])
    except JWTError as e:
        six.raise_from(Unauthorized, e)
