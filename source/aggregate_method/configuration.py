import os


class Configuration:

    SECRET_KEY = os.environ.get("EMIS_AGGREGATE_METHOD_SECRET_KEY") or \
        "yabbadabbadoo!"
    JSON_AS_ASCII = False

    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    @staticmethod
    def init_app(
            app):
        pass


class DevelopmentConfiguration(Configuration):

    DEBUG = True
    DEBUG_TOOLBAR_ENABLED = True
    FLASK_DEBUG_DISABLE_STRICT = True


    @staticmethod
    def init_app(
            app):
        Configuration.init_app(app)

        from flask_debug import Debug
        Debug(app)


class TestingConfiguration(Configuration):

    SERVER_NAME = os.environ.get("EMIS_AGGREGATE_METHOD_SERVER_NAME") or \
        "localhost"
    TESTING = True


class ProductionConfiguration(Configuration):

    pass


configuration = {
    "development": DevelopmentConfiguration,
    "testing": TestingConfiguration,
    "production": ProductionConfiguration
}
