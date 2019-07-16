from py.db.models.lunchbox import Lunchbox
from py.db.models.lunchbox_product import LunchboxProduct
from py.db.models.product import Product


def get_lunchboxes():
    lunchboxes = Lunchbox.query.all()
    return [x.as_json() for x in lunchboxes]


def get_lunchbox_full(id):
    lunchbox = Lunchbox.query.filter_by(id=id).first()
    if lunchbox is None:
        return 'No lunchbox with this id', 400

    products_ids = [x.product_id for x in LunchboxProduct.query.filter_by(lunchbox_id=id).all()]
    products = Product.query.filter(Product.id.in_(products_ids)).all()

    return {
        'id': str(lunchbox.id),
        'name': lunchbox.name,
        'price': str(lunchbox.price),
        'products': [
            x.as_json_cut() for x in products
        ]
    }, 200
