import datetime
import uuid
from marshmallow import fields, post_dump, post_load, pre_load, ValidationError
from .. import ma
from .model import AggregateMethodModel


def must_not_be_blank(
        data):
    if not data:
        raise ValidationError("Data not provided")


class AggregateMethodSchema(ma.Schema):

    class Meta:
        # Fields to include in the serialized result.
        fields = ("name", "_links")


    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True, validate=must_not_be_blank)
    posted_at = fields.DateTime(dump_only=True,
        missing=datetime.datetime.utcnow().isoformat())
    _links = ma.Hyperlinks({
            "self": ma.URLFor("api.aggregate_method", method_id="<id>"),
            "collection": ma.URLFor("api.aggregate_methods")
        })


    def key(self,
            many):
        return "aggregate_methods" if many else "aggregate_method"


    @pre_load(
        pass_many=True)
    def unwrap(self,
            data,
            many):
        key = self.key(many)

        if key not in data:
            raise ValidationError("Input data must have a {} key".format(key))

        return data[key]


    @post_dump(
        pass_many=True)
    def wrap(self,
            data, many):
        key = self.key(many)

        return {
            key: data
        }


    @post_load
    def make_object(self,
            data):
        return AggregateMethodModel(
            id=uuid.uuid4(),
            name=data["name"],
            posted_at=datetime.datetime.utcnow()
        )
