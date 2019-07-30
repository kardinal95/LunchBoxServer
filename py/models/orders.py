from py.db.models.order import Order
from py.models.lunchboxes import ClientLunchboxModel


class InputOrderModel:
    def __init__(self, user_id, params):
        self.user_id = user_id
        self.lunchbox_ids = params['boxes']
        self.timeslot_id = params['timeslot']


class ClientOrderModel:
    def __init__(self, order: Order, items):
        self.id = order.id
        self.status_id = order.status_id
        self.items = items
        self.timeslot_id = order.timeslot_id
        self.created = order.created_at

    def as_json(self):
        return {
            'id': self.id,
            'status_id': self.status_id,
            'items': [x.as_json() for x in self.items],
            'timeslot_id': self.timeslot_id,
            'created': self.created
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
