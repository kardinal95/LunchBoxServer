from py.db.endpoint import DatabaseEndpoint as de


class LunchboxProduct(de.db.Model):
    __tablename__ = 'lunchbox_products'
    id = de.db.Column(de.db.Integer, primary_key=True)
    lunchbox_id = de.db.Column(de.db.Integer,
                               de.db.ForeignKey('lunchboxes.id'),
                               nullable=False)
    product_id = de.db.Column(de.db.Integer,
                              de.db.ForeignKey('products.id'),
                              nullable=True)
