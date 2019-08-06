from py.db.endpoint import DatabaseEndpoint as de


class Role(de.db.Model):
    __tablename__ = 'roles'
    __title__ = 'роль'
    id = de.db.Column(de.db.Integer, primary_key=True)
    name = de.db.Column(de.db.String(80), nullable=False)
