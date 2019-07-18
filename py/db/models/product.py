from py.db.endpoint import DatabaseEndpoint as de


class Product(de.db.Model):
    __tablename__ = 'products'
    id = de.db.Column(de.db.Integer, primary_key=True)
    name = de.db.Column(de.db.String(80), nullable=False)
    description = de.db.Column(de.db.String(230), nullable=True)

    def as_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

    def as_json_cut(self):
        return {
            "name": self.name,
            "description": self.description
        }