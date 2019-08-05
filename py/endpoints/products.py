from py.exceptions import BaseLBSException
from py.lib import has_required_role
from py.models.products import ProductModel, ProductEditModel
from py.operations.products import get_products, get_product_with_id, edit_product_with_id, remove_product_with_id, \
    archive_product_with_id, lock_product_with_id, add_product


def get_products_ep(user, archived, locked):
    if not has_required_role(user, 'product manager'):
        return 'Недопустимо для текущего пользователя', 403

    products = get_products(archived, locked)

    return [ProductModel(item).as_json() for item in products], 200


def get_product_with_id_ep(user, id):
    if not has_required_role(user, 'product manager'):
        return 'Недопустимо для текущего пользователя', 403

    try:
        product = get_product_with_id(id)
        return ProductModel(product).as_json(), 200
    except BaseLBSException as e:
        return e.response()


def edit_product_with_id_ep(user, id, body):
    if not has_required_role(user, 'product manager'):
        return 'Недопустимо для текущего пользователя', 403

    try:
        product = edit_product_with_id(id, ProductEditModel(body))
        return ProductModel(product).as_json(), 200
    except BaseLBSException as e:
        return e.response()


def remove_product_with_id_ep(user, id):
    if not has_required_role(user, 'product manager'):
        return 'Недопустимо для текущего пользователя', 403

    try:
        remove_product_with_id(id)
        return 'Успех', 200
    except BaseLBSException as e:
        return e.response()


def archive_product_with_id_ep(user, id):
    if not has_required_role(user, 'product manager'):
        return 'Недопустимо для текущего пользователя', 403

    try:
        product = archive_product_with_id(id)
        return ProductModel(product).as_json(), 200
    except BaseLBSException as e:
        return e.response()


def lock_product_with_id_ep(user, id):
    if not has_required_role(user, 'product manager'):
        return 'Недопустимо для текущего пользователя', 403

    try:
        product = lock_product_with_id(id)
        return ProductModel(product).as_json(), 200
    except BaseLBSException as e:
        return e.response()


def add_product_ep(user, body):
    if not has_required_role(user, 'product manager'):
        return 'Недопустимо для текущего пользователя', 403

    model = ProductEditModel(body)
    try:
        product = add_product(model)
        return ProductModel(product).as_json(), 200
    except BaseLBSException as e:
        return e.response()
