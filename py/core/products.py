from py.db.models.product import Product
from py.lib import has_required_role

from py.db.endpoint import DatabaseEndpoint as de


def get_products(user):
    if not has_required_role(user, 'product manager'):
        return 'Not allowed for current user', 403

    products = Product.query.all()
    return [item.as_json() for item in products]


def add_products(user, body):
    if not has_required_role(user, 'product manager'):
        return 'Not allowed for current user', 403

    for item in body['products']:
        product = Product(
            name=item['name'],
            description='' if 'description' not in item.keys() else item['description']
        )
        de.db.session.add(product)
    de.db.session.commit()


def delete_products(user, body):
    if not has_required_role(user, 'product manager'):
        return 'Not allowed for current user', 403

    targets = Product.query.filter(Product.id.in_(body['ids'])).all()

    for item in targets:
        de.db.session.delete(item)
    de.db.session.commit()

    return 'Success', 200