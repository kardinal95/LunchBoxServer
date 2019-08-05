from py.db.models.lunchbox import Lunchbox
from py.exceptions import TargetNotExists


def get_lunchbox(lunchbox_id):
    lunchbox = Lunchbox.query.filter_by(id=lunchbox_id).first()
    if lunchbox is None:
        raise TargetNotExists(Lunchbox, lunchbox_id)
    return lunchbox

