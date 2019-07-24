from sqlalchemy.sql import expression

from py.db.endpoint import DatabaseEndpoint as de


class Product(de.db.Model):
    __tablename__ = 'products'
    id = de.db.Column(de.db.Integer, primary_key=True)
    name = de.db.Column(de.db.String(80), nullable=False)
    description = de.db.Column(de.db.String(230), nullable=True)
    locked = de.db.Column(de.db.Boolean, nullable=False, default=expression.false())
    archived = de.db.Column(de.db.Boolean, nullable=False, default=expression.false())

    def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'locked': self.locked,
            'archived': self.archived
        }

    def as_json_short(self):
        return {
            'name': self.name,
            'description': self.description,
        }
