from py.db.models.order_status import OrderStatus


def get_statuses():
    statuses = OrderStatus.query.all()

    return [x.as_json() for x in statuses]