from py.exceptions import BaseLBSException
from py.lib import has_required_role
from py.models.orders import InputOrderModel, OrderItemModel, ClientOrderModel
from py.operations.orders import make_new_order, get_orders_for_user, get_order_items


def make_new_order_ep(user, body):
    if not has_required_role(user, 'client'):
        return 'Недопустимо для текущего пользователя', 403

    order = InputOrderModel(user, body)
    try:
        return make_new_order(order)
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