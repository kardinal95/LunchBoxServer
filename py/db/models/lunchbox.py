from py.db.endpoint import DatabaseEndpoint as de


class Lunchbox(de.db.Model):
    __tablename__ = 'lunchboxes'
    id = de.db.Column(de.db.Integer, primary_key=True)
    name = de.db.Column(de.db.String(80), nullable=False)
    price = de.db.Column(de.db.Integer, nullable=False)

    def as_json(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'price': str(self.price)
        }
