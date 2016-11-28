import os.path
import unittest
import uuid
from flask import current_app, json
from aggregate_method import create_app, db
from aggregate_method.api.schema import *


class AggregateMethodTestCase(unittest.TestCase):


    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def post_aggregate_methods(self):

        payloads = [
                {
                    "name": "maximum",
                },
                {
                    "name": "minimum",
                },
                {
                    "name": "mean",
                },
            ]

        for payload in payloads:
            response = self.client.post("/aggregate_methods",
                data=json.dumps({"aggregate_method": payload}),
                content_type="application/json")
            data = response.data.decode("utf8")

            self.assertEqual(response.status_code, 201, "{}: {}".format(
                response.status_code, data))

    # def do_test_get_aggregate_methods_by_user(self,
    #         user_id,
    #         nr_results_required):

    #     self.post_aggregate_methods()

    #     response = self.client.get("/aggregate_methods/{}".format(user_id))
    #     data = response.data.decode("utf8")

    #     self.assertEqual(response.status_code, 200, "{}: {}".format(
    #         response.status_code, data))

    #     data = json.loads(data)

    #     self.assertTrue("aggregate_methods" in data)

    #     methods = data["aggregate_methods"]

    #     self.assertEqual(len(methods), nr_results_required)


    # def test_get_aggregate_methods_by_user1(self):
    #     self.do_test_get_aggregate_methods_by_user(self.user1, 2)


    # def test_get_aggregate_methods_by_user2(self):
    #     self.do_test_get_aggregate_methods_by_user(self.user2, 1)


    # def test_get_aggregate_methods_by_user3(self):
    #     self.do_test_get_aggregate_methods_by_user(self.user3, 0)


    def test_get_aggregate_methods1(self):
        # No methods posted.
        response = self.client.get("/aggregate_methods")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("aggregate_methods" in data)
        self.assertEqual(data["aggregate_methods"], [])


    def test_get_aggregate_methods2(self):
        # Some methods posted.
        self.post_aggregate_methods()

        response = self.client.get("/aggregate_methods")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("aggregate_methods" in data)

        methods = data["aggregate_methods"]

        self.assertEqual(len(methods), 3)


    def test_get_aggregate_method(self):
        self.post_aggregate_methods()

        response = self.client.get("/aggregate_methods")
        data = response.data.decode("utf8")
        data = json.loads(data)
        methods = data["aggregate_methods"]
        method = methods[0]
        uri = method["_links"]["self"]
        response = self.client.get(uri)

        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("aggregate_method" in data)

        self.assertEqual(data["aggregate_method"], method)

        self.assertTrue("id" not in method)
        self.assertTrue("posted_at" not in method)

        self.assertTrue("name" in method)
        self.assertEqual(method["name"], "maximum")

        self.assertTrue("_links" in method)

        links = method["_links"]

        self.assertTrue("self" in links)
        self.assertEqual(links["self"], uri)

        self.assertTrue("collection" in links)


    def test_get_unexisting_aggregate_method(self):
        self.post_aggregate_methods()

        response = self.client.get("/aggregate_methods")
        data = response.data.decode("utf8")
        data = json.loads(data)
        methods = data["aggregate_methods"]
        method = methods[0]
        uri = method["_links"]["self"]
        # Invalidate uri
        uri = os.path.join(os.path.split(uri)[0], str(uuid.uuid4()))
        response = self.client.get(uri)

        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 400, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


    def test_post_aggregate_method(self):
        payload = {
                "name": "maximum"
            }
        response = self.client.post("/aggregate_methods",
            data=json.dumps({"aggregate_method": payload}),
            content_type="application/json")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 201, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("aggregate_method" in data)

        method = data["aggregate_method"]

        self.assertTrue("id" not in method)
        self.assertTrue("posted_at" not in method)

        self.assertTrue("name" in method)
        self.assertEqual(method["name"], "maximum")

        self.assertTrue("_links" in method)

        links = method["_links"]

        self.assertTrue("self" in links)
        self.assertTrue("collection" in links)

        response = self.client.get("/aggregate_methods")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("aggregate_methods" in data)

        methods = data["aggregate_methods"]

        self.assertEqual(len(methods), 1)


    def test_post_bad_request(self):
        response = self.client.post("/aggregate_methods")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 400, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


    def test_post_unprocessable_entity(self):
        payload = ""
        response = self.client.post("/aggregate_methods",
            data=json.dumps({"aggregate_method": payload}),
            content_type="application/json")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 422, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


if __name__ == "__main__":
    unittest.main()
