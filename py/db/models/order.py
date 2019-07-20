import datetime

from py.db.endpoint import DatabaseEndpoint as de


class Order(de.db.Model):
    __tablename__ = 'orders'
    id = de.db.Column(de.db.Integer, primary_key=True)
    client_id = de.db.Column(de.db.Integer,
                             de.db.ForeignKey('roles.id'),
                             nullable=False,
                             onupdate='CASCADE',
                             ondelete='CASCADE')
    status_id = de.db.Column(de.db.Integer,
                             de.db.ForeignKey('order_statuses.id'),
                             nullable=False,
                             onupdate='CASCADE',
                             ondelete='SET NULL')
    created_at = de.db.Column(de.db.DateTime, default=datetime.datetime.utcnow)
    timeslot_id = de.db.Column(de.db.Integer,
                               de.db.ForeignKey('timeslots.id'),
                               nullable=False,
                               onupdate='CASCADE',
                               ondelete='SET NULL')
