from py.db.models.lunchbox import Lunchbox
from py.db.models.lunchbox_product import LunchboxProduct
from py.db.models.product import Product
from py.lib import has_required_role, filter_locked_and_archived

from py.db.endpoint import DatabaseEndpoint as de


def get_products(user, archived, locked):
    if not has_required_role(user, 'product manager'):
        return 'Недопустимо для текущего пользователя', 403

    products = filter_locked_and_archived(Product.query, locked, archived).all()

    return [item.as_json() for item in products], 200


def get_product_with_id(user, id):
    if not has_required_role(user, 'product manager'):
        return 'Недопустимо для текущего пользователя', 403

    product = Product.query.filter_by(id=id).first()

    if product is None:
        return "Продукт не найден", 404

    return product.as_json(), 200


def edit_product_with_id(user, id, body):
    if not has_required_role(user, 'product manager'):
        return 'Недопустимо для текущего пользователя', 403

    product = Product.query.filter_by(id=id).first()

    if product is None:
        return "Продукт не найден", 404

    if product.locked or product.archived:
        return 'Продукт заблокирован для изменений!', 400

    product.name = body['name']
    product.description = body['description'] if 'description' in body.keys() else None

    de.db.session.add(product)
    de.db.session.commit()

    return product.as_json(), 200


def remove_product_with_id(user, id):
    if not has_required_role(user, 'product manager'):
        return 'Недопустимо для текущего пользователя', 403

    product = Product.query.filter_by(id=id).first()

    if product is None:
        return "Продукт не найден", 404

    if product.locked or product.archived:
        return 'Продукт заблокирован для удаления!', 400

    box = LunchboxProduct.query.filter_by(product_id=id).all()
    if len(box) > 0:
        return "Продукт находится в составе ланчбоксов с ID {}. " \
               "Сначала удалите продукт из ланчбокса!"\
                   .format(', '.join(set(str(x.lunchbox_id) for x in box))), 400

    de.db.session.delete(product)
    de.db.session.commit()

    return 'Успешно удалено', 200


def archive_product_with_id(user, id):
    if not has_required_role(user, 'product manager'):
        return 'Недопустимо для текущего пользователя', 403

    product = Product.query.filter_by(id=id).first()

    if product is None:
        return "Продукт не найден", 404

    if product.archived:
        return 'Продукт уже архивирован!', 400

    rels = [x.lunchbox_id for x in LunchboxProduct.query.filter_by(product_id=id).all()]
    box = Lunchbox.query.filter(Lunchbox.id.in_(rels)).filter_by(archived=False).all()
    if len(box) > 0:
        return "Продукт находится в составе неархивированных ланчбоксов с ID {}. "\
                   .format(', '.join(set(str(x.id) for x in box))), 400

    product.archived = True
    product.locked = True

    de.db.session.add(product)
    de.db.session.commit()

    return 'Успешно архивировано', 200


def lock_product_with_id(user, id):
    if not has_required_role(user, 'product manager'):
        return 'Недопустимо для текущего пользователя', 403

    product = Product.query.filter_by(id=id).first()

    if product is None:
        return "Продукт не найден", 404

    if product.locked:
        return 'Продукт уже архивирован!', 400

    product.locked = True

    de.db.session.add(product)
    de.db.session.commit()

    return 'Успешно заблокировано', 200


def add_product(user, body):
    if not has_required_role(user, 'product manager'):
        return 'Недопустимо для текущего пользователя', 403

    product = Product(
        name=body['name'],
        description=body['description'] if 'description' in body.keys() else None,
        locked=False,
        archived=False
    )

    de.db.session.add(product)
    de.db.session.commit()

    return 'Успешно добавлено', 200


def batch_add_products(user, body):
    if not has_required_role(user, 'product manager'):
        return 'Недопустимо для текущего пользователя', 403

    for item in body:
        product = Product(
            name=item['name'],
            description=item['description'] if 'description' in item.keys() else None,
            locked=False,
            archived=False
        )
        de.db.session.add(product)

    de.db.session.commit()

    return 'Успешно добавлено', 200


def batch_edit_products(user, body):
    if not has_required_role(user, 'product manager'):
        return 'Недопустимо для текущего пользователя', 403

    for item in body:
        product = Product.query.filter_by(id=item['id']).first()
        if product is None:
            return 'Продукт с id {} не найден, операция остановлена'.format(item['id']), 400

        if product.locked or product.archived:
            return 'Продукт c id {} заблокирован для изменения, операция остановлена', 400

        product = Product(
            name=item['name'],
            description=item['description'] if 'description' in item.keys() else None
        )
        de.db.session.add(product)

    de.db.session.commit()

    return 'Успешно изменено', 200


def batch_remove_products(user, body):
    if not has_required_role(user, 'product manager'):
        return 'Недопустимо для текущего пользователя', 403

    targets = Product.query.filter(Product.id.in_(body)).all()

    box = LunchboxProduct.query.filter(LunchboxProduct.product_id.in_(body)).all()
    if len(box) > 0:
        return "Некоторые продукты находятся в составе ланчбоксов с ID {}. " \
               "Сначала удалите продукты из ланчбоксов!"\
                   .format(', '.join(set(str(x.lunchbox_id) for x in box))), 400

    for item in targets:
        if item.locked or item.archived:
            return 'Продукт c id {} заблокирован для удаления, операция остановлена', 400

        de.db.session.delete(item)
    de.db.session.commit()

    return 'Продукты успешно удалены', 200
