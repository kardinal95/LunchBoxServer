from py.db.models.order import Order
from py.db.models.timeslot import Timeslot
from py.models.common import TimeslotModel
from py.models.lunchboxes import ClientLunchboxModel


class InputOrderModel:
    def __init__(self, user_id, params):
        self.user_id = user_id
        self.lunchbox_ids = params['boxes']
        self.timeslot_id = params['timeslot']


class ClientOrderModel:
    def __init__(self, order: Order, items, timeslot: Timeslot):
        self.id = order.id
        self.status_id = order.status_id
        self.items = items
        self.timeslot = None if timeslot is None else TimeslotModel(timeslot)
        self.created = order.created_at

    def as_json(self):
        return {
            'id': self.id,
            'status_id': self.status_id,
            'items': [x.as_json() for x in self.items],
            'timeslot': self.timeslot.as_json() if self.timeslot is not None else None,
            'created': str(self.created)
        }


class OrderItemModel:
    def __init__(self, lunchbox, quantity):
        self.lunchbox = ClientLunchboxModel(lunchbox)
        self.quantity = quantity

    def as_json(self):
        return {
            'lunchbox': self.lunchbox.as_json(),
            'quantity': self.quantity
        }
