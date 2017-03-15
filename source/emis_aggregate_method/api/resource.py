from werkzeug.exceptions import *
from flask_restful import Resource
from flask import request
from .. import db
from .model import AggregateMethodModel
from .schema import AggregateMethodSchema


aggregate_method_schema = AggregateMethodSchema()


class AggregateMethodResource(Resource):

    def get(self,
            method_id):

        method = AggregateMethodModel.query.get(method_id)

        if method is None:
            raise BadRequest("Aggregate method could not be found")


        data, errors = aggregate_method_schema.dump(method)

        if errors:
            raise InternalServerError(errors)


        return data


class AggregateMethodsResource(Resource):

    def get(self):

        methods = AggregateMethodModel.query.all()
        data, errors = aggregate_method_schema.dump(methods, many=True)

        if errors:
            raise InternalServerError(errors)

        assert isinstance(data, dict), data


        return data


    def post(self):

        json_data = request.get_json()

        if json_data is None:
            raise BadRequest("No input data provided")


        # Validate and deserialize input.
        method, errors = aggregate_method_schema.load(json_data)

        if errors:
            raise UnprocessableEntity(errors)


        # Write method to database.
        db.session.add(method)
        db.session.commit()


        # From record in database to dict representing an aggregate method.
        data, errors = aggregate_method_schema.dump(
            AggregateMethodModel.query.get(method.id))
        assert not errors, errors
        assert isinstance(data, dict), data


        return data, 201
