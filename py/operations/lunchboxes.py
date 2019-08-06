from itertools import groupby
from typing import Tuple, List

from py.db.endpoint import DatabaseEndpoint as de
from py.db.models.lunchbox import Lunchbox
from py.db.models.lunchbox_product import LunchboxProduct
from py.db.models.product import Product
from py.exceptions import TargetNotExists, TargetLocked, TargetArchived, BaseLBSException
from py.lib import filter_locked_and_archived, get_missing_products
from py.models.lunchboxes import LunchboxEditModel


def get_lunchbox_simple(index: int) -> Lunchbox:
    lunchbox = Lunchbox.query.filter_by(id=index).first()
    if lunchbox is None:
        raise TargetNotExists(Lunchbox, [index])
    return lunchbox


def get_lunchboxes(locked: bool, archived: bool) -> dict:
    raw = de.db.session.query(Lunchbox,
                              LunchboxProduct).filter(Lunchbox.id == LunchboxProduct.lunchbox_id).all()

    targets = filter_locked_and_archived(Lunchbox.query, locked, archived).all()

    # Группируем в формате ланчбокс: список продуктов
    filtered = {key: [x[1].product_id for x in list(value)] for key, value in groupby(raw, lambda x: x[0])}

    return {x: filtered[x] for x in filtered if x in targets}


def get_lunchbox_with_id(index: int) -> Tuple:
    raw = de.db.session.query(Lunchbox,
                              LunchboxProduct).filter(Lunchbox.id == index,
                                                      Lunchbox.id == LunchboxProduct.lunchbox_id).all()

    if len(raw) == 0:
        raise TargetNotExists(Lunchbox, [index])

    # Группируем в формате ланчбокс: список продуктов
    filtered = {key: [x[1].product_id for x in list(value)] for key, value in groupby(raw, lambda x: x[0])}
    box = filtered.popitem()

    return box


def get_lunchbox_full_with_id(index: int) -> Tuple:
    raw = de.db.session.query(Lunchbox,
                              LunchboxProduct,
                              Product).filter(Lunchbox.id == index,
                                              Lunchbox.id == LunchboxProduct.lunchbox_id,
                                              LunchboxProduct.product_id == Product.id).all()

    if len(raw) == 0:
        raise TargetNotExists(Lunchbox, [index])

    # Группируем в формате ланчбокс: список продуктов
    filtered = {key: [x[2] for x in list(value)] for key, value in groupby(raw, lambda x: x[0])}
    box = filtered.popitem()

    return box


def get_lunchbox_products_with_id(index: int) -> List[Product]:
    raw = de.db.session.query(LunchboxProduct,
                              Product).filter(LunchboxProduct.lunchbox_id == index,
                                              LunchboxProduct.product_id == Product.id).all()

    if len(raw) == 0:
        raise TargetNotExists(Lunchbox, [index])

    return [x[1] for x in raw]


def edit_lunchbox_with_id(model: LunchboxEditModel) -> tuple:
    lunchbox = get_lunchbox_simple(index)

    if lunchbox.locked:
        raise TargetLocked(Lunchbox, model.index)
    if lunchbox.archived:
        raise TargetArchived(Lunchbox, model.index)

    missing_products = get_missing_products(model.products)
    if len(missing_products) != 0:
        raise TargetNotExists(Product, missing_products)

    lunchbox.name = model.name
    lunchbox.price = model.price
    de.db.session.add(lunchbox)

    target_products = Product.query.filter(Product.id.in_(model.products)).all()
    for item in target_products:
        if item.archived:
            raise TargetArchived(Product, item.id)

    box_products = LunchboxProduct.query.filter_by(lunchbox_id=model.index).all()
    box_products_ids = [x.product_id for x in box_products]
    for item in box_products:
        if item.product_id not in model.products:
            de.db.session.delete(item)

    for item in model.products:
        if item not in box_products_ids:
            box_product = LunchboxProduct(lunchbox_id=model.index, product_id=item)
            de.db.session.add(box_product)

    de.db.session.commit()
    return get_lunchbox_with_id(model.index)


def archive_lunchbox_with_id(index: int) -> tuple:
    full = get_lunchbox_full_with_id(index)
    lunchbox = full[0]
    products = full[1]

    if lunchbox.archived:
        raise TargetArchived(Lunchbox, lunchbox.id)

    if not lunchbox.locked:
        for item in products:
            if not item.locked:
                item.locked = True
                de.db.session.add(item)

    lunchbox.archived = True
    lunchbox.locked = True

    de.db.session.add(lunchbox)
    de.db.session.commit()

    return get_lunchbox_with_id(index)


def lock_lunchbox_with_id(index: int) -> tuple:
    full = get_lunchbox_full_with_id(index)
    lunchbox = full[0]
    products = full[1]

    if lunchbox.archived:
        raise TargetArchived(Lunchbox, index)
    if lunchbox.locked:
        raise TargetLocked(Lunchbox, index)

    for item in products:
        if not item.locked:
            item.locked = True
            de.db.session.add(item)

    lunchbox.locked = True

    de.db.session.add(lunchbox)
    de.db.session.commit()

    return get_lunchbox_with_id(index)


def stock_lunchbox_with_id(index: int, stock: bool) -> tuple:
    lunchbox = get_lunchbox_simple(index)

    if lunchbox.archived:
        raise TargetArchived(Lunchbox, index)
    if not lunchbox.locked:
        raise BaseLBSException('Ланчбокс не заблокирован!', 400)

    lunchbox.stock = stock

    de.db.session.add(lunchbox)
    de.db.session.commit()

    return get_lunchbox_with_id(index)


def remove_lunchbox_with_id(index: int) -> None:
    lunchbox = get_lunchbox_simple(index)

    if lunchbox.archived:
        raise TargetArchived(Lunchbox, index)
    if lunchbox.locked:
        raise TargetLocked(Lunchbox, index)

    de.db.session.delete(lunchbox)
    de.db.session.commit()


def add_lunchbox(model: LunchboxEditModel) -> tuple:
    missing_products = get_missing_products(model.products)
    if len(missing_products) != 0:
        raise TargetNotExists(Product, missing_products)

    target_products = Product.query.filter(Product.id.in_(model.products)).all()
    for item in target_products:
        if item.archived:
            raise TargetArchived(Product, item.id)

    lunchbox = Lunchbox(
        name=model.name,
        price=model.price,
        stock=False
    )
    de.db.session.add(lunchbox)
    de.db.session.flush()

    for item in model.products:
        box_product = LunchboxProduct(lunchbox_id=lunchbox.id, product_id=item)
        de.db.session.add(box_product)

    de.db.session.commit()

    return get_lunchbox_with_id(lunchbox.id)


def get_pub_lunchbox_with_id(index: int) -> tuple:
    box = get_lunchbox_with_id(index)
    if box[0].archived or not box[0].locked:
        raise TargetNotExists(Lunchbox, [index])

    return box


def get_pub_lunchbox_full_with_id(index: int) -> tuple:
    box = get_lunchbox_full_with_id(index)

    if box[0].archived or not box[0].locked:
        raise TargetNotExists(Lunchbox, [index])

    return box


def get_pub_lunchbox_products_with_id(index: int) -> List[Product]:
    products = get_lunchbox_products_with_id(index)

    box = get_lunchbox_simple(index)
    if box.archived or not box.locked:
        raise TargetNotExists(Lunchbox, [index])

    return products
