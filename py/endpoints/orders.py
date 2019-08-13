from py.exceptions import BaseLBSException
from py.lib import has_required_role
from py.models.orders import InputOrderModel, OrderItemModel, ClientOrderModel
from py.operations.orders import make_new_order, get_orders_for_user, get_order_items, get_order_for_user, \
    cancel_order_for_user, get_active_orders, confirm_order, get_late_orders, refuse_order


def make_new_order_ep(user, body):
    if not has_required_role(user, 'client'):
        return 'Недопустимо для текущего пользователя', 403

    order = InputOrderModel(user, body)
    try:
        make_new_order(order)
        return 'Успех', 200
    except BaseLBSException as e:
        return e.response()


def get_orders_ep(user):
    if not has_required_role(user, 'client'):
        return 'Недопустимо для текущего пользователя', 403

    orders = get_orders_for_user(user)

    result = list()
    for order in orders:
        items = get_order_items(order.id)
        order_items = [OrderItemModel(x[0], x[1]) for x in items]
        result.append(ClientOrderModel(order, order_items))

    return [x.as_json() for x in result], 200


def get_order_ep(user, id):
    if not has_required_role(user, 'client'):
        return 'Недопустимо для текущего пользователя', 403

    try:
        order = get_order_for_user(user, id)
        items = get_order_items(order.id)
        order_items = [OrderItemModel(x[0], x[1]) for x in items]
        return ClientOrderModel(order, order_items).as_json(), 200
    except BaseLBSException as e:
        return e.response()


def cancel_order_ep(user, id):
    if not has_required_role(user, 'client'):
        return 'Недопустимо для текущего пользователя', 403

    try:
        cancel_order_for_user(user, id)
        return 'Успех', 200
    except BaseLBSException as e:
        return e.response()


def manage_get_orders_active_ep(user):
    if not has_required_role(user, 'order manager'):
        return 'Недопустимо для текущего пользователя', 403

    orders = get_active_orders()

    result = list()
    for order in orders:
        items = get_order_items(order.id)
        order_items = [OrderItemModel(x[0], x[1]) for x in items]
        result.append(ClientOrderModel(order, order_items))

    return [x.as_json() for x in result], 200


def manage_confirm_order_ep(user, id):
    if not has_required_role(user, 'order manager'):
        return 'Недопустимо для текущего пользователя', 403

    try:
        confirm_order(id)
        return 'Успех', 200
    except BaseLBSException as e:
        return e.response()


def manage_get_late_orders_ep(user):
    if not has_required_role(user, 'order manager'):
        return 'Недопустимо для текущего пользователя', 403

    orders = get_late_orders()

    result = list()
    for order in orders:
        items = get_order_items(order.id)
        order_items = [OrderItemModel(x[0], x[1]) for x in items]
        result.append(ClientOrderModel(order, order_items))

    return [x.as_json() for x in result], 200


def manage_refuse_order_ep(user, id):
    if not has_required_role(user, 'order manager'):
        return 'Недопустимо для текущего пользователя', 403

    try:
        refuse_order(id)
        return 'Успех', 200
    except BaseLBSException as e:
        return e.response()