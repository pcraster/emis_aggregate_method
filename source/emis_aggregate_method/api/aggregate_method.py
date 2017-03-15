from . import api_restful
from .resource import *


# All aggregate methods.
# - Get all methods
# - Post method
api_restful.add_resource(AggregateMethodsResource,
    "/aggregate_methods",
    endpoint="aggregate_methods")

# Aggregate method by method-id.
# - Get method by method-id
api_restful.add_resource(AggregateMethodResource,
    "/aggregate_methods/<uuid:method_id>",
    endpoint="aggregate_method")
