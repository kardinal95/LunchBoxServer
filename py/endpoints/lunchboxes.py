from py.exceptions import BaseLBSException
from py.lib import has_required_role
from py.models.lunchboxes import LunchboxWithProductIdsModel, LunchboxWithProductsModel, LunchboxEditModel, \
    ClientLunchboxWithProductIdsModel, ClientLunchboxWithProductsModel
from py.models.products import ProductModel, ClientProductModel
from py.operations.lunchboxes import get_lunchboxes, get_lunchbox_with_id, get_lunchbox_full_with_id, \
    get_lunchbox_products_with_id, edit_lunchbox_with_id, archive_lunchbox_with_id, lock_lunchbox_with_id, \
    stock_lunchbox_with_id, remove_lunchbox_with_id, add_lunchbox, get_pub_lunchbox_with_id, \
    get_pub_lunchbox_full_with_id, get_pub_lunchbox_products_with_id


def get_lunchboxes_ep(user, locked, archived):
    if not has_required_role(user, 'lunchbox manager'):
        return 'Недопустимо для текущего пользователя', 403

    boxes = get_lunchboxes(locked, archived)

    return [LunchboxWithProductIdsModel(x[0], x[1]).as_json() for x in boxes.items()]


def get_lunchbox_with_id_ep(id, user):
    if not has_required_role(user, 'lunchbox manager'):
        return 'Недопустимо для текущего пользователя', 403

    try:
        box = get_lunchbox_with_id(id)
        return LunchboxWithProductIdsModel(box[0], box[1]).as_json(), 200
    except BaseLBSException as e:
        return e.response()


def get_lunchbox_full_with_id_ep(id, user):
    if not has_required_role(user, 'lunchbox manager'):
        return 'Недопустимо для текущего пользователя', 403

    try:
        box = get_lunchbox_full_with_id(id)
        return LunchboxWithProductsModel(box[0], box[1]).as_json(), 200
    except BaseLBSException as e:
        return e.response()


def get_lunchbox_products_with_id_ep(id, user):
    if not has_required_role(user, 'lunchbox manager'):
        return 'Недопустимо для текущего пользователя', 403

    try:
        products = get_lunchbox_products_with_id(id)
        return [ProductModel(x).as_json() for x in products], 200
    except BaseLBSException as e:
        return e.response()


def edit_lunchbox_with_id_ep(id, body, user):
    if not has_required_role(user, 'lunchbox manager'):
        return 'Недопустимо для текущего пользователя', 403

    model = LunchboxEditModel(id, body)
    try:
        box = edit_lunchbox_with_id(model)
        return LunchboxWithProductIdsModel(box[0], box[1]).as_json(), 200
    except BaseLBSException as e:
        return e.response()


def archive_lunchbox_with_id_ep(id, user):
    if not has_required_role(user, 'lunchbox manager'):
        return 'Недопустимо для текущего пользователя', 403

    try:
        box = archive_lunchbox_with_id(id)
        return LunchboxWithProductIdsModel(box[0], box[1]).as_json(), 200
    except BaseLBSException as e:
        return e.response()


def lock_lunchbox_with_id_ep(id, user):
    if not has_required_role(user, 'lunchbox manager'):
        return 'Недопустимо для текущего пользователя', 403

    try:
        box = lock_lunchbox_with_id(id)
        return LunchboxWithProductIdsModel(box[0], box[1]).as_json(), 200
    except BaseLBSException as e:
        return e.response()


def stock_lunchbox_with_id_ep(id, stock, user):
    if not has_required_role(user, 'lunchbox manager'):
        return 'Недопустимо для текущего пользователя', 403

    try:
        box = stock_lunchbox_with_id(id, stock)
        return LunchboxWithProductIdsModel(box[0], box[1]).as_json(), 200
    except BaseLBSException as e:
        return e.response()


def remove_lunchbox_with_id_ep(id, user):
    if not has_required_role(user, 'lunchbox manager'):
        return 'Недопустимо для текущего пользователя', 403

    try:
        remove_lunchbox_with_id(id)
        return 'Успех', 200
    except BaseLBSException as e:
        return e.response()


def add_lunchbox_ep(body, user):
    if not has_required_role(user, 'lunchbox manager'):
        return 'Недопустимо для текущего пользователя', 403

    model = LunchboxEditModel(0, body)
    try:
        box = add_lunchbox(model)
        return LunchboxWithProductIdsModel(box[0], box[1]).as_json(), 200
    except BaseLBSException as e:
        return e.response()


def get_pub_lunchboxes_ep():
    boxes = get_lunchboxes(True, False)
    return [ClientLunchboxWithProductIdsModel(x[0], x[1]).as_json() for x in boxes.items()], 200


def get_pub_lunchbox_with_id_ep(id):
    try:
        box = get_pub_lunchbox_with_id(id)
        return ClientLunchboxWithProductIdsModel(box[0], box[1]).as_json(), 200
    except BaseLBSException as e:
        return e.response()


def get_pub_lunchbox_full_with_id_ep(id):
    try:
        box = get_pub_lunchbox_full_with_id(id)
        return ClientLunchboxWithProductsModel(box[0], box[1]).as_json(), 200
    except BaseLBSException as e:
        return e.response()


def get_pub_lunchbox_products_with_id_ep(id):
    try:
        products = get_pub_lunchbox_products_with_id(id)
        return [ClientProductModel(x).as_json() for x in products], 200
    except BaseLBSException as e:
        return e.response()
