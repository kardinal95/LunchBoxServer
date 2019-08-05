from typing import List

from py.db.endpoint import DatabaseEndpoint as de
from py.db.models.lunchbox import Lunchbox
from py.db.models.lunchbox_product import LunchboxProduct
from py.db.models.product import Product
from py.exceptions import TargetNotExists, TargetLocked, TargetArchived, TargetInRelation, BaseLBSException
from py.lib import filter_locked_and_archived
from py.models.products import ProductEditModel
from py.operations.relations import get_lunchboxes_with_products


def _get_product_from_db(index: int, archived: bool = False, locked: bool = False) -> Product:
    product = Product.query.filter_by(id=index).first()

    if product is None:
        raise TargetNotExists(Product, index)

    if not archived and product.archived:
        raise TargetArchived()
    if not locked and product.locked:
        raise TargetLocked()

    return product


def get_products(archived: bool = None, locked: bool = None) -> List[Product]:
    products = filter_locked_and_archived(Product.query, locked, archived).all()

    return products


def get_product_with_id(index: int) -> Product:
    product = Product.query.filter_by(id=index).first()

    if product is None:
        raise TargetNotExists(Product, index)

    return product


def edit_product_with_id(index: int, prod: ProductEditModel) -> Product:
    product = _get_product_from_db(index, False, False)

    product.name = prod.name
    product.description = prod.description

    de.db.session.add(product)
    de.db.session.commit()

    return product


def remove_product_with_id(index: int) -> None:
    product = _get_product_from_db(index, False, False)

    boxes = LunchboxProduct.query.filter_by(product_id=index).all()

    if len(boxes) > 0:
        raise TargetInRelation(Lunchbox, set(str(x.lunchbox_id) for x in boxes))

    de.db.session.delete(product)
    de.db.session.commit()


def archive_product_with_id(index: int) -> Product:
    product = _get_product_from_db(index, False, True)

    boxes = get_lunchboxes_with_products([index])
    filtered = [x for x in boxes if not x.archived]

    if len(filtered) > 0:
        raise BaseLBSException("Продукт находится в составе неархивированных ланчбоксов с ID {}. "
                               .format(', '.join(set(str(x.id) for x in filtered))), 400)

    product.archived = True
    product.locked = True

    de.db.session.add(product)
    de.db.session.commit()

    return product


def lock_product_with_id(index: int) -> Product:
    product = _get_product_from_db(index, False, False)

    product.locked = True

    de.db.session.add(product)
    de.db.session.commit()

    return product


def add_product(product: ProductEditModel) -> Product:
    target = Product(
        name=product.name,
        description=product.description,
        locked=False,
        archived=False
    )

    de.db.session.add(target)
    de.db.session.commit()

    return target
