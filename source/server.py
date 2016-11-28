import os
from aggregate_method import create_app


app = create_app(os.getenv("AGGREGATE_METHOD_CONFIGURATION"))
