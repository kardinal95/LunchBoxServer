from sqlalchemy.sql import expression

from py.db.endpoint import DatabaseEndpoint as de


class Product(de.db.Model):
    __tablename__ = 'products'
    __title__ = 'продукт'
    id = de.db.Column(de.db.Integer, primary_key=True)
    name = de.db.Column(de.db.String(80), nullable=False)
    description = de.db.Column(de.db.String(230), nullable=True)
    locked = de.db.Column(de.db.Boolean, nullable=False, default=expression.false())
    archived = de.db.Column(de.db.Boolean, nullable=False, default=expression.false())
