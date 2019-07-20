from typing import List

from sqlalchemy.sql import expression

from py.db.endpoint import DatabaseEndpoint as de
from py.db.models.product import Product


class Lunchbox(de.db.Model):
    __tablename__ = 'lunchboxes'
    id = de.db.Column(de.db.Integer, primary_key=True)
    name = de.db.Column(de.db.String(80), nullable=False)
    price = de.db.Column(de.db.Integer, nullable=False)
    locked = de.db.Column(de.db.Boolean, nullable=False, default=expression.false())
    archived = de.db.Column(de.db.Boolean, nullable=False, default=expression.false())

    def as_json_full(self, products: List[Product]) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'products': [item.as_json() for item in products]
        }

    def as_json(self, products: List[int]) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'products': products
        }
