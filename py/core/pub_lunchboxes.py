from itertools import groupby

from py.db.models.lunchbox import Lunchbox
from py.db.models.lunchbox_product import LunchboxProduct
from py.db.models.product import Product
from py.lib import has_required_role, filter_locked_and_archived

from py.db.endpoint import DatabaseEndpoint as de


def get_lunchboxes():
    raw = de.db.session.query(Lunchbox,
                              LunchboxProduct).filter(Lunchbox.id == LunchboxProduct.lunchbox_id).all()

    targets = filter_locked_and_archived(Lunchbox.query, True, False).all()

    # Группируем в формате ланчбокс: список продуктов
    filtered = {key: [x[1].product_id for x in list(value)] for key, value in groupby(raw, lambda x: x[0])}

    return [x.as_json_pub(filtered[x]) for x in filtered.keys() if x in targets], 200


def get_lunchbox_with_id(id):
    raw = de.db.session.query(Lunchbox,
                              LunchboxProduct).filter(Lunchbox.id == id,
                                                      Lunchbox.id == LunchboxProduct.lunchbox_id).all()

    if len(raw) == 0:
        return 'Не найден ланчбокс с указанным ID', 400

    # Группируем в формате ланчбокс: список продуктов
    filtered = {key: [x[1].product_id for x in list(value)] for key, value in groupby(raw, lambda x: x[0])}
    box = filtered.popitem()

    if box[0].archived or not box[0].locked:
        return 'Не найден ланчбокс с указанным ID', 400

    return box[0].as_json_pub(box[1]), 200


def get_lunchbox_full_with_id(id):
    raw = de.db.session.query(Lunchbox,
                              LunchboxProduct,
                              Product).filter(Lunchbox.id == id,
                                              Lunchbox.id == LunchboxProduct.lunchbox_id,
                                              LunchboxProduct.product_id == Product.id).all()

    if len(raw) == 0:
        return 'Не найден ланчбокс с указанным ID', 400

    # Группируем в формате ланчбокс: список продуктов
    filtered = {key: [x[2] for x in list(value)] for key, value in groupby(raw, lambda x: x[0])}
    box = filtered.popitem()

    if box[0].archived or not box[0].locked:
        return 'Не найден ланчбокс с указанным ID', 400

    return box[0].as_json_pub_full(box[1]), 200


def get_lunchbox_products_with_id(id):
    raw = de.db.session.query(LunchboxProduct,
                              Product).filter(LunchboxProduct.lunchbox_id == id,
                                              LunchboxProduct.product_id == Product.id).all()

    if len(raw) == 0:
        return 'Не найден ланчбокс с указанным ID', 400

    box = Lunchbox.query.filter_by(id=id).first()
    if box.archived or not box.locked:
        return 'Не найден ланчбокс с указанным ID', 400

    return [x[1].as_json_short() for x in raw], 200
