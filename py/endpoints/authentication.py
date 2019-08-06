from py.exceptions import BaseLBSException
from py.models.users import AuthModel
from py.operations.authentication import refresh, authorize, validate


def authorize_ep(body):
    model = AuthModel(body)

    try:
        token = authorize(model)
        return token, 200
    except BaseLBSException as e:
        return e.response()


def refresh_ep(user):
    token = refresh(user)
    return token, 200


def validate_ep(token_info):
    return validate(token_info), 200
