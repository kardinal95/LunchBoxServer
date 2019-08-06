from py.db.models.order_status import OrderStatus
from py.db.models.timeslot import Timeslot


class TimeslotModel:
    def __init__(self, timeslot: Timeslot):
        self.id = timeslot.id
        self.time_start = timeslot.time_start
        self.time_end = timeslot.time_end

    def as_json(self):
        return {
            'id': self.id,
            'time_start': str(self.time_start),
            'time_end': str(self.time_end)
        }


class OrderStatusModel:
    def __init__(self, stat: OrderStatus):
        self.id = stat.id
        self.name = stat.name

    def as_json(self):
        return {
            'id': self.id,
            'name': self.name
        }
