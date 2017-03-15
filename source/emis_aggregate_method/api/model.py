from sqlalchemy_utils import UUIDType
from .. import db


class AggregateMethodModel(db.Model):
    id = db.Column(UUIDType(), primary_key=True)
    name = db.Column(db.Unicode(15))
    posted_at = db.Column(db.DateTime)
