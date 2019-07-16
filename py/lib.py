from py.db.models.role import Role
from py.db.models.user_role import UserRole


def has_required_role(user_id, role):
    current_roles = [x.id for x in UserRole.query.filter_by(user_id=user_id).all()]
    possible_roles = [x.id for x in Role.query.all() if x.name == 'superrole' or x.name == role]

    return len(set(current_roles) & set(possible_roles)) != 0
