from itertools import groupby

from py.db.models.lunchbox import Lunchbox
from py.db.models.lunchbox_product import LunchboxProduct
from py.db.models.product import Product

from py.db.endpoint import DatabaseEndpoint as de
from py.lib import get_missing_products


def get_lunchboxes():
    raw = de.db.session.query(Lunchbox,
                              LunchboxProduct).filter(Lunchbox.id == LunchboxProduct.lunchbox_id).all()

    # Группируем в формате ланчбокс: список продуктов
    filtered = {key: [x[1].product_id for x in list(value)] for key, value in groupby(raw, lambda x: x[0])}

    return [x.as_json(filtered[x]) for x in filtered.keys()], 200


def get_lunchbox_with_id(id):
    raw = de.db.session.query(Lunchbox,
                              LunchboxProduct).filter(Lunchbox.id == id,
                                                      Lunchbox.id == LunchboxProduct.lunchbox_id).all()

    if len(raw) == 0:
        return 'Не найден ланчбокс с указанным ID', 400

    # Группируем в формате ланчбокс: список продуктов
    filtered = {key: [x[1].product_id for x in list(value)] for key, value in groupby(raw, lambda x: x[0])}
    box = filtered.popitem()

    return box[0].as_json(box[1]), 200


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

    return box[0].as_json_full(box[1]), 200


def get_lunchbox_products_with_id(id):
    raw = de.db.session.query(LunchboxProduct,
                              Product).filter(LunchboxProduct.lunchbox_id == id,
                                              LunchboxProduct.product_id == Product.id).all()

    if len(raw) == 0:
        return 'Не найден ланчбокс с указанным ID', 400

    return [x[1].as_json() for x in raw], 200


def edit_lunchbox_with_id(id, body):
    lunchbox = Lunchbox.query.filter_by(id=id).first()
    if lunchbox is None:
        return 'Не найден ланчбокс с указанным ID', 404

    missing_products = get_missing_products(body['products'])
    if len(missing_products) != 0:
        return 'Не найдены продукты с ID: {}'.format(', '.join(missing_products)), 404

    lunchbox.name = body['name']
    lunchbox.price = body['price']
    de.db.session.add(lunchbox)

    box_products = LunchboxProduct.query.filter_by(lunchbox_id=id).all()
    box_products_ids = [x.product_id for x in box_products]
    for item in box_products:
        if item.product_id not in body['products']:
            de.db.session.delete(item)

    for item in body['products']:
        if item not in box_products_ids:
            box_product = LunchboxProduct(lunchbox_id=id, product_id=item)
            de.db.session.add(box_product)

    de.db.session.commit()
    return 'Успех', 200


def remove_lunchbox_with_id(id):
    lunchbox = Lunchbox.query.filter_by(id=id).first()
    if lunchbox is None:
        return 'Не найден ланчбокс с указанным ID', 404

    # Удаление цепочек продуктов через каскадное удаление!

    de.db.session.delete(lunchbox)
    de.db.session.commit()

    return 'Успех', 200


def add_lunchbox(body):
    missing_products = get_missing_products(body['products'])
    if len(missing_products) != 0:
        return 'Не найдены продукты с ID: {}'.format(', '.join(missing_products)), 404

    lunchbox = Lunchbox(
        name = body['name'],
        price=body['price']
    )
    de.db.session.add(lunchbox)
    de.db.session.flush()

    for item in body['products']:
        box_product = LunchboxProduct(lunchbox_id=lunchbox.id, product_id=item)
        de.db.session.add(box_product)

    de.db.session.commit()
    return 'Успех', 200