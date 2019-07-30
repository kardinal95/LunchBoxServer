from py.db.models.lunchbox import Lunchbox


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
