import os
from aggregate_method import create_app


app = create_app(os.getenv("EMIS_AGGREGATE_METHOD_CONFIGURATION"))
