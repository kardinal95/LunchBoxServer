from typing import List, Tuple

import timestring as ts

from py.db.endpoint import DatabaseEndpoint as de
from py.db.models.lunchbox import Lunchbox
from py.db.models.order import Order
from py.db.models.order_item import OrderItem
from py.exceptions import TargetNotExists, BaseLBSException, MaxOrderExceeded, MaxOrderItemExceed, IncorrectLunchbox, \
    IncorrectTimeslot
from py.models.orders import InputOrderModel
from py.operations import timeslots
from py.operations.lunchboxes import get_lunchbox_simple
from py.settings import Settings


def _order_late(order: Order) -> bool:
    now = ts.Date('now')
    day = ts.Date('0:00')

    if order.status_id != 1:
        return False

    if ts.Date(order.created_at) < day:
        return True

    end = ts.Date(str(timeslots.get_timeslot(order.timeslot_id).time_end))
    if now > end:
        return True

    return False


def get_orders_for_user(user_id: int, status: List[int] = None) -> List[Order]:
    raw = Order.query.filter_by(client_id=user_id)
    if status is not None:
        raw = raw.filter(Order.status_id.in_(status))
    return raw.all()


def get_order_for_user(user_id: int, order_id: int) -> Order:
    order = Order.query.filter_by(client_id=user_id).filter_by(id=order_id).first()

    if order is None:
        raise TargetNotExists(Order, [order_id])

    return order


def cancel_order_for_user(user_id: int, order_id: int) -> None:
    order = get_order_for_user(user_id, order_id)

    if order.status_id != 1:
        raise BaseLBSException('Невозможно отменить заказ в данном статусе!', 400)

    now = ts.Date('now')
    start = ts.Date(str(timeslots.get_timeslot(order.timeslot_id).time_start))

    if now + Settings.main['config']['client']['cancelOrderTime'] > start:
        raise BaseLBSException('Время отмены заказа истекло!', 400)

    order_items = OrderItem.query.filter_by(order_id=order_id).all()
    for x in order_items:
        de.db.session.delete(x)
    de.db.session.delete(order)
    de.db.session.commit()


def get_order_items(order_id: int) -> List[Tuple]:
    items = OrderItem.query.filter_by(order_id=order_id).all()
    if len(items) == 0:
        raise TargetNotExists(Order, [order_id])
    boxes_raw = {x.lunchbox_id: x.quantity for x in items}
    boxes = {x.id: x for x in Lunchbox.query.filter(Lunchbox.id.in_(boxes_raw.keys())).all()}

    return [(boxes[x[0]], x[1]) for x in boxes_raw.items()]


def get_orders_with_timeslot(timeslot_id: int) -> List[Order]:
    today = ts.Date('0:00')
    orders = Order.query.filter_by(timeslot_id=timeslot_id).all()
    filtered = [x for x in orders if ts.Date(x.created_at) > today]
    return filtered


def make_new_order(order: InputOrderModel) -> None:
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

    slots_ids = [x.id for x in timeslots.get_available_timeslots()]
    if order.timeslot_id not in slots_ids:
        raise IncorrectTimeslot()
    slot_orders = get_orders_with_timeslot(order.timeslot_id)
    slot_orders = [x for x in slot_orders if x.status_id == 1]
    timeslot = timeslots.get_timeslot(order.timeslot_id)
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


def get_active_orders() -> List[Order]:
    orders = Order.query.filter_by(status_id=1).all()
    filtered = [x for x in orders if not _order_late(x)]

    return filtered


def get_late_orders() -> List[Order]:
    orders = Order.query.filter_by(status_id=1).all()
    filtered = [x for x in orders if _order_late(x)]

    return filtered


def confirm_order(order_id: int) -> None:
    order = Order.query.filter_by(id=order_id).first()
    if order is None:
        raise TargetNotExists(Order, [order_id])
    if order.status_id != 1:
        raise BaseLBSException('Некорректный статус у целевого заказа!', 400)
    order.status_id = 3
    order.timeslot_id = None

    de.db.session.add(order)
    de.db.session.commit()


def refuse_order(order_id: int) -> None:
    order = Order.query.filter_by(id=order_id).first()
    if order is None:
        raise TargetNotExists(Order, [order_id])
    if not _order_late(order):
        raise BaseLBSException('Некорректный статус у целевого заказа!', 400)

    order.status_id = 2
    order.timeslot_id = None

    de.db.session.add(order)
    de.db.session.commit()