from itertools import groupby

from py.db.models.lunchbox import Lunchbox
from py.db.models.lunchbox_product import LunchboxProduct
from py.db.models.product import Product

from py.db.endpoint import DatabaseEndpoint as de
from py.lib import get_missing_products, has_required_role, filter_locked_and_archived


def get_lunchboxes(user, locked, archived):
    if not has_required_role(user, 'lunchbox manager'):
        return 'Недопустимо для текущего пользователя', 403

    raw = de.db.session.query(Lunchbox,
                              LunchboxProduct).filter(Lunchbox.id == LunchboxProduct.lunchbox_id).all()

    targets = filter_locked_and_archived(Lunchbox.query, locked, archived).all()

    # Группируем в формате ланчбокс: список продуктов
    filtered = {key: [x[1].product_id for x in list(value)] for key, value in groupby(raw, lambda x: x[0])}

    return [x.as_json(filtered[x]) for x in filtered.keys() if x in targets], 200


def get_lunchbox_with_id(id, user):
    if not has_required_role(user, 'lunchbox manager'):
        return 'Недопустимо для текущего пользователя', 403

    raw = de.db.session.query(Lunchbox,
                              LunchboxProduct).filter(Lunchbox.id == id,
                                                      Lunchbox.id == LunchboxProduct.lunchbox_id).all()

    if len(raw) == 0:
        return 'Не найден ланчбокс с указанным ID', 400

    # Группируем в формате ланчбокс: список продуктов
    filtered = {key: [x[1].product_id for x in list(value)] for key, value in groupby(raw, lambda x: x[0])}
    box = filtered.popitem()

    return box[0].as_json(box[1]), 200


def get_lunchbox_full_with_id(id, user):
    if not has_required_role(user, 'lunchbox manager'):
        return 'Недопустимо для текущего пользователя', 403

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


def get_lunchbox_products_with_id(id, user):
    if not has_required_role(user, 'lunchbox manager'):
        return 'Недопустимо для текущего пользователя', 403

    raw = de.db.session.query(LunchboxProduct,
                              Product).filter(LunchboxProduct.lunchbox_id == id,
                                              LunchboxProduct.product_id == Product.id).all()

    if len(raw) == 0:
        return 'Не найден ланчбокс с указанным ID', 400

    return [x[1].as_json() for x in raw], 200


def edit_lunchbox_with_id(id, body, user):
    if not has_required_role(user, 'lunchbox manager'):
        return 'Недопустимо для текущего пользователя', 403

    lunchbox = Lunchbox.query.filter_by(id=id).first()
    if lunchbox is None:
        return 'Не найден ланчбокс с указанным ID', 404

    if lunchbox.locked or lunchbox.archived:
        return 'Ланчбокс заблокирован для изменений!', 400

    missing_products = get_missing_products(body['products'])
    if len(missing_products) != 0:
        return 'Не найдены продукты с ID: {}'.format(', '.join(missing_products)), 404

    lunchbox.name = body['name']
    lunchbox.price = body['price']
    de.db.session.add(lunchbox)

    target_products = Product.query.filter(Product.id.in_(body['products'])).all()
    for item in target_products:
        if item.archived:
            return 'Невозможно добавить архивный продукт {}, операция остановлена'.format(item.id), 400

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


def remove_lunchbox_with_id(id, user):
    if not has_required_role(user, 'lunchbox manager'):
        return 'Недопустимо для текущего пользователя', 403

    lunchbox = Lunchbox.query.filter_by(id=id).first()
    if lunchbox is None:
        return 'Не найден ланчбокс с указанным ID', 404

    if lunchbox.locked or lunchbox.archived:
        return 'Ланчбокс заблокирован!', 400

    de.db.session.delete(lunchbox)
    de.db.session.commit()

    return 'Успех', 200


def archive_lunchbox_with_id(id, user):
    if not has_required_role(user, 'lunchbox manager'):
        return 'Недопустимо для текущего пользователя', 403

    lunchbox = Lunchbox.query.filter_by(id=id).first()
    if lunchbox is None:
        return 'Не найден ланчбокс с указанным ID', 404

    if lunchbox.archived:
        return 'Ланчбокс уже архивирован!', 400

    if not lunchbox.locked:
        products_ids = [x.product_id for x in LunchboxProduct.query.filter_by(lunchbox_id=id).all()]
        products = Product.query.filter(Product.id.in_(products_ids)).all()
        for item in products:
            if not item.locked:
                item.locked = True
                de.db.session.add(item)

    lunchbox.archived = True
    lunchbox.locked = True

    de.db.session.add(lunchbox)
    de.db.session.commit()

    return 'Успех', 200


def lock_lunchbox_with_id(id, user):
    if not has_required_role(user, 'lunchbox manager'):
        return 'Недопустимо для текущего пользователя', 403

    lunchbox = Lunchbox.query.filter_by(id=id).first()
    if lunchbox is None:
        return 'Не найден ланчбокс с указанным ID', 404

    if lunchbox.archived:
        return 'Ланчбокс архивирован!', 400

    if lunchbox.locked:
        return 'Ланчбокс уже заблокирован!', 400

    products_ids = [x.product_id for x in LunchboxProduct.query.filter_by(lunchbox_id=id).all()]
    products = Product.query.filter(Product.id.in_(products_ids)).all()
    for item in products:
        if not item.locked:
            item.locked = True
            de.db.session.add(item)

    lunchbox.locked = True

    de.db.session.add(lunchbox)
    de.db.session.commit()

    return 'Успех', 200


def stock_lunchbox_with_id(id, stock, user):
    if not has_required_role(user, 'lunchbox manager'):
        return 'Недопустимо для текущего пользователя', 403

    lunchbox = Lunchbox.query.filter_by(id=id).first()
    if lunchbox is None:
        return 'Не найден ланчбокс с указанным ID', 404

    if lunchbox.archived:
        return 'Ланчбокс архивирован!', 400

    if not lunchbox.locked:
        return 'Ланчбокс не заблокирован!', 400

    lunchbox.stock = stock

    de.db.session.add(lunchbox)
    de.db.session.commit()

    return 'Успех', 200


def add_lunchbox(body, user):
    if not has_required_role(user, 'lunchbox manager'):
        return 'Недопустимо для текущего пользователя', 403

    missing_products = get_missing_products(body['products'])
    if len(missing_products) != 0:
        return 'Не найдены продукты с ID: {}'.format(', '.join(missing_products)), 404

    target_products = Product.query.filter(Product.id.in_(body['products'])).all()
    for item in target_products:
        if item.archived:
            return 'Невозможно добавить архивный продукт {}, операция остановлена'.format(item.id), 400

    lunchbox = Lunchbox(
        name=body['name'],
        price=body['price']
    )
    de.db.session.add(lunchbox)
    de.db.session.flush()

    for item in body['products']:
        box_product = LunchboxProduct(lunchbox_id=lunchbox.id, product_id=item)
        de.db.session.add(box_product)

    de.db.session.commit()
    return 'Успех', 200
