from py.db.models.product import Product


class ProductModel:
    def __init__(self, product: Product):
        self.id = product.id
        self.name = product.name
        self.description = product.description
        self.locked = product.locked
        self.archived = product.archived

    def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'locked': self.locked,
            'archived': self.archived
        }


class ProductEditModel:
    def __init__(self, params):
        self.name = params['name']
        self.description = params['description'] if 'description' in params.keys() else None
