from typing import List

import timestring as ts

from py.db.models.order_status import OrderStatus
from py.db.models.timeslot import Timeslot
from py.exceptions import ServiceNotWorking
from py.settings import Settings


def get_timeslots() -> List[Timeslot]:
    current = ts.Date('now')
    deadzone = Settings.main['config']['timeslots']['deadzone']

    borders = None
    schedule = Settings.main['schedule']
    for item in schedule.keys():
        if ts.Date(item).weekday == current.weekday:
            borders = (ts.Date(schedule[item]['start']) + deadzone,
                       ts.Date(schedule[item]['end']) - deadzone)

    if borders is None:
        raise ServiceNotWorking()

    slots = Timeslot.query.filter(Timeslot.time_start >= current.date.time()). \
        filter(Timeslot.time_start >= borders[0].date.time()). \
        filter(Timeslot.time_end <= borders[1].date.time()).all()

    # TODO Check existing orders and capacity her

    return slots


def get_statuses():
    return OrderStatus.query.all()
