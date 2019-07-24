from py.db.models.product import Product
from py.db.models.role import Role
from py.db.models.user_role import UserRole


def has_required_role(user_id, role):
    current_roles = [x.id for x in UserRole.query.filter_by(user_id=user_id).all()]
    possible_roles = [x.id for x in Role.query.all() if x.name == 'superrole' or x.name == role]

    return len(set(current_roles) & set(possible_roles)) != 0


def get_missing_products(products):
    target_products = Product.query.filter(Product.id.in_(products)).all()
    missing_products = set(products) - (set(products) & set([x.id for x in target_products]))

    return missing_products


def filter_locked_and_archived(query, locked, archived):
    result = query
    if archived is not None:
        result = result.filter_by(archived=archived)
    if locked is not None:
        result = result.filter_by(locked=locked)
    return result