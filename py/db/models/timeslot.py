from py.db.endpoint import DatabaseEndpoint as de


class Timeslot(de.db.Model):
    __tablename__ = 'timeslots'
    id = de.db.Column(de.db.Integer, primary_key=True)
    time_start = de.db.Column(de.db.Time, nullable=False)
    time_end = de.db.Column(de.db.Time, nullable=False)
    capacity = de.db.Column(de.db.Integer, nullable=False)

    def as_json(self):
        return {
            'id': self.id,
            'time_start': str(self.time_start),
            'time_end': str(self.time_end)
        }
