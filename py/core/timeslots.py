from itertools import groupby

import timestring as ts

from py.db.models.order import Order
from py.db.models.timeslot import Timeslot
from py.settings import Settings


def get_timeslots():
    current = ts.Date('now')
    deadzone = Settings.main['config']['timeslots']['deadzone']

    borders = None
    schedule = Settings.main['schedule']
    for item in schedule.keys():
        if ts.Date(item).weekday == current.weekday:
            borders = (ts.Date(schedule[item]['start']) + deadzone,
                       ts.Date(schedule[item]['end']) - deadzone)

    if borders is None:
        return 'Сервис не работает в текущий день', 400

    slots = Timeslot.query.filter(Timeslot.time_start >= current.date.time()).\
        filter(Timeslot.time_start >= borders[0].date.time()).\
        filter(Timeslot.time_end <= borders[1].date.time()).all()

    orders = Order.query.filter_by(status_id=1).all()
    filtered = {key: value for key, value in groupby(orders, lambda x: x.timeslot_id)}
    print(filtered)

    if slots is None:
        return 'Нет доступных промежутков времени', 400

    return [x.as_json() for x in slots]