from py.db.endpoint import DatabaseEndpoint as de


class OrderStatus(de.db.Model):
    __tablename__ = 'order_statuses'
    id = de.db.Column(de.db.Integer, primary_key=True)
    name = de.db.Column(de.db.String(80), nullable=False)