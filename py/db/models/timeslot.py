from py.db.endpoint import DatabaseEndpoint as de


class Timeslot(de.db.Model):
    __tablename__ = 'timeslots'
    id = de.db.Column(de.db.Integer, primary_key=True)
    time_start = de.db.Column(de.db.Time, nullable=False)
    time_end = de.db.Column(de.db.Time, nullable=False)
    capacity = de.db.Column(de.db.Integer, nullable=False)