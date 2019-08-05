from py.db.models.lunchbox import Lunchbox
from py.db.models.lunchbox_product import LunchboxProduct


def get_lunchboxes_with_products(ids):
    lps = LunchboxProduct.query.filter(LunchboxProduct.product_id.in_(ids)).all()
    boxes = set(x.lunchbox_id for x in lps)

    return Lunchbox.query.filter(Lunchbox.id.in_(boxes)).all()
