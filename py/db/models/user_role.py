from py.db.endpoint import DatabaseEndpoint as de


class UserRole(de.db.Model):
    __tablename__ = 'user_roles'
    id = de.db.Column(de.db.Integer, primary_key=True)
    user_id = de.db.Column(de.db.Integer,
                           de.db.ForeignKey('users.id'),
                           nullable=False)
    role_id = de.db.Column(de.db.Integer,
                           de.db.ForeignKey('roles.id'),
                           nullable=False)
