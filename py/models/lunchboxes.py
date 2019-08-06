from py.db.models.lunchbox import Lunchbox
from py.models.products import ProductModel


class ClientLunchboxModel:
    def __init__(self, lunchbox: Lunchbox):
        self.id = lunchbox.id
        self.name = lunchbox.name
        self.stock = lunchbox.stock
        self.price = lunchbox.price

    def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'stock': self.stock,
            'price': self.price
        }


class LunchboxWithProductIdsModel:
    def __init__(self, lunchbox, product_ids):
        self.id = lunchbox.id
        self.name = lunchbox.name
        self.price = lunchbox.price
        self.archived = lunchbox.archived
        self.locked = lunchbox.locked
        self.stock = lunchbox.stock
        self.products = product_ids

    def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'archived': self.archived,
            'locked': self.locked,
            'stock': self.stock,
            'products': self.products
        }


class LunchboxWithProductsModel:
    def __init__(self, lunchbox, products):
        self.id = lunchbox.id
        self.name = lunchbox.name
        self.price = lunchbox.price
        self.archived = lunchbox.archived
        self.locked = lunchbox.locked
        self.stock = lunchbox.stock
        self.products = [ProductModel(x) for x in products]

    def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'archived': self.archived,
            'locked': self.locked,
            'stock': self.stock,
            'products': [x.as_json() for x in self.products]
        }


class LunchboxEditModel:
    def __init__(self, index, params):
        self.index = index
        self.name = params['name']
        self.price = params['price']
        self.products = params['products']


class ClientLunchboxWithProductIdsModel:
    def __init__(self, lunchbox, product_ids):
        self.id = lunchbox.id
        self.name = lunchbox.name
        self.price = lunchbox.price
        self.stock = lunchbox.stock
        self.products = product_ids

    def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'stock': self.stock,
            'products': self.products
        }


class ClientLunchboxWithProductsModel:
    def __init__(self, lunchbox, products):
        self.id = lunchbox.id
        self.name = lunchbox.name
        self.price = lunchbox.price
        self.stock = lunchbox.stock
        self.products = [ProductModel(x) for x in products]

    def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'stock': self.stock,
            'products': [x.as_json() for x in self.products]
        }
