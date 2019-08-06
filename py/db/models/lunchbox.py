from typing import List

from sqlalchemy.sql import expression

from py.db.endpoint import DatabaseEndpoint as de
from py.db.models.product import Product


class Lunchbox(de.db.Model):
    __tablename__ = 'lunchboxes'
    __title__ = 'ланчбокс'
    id = de.db.Column(de.db.Integer, primary_key=True)
    name = de.db.Column(de.db.String(80), nullable=False)
    price = de.db.Column(de.db.Integer, nullable=False)
    locked = de.db.Column(de.db.Boolean, nullable=False, default=expression.false())
    archived = de.db.Column(de.db.Boolean, nullable=False, default=expression.false())
    stock = de.db.Column(de.db.Boolean, nullable=False, default=expression.true())