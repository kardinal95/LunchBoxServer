from py.db.endpoint import DatabaseEndpoint as de
from py.db.models.lunchbox import Lunchbox
from py.db.models.order import Order
from py.db.models.order_item import OrderItem
from py.exceptions import MaxOrderExceeded, IncorrectLunchbox, IncorrectTimeslot, MaxOrderItemExceed, TargetNotExists
from py.models.orders import InputOrderModel
from py.operations.lunchboxes import get_lunchbox_simple
from py.operations.timeslots import get_available_timeslots, get_timeslot
from py.settings import Settings


def get_orders_for_user(user_id):
    return Order.query.filter_by(client_id=user_id).all()


def get_order_items(order_id):
    items = OrderItem.query.filter_by(order_id=order_id).all()
    if len(items) == 0:
        raise TargetNotExists(Order, [order_id])
    boxes_raw = {x.lunchbox_id: x.quantity for x in items}
    boxes = {x.id: x for x in Lunchbox.query.filter(Lunchbox.id.in_(boxes_raw.keys())).all()}

    return [(boxes[x[0]], x[1]) for x in boxes_raw.items()]


def get_orders_with_timeslot(timeslot_id):
    return Order.query.filter_by(timeslot_id=timeslot_id).all()


def make_new_order(order: InputOrderModel) -> (str, int):
    max_orders = Settings.main['config']['client']['maxOrders']
    current_orders = len([x for x in get_orders_for_user(order.user_id) if x.status_id == 1])
    if current_orders >= max_orders:
        raise MaxOrderExceeded(current_orders, max_orders)

    max_items_in_order = Settings.main['config']['client']['maxOrderItems']
    current_items = len(order.lunchbox_ids)
    if current_items > max_items_in_order:
        raise MaxOrderItemExceed(current_items, max_items_in_order)

    for lunchbox_id in order.lunchbox_ids:
        lunchbox = get_lunchbox_simple(lunchbox_id)
        if lunchbox.archived or not lunchbox.stock or not lunchbox.locked:
            raise IncorrectLunchbox()

    slots_ids = [x.id for x in get_available_timeslots()]
    if order.timeslot_id not in slots_ids:
        raise IncorrectTimeslot()
    slot_orders = get_orders_with_timeslot(order.timeslot_id)
    slot_orders = [x for x in slot_orders if x.status_id == 1]
    timeslot = get_timeslot(order.timeslot_id)
    if len(slot_orders) > timeslot.capacity:
        raise IncorrectTimeslot()

    target = Order(
        client_id=order.user_id,
        status_id=1,
        timeslot_id=order.timeslot_id
    )
    de.db.session.add(target)
    de.db.session.flush()

    for item in order.lunchbox_ids:
        order_item = OrderItem(
            order_id=target.id,
            lunchbox_id=item,
            quantity=1)
        de.db.session.add(order_item)
    de.db.session.commit()

    return 'Успех', 200