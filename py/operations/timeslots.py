import timestring as ts

from py.db.models.timeslot import Timeslot
from py.exceptions import ServiceNotWorking
from py.settings import Settings


def _get_current_borders(current):
    deadzone = Settings.main['config']['timeslots']['deadzone']

    borders = None
    schedule = Settings.main['schedule']
    for item in schedule.keys():
        if ts.Date(item).weekday == current.weekday:
            borders = (ts.Date(schedule[item]['start']) + deadzone,
                       ts.Date(schedule[item]['end']) - deadzone)

    if borders is None:
        raise ServiceNotWorking()
    return borders


def get_timeslot(timeslot_id):
    if timeslot_id is None:
        return None
    return Timeslot.query.filter_by(id=timeslot_id).first()


def get_available_timeslots():
    current = ts.Date('now')
    borders = _get_current_borders(current)

    slots = Timeslot.query.filter(Timeslot.time_start >= current.date.time()). \
        filter(Timeslot.time_start >= borders[0].date.time()). \
        filter(Timeslot.time_end <= borders[1].date.time()).all()

    from py.operations.orders import get_orders_with_timeslot
    filtered = [x for x in slots if len(get_orders_with_timeslot(x.id)) < x.capacity]

    return filtered
