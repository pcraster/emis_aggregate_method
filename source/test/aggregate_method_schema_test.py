import datetime
import unittest
import uuid
from emis_aggregate_method import create_app
from emis_aggregate_method.api.schema import *


class AggregateMethodSchemaTestCase(unittest.TestCase):


    def setUp(self):
        self.app = create_app("test")
        self.app.config["TESTING"] = True

        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client()
        self.schema = AggregateMethodSchema()


    def tearDown(self):
        self.schema = None

        self.app_context.pop()


    def test_empty1(self):
        client_data = {
            }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
                "_schema": ["Input data must have a aggregate_method key"]
            })


    def test_empty2(self):
        client_data = {
                "aggregate_method": {}
            }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
                "name": ["Missing data for required field."]
            })


    def test_empty_name(self):
        client_data = {
                "aggregate_method": {
                    "name": ""
                }
            }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
                "name": ["Data not provided"]
            })


    def test_empty3(self):

        client_data = {
                "aggregate_method": {
                    "name": "max"
                }
            }
        data, errors = self.schema.load(client_data)

        self.assertFalse(errors)

        self.assertTrue(hasattr(data, "id"))
        self.assertTrue(isinstance(data.id, uuid.UUID))

        self.assertTrue(hasattr(data, "posted_at"))
        self.assertTrue(isinstance(data.posted_at, datetime.datetime))

        self.assertTrue(hasattr(data, "name"))
        self.assertEqual(data.name, "max")

        data.id = uuid.uuid4()
        data, errors = self.schema.dump(data)

        self.assertFalse(errors)
        self.assertTrue("aggregate_method" in data)

        method = data["aggregate_method"]

        self.assertTrue("id" not in method)
        self.assertTrue("posted_at" not in method)

        self.assertTrue("name" in method)
        self.assertEqual(method["name"], "max")

        self.assertTrue("_links" in method)

        links = method["_links"]

        self.assertTrue("self" in links)
        self.assertTrue("collection" in links)


if __name__ == "__main__":
    unittest.main()
