from py.db.endpoint import DatabaseEndpoint as de


class OrderItem(de.db.Model):
    __tablename__ = 'order_items'
    id = de.db.Column(de.db.Integer, primary_key=True)
    order_id = de.db.Column(de.db.Integer,
                            de.db.ForeignKey('orders.id', onupdate='CASCADE', ondelete='CASCADE'),
                            nullable=False)
    lunchbox_id = de.db.Column(de.db.Integer,
                               de.db.ForeignKey('lunchboxes.id', onupdate='CASCADE', ondelete='CASCADE'),
                               nullable=True)
    quantity = de.db.Column(de.db.Integer)
