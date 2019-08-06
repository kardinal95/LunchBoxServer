from py.exceptions import BaseLBSException
from py.models.common import TimeslotModel, OrderStatusModel
from py.operations.common import get_timeslots, get_statuses


def get_timeslots_ep():
    try:
        slots = get_timeslots()
        return [TimeslotModel(x).as_json() for x in slots], 200
    except BaseLBSException as e:
        return e.response()


def get_statuses_ep():
    statuses = get_statuses()
    return [OrderStatusModel(x).as_json() for x in statuses], 200