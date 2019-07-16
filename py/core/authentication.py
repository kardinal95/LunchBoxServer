import os
import time

import six
from jose import jwt, JWTError
from datetime import datetime

from werkzeug.exceptions import Unauthorized

from py.db.models.user import User


def _current_timestamp() -> int:
    return int(time.time())


def generate_token(user):
    timestamp = _current_timestamp()
    payload = {
        'iss': os.getenv('JWT_ISSUER'),
        'iat': int(timestamp),
        'exp': int(timestamp + int(os.getenv('JWT_LIFETIME_SECONDS'))),
        'sub': str(user.id)
    }

    return jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm=os.getenv('JWT_ALGORITHM'))


def decode_token(token):
    try:
        return jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=[os.getenv('JWT_ALGORITHM')])
    except JWTError as e:
        six.raise_from(Unauthorized, e)


def authorize(body):
    # TODO Incorrect parameters
    login = body['login']
    user = User.query.filter_by(login=login).first()

    if user is None or not user.check_password(body['password']):
        return "Authentication unsuccessful", 400

    return generate_token(user)


def validate(token_info):
    result = 'Correct token. '
    result += 'Token end time: {} on server time. '\
        .format(datetime.fromtimestamp(token_info['exp'])
                .strftime('%Y-%m-%d %H:%M:%S'))
    result += 'Current server time: {}.'\
        .format(datetime.fromtimestamp(_current_timestamp())
                .strftime('%Y-%m-%d %H:%M:%S'))
    return result