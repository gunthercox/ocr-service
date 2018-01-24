from unittest import TestCase
from app import api
import json


class ApiTestCase(TestCase):

    def setUp(self):
        import os
        import base64

        self.client = api.app.test_client()

        test_directory = os.path.dirname(os.path.abspath(__file__))

        image_path = os.path.join(test_directory, 'image.png')

        with open(image_path, 'rb') as image_file:
            self.base64_image = base64.b64encode(image_file.read()).decode()

    def test_image_missing(self):
        """
        Test that the 'image' value is missing.
        """
        response = self.client.post(
            '/',
            content_type='application/json',
            data=json.dumps({
                'image': self.base64_image
            })
        )

        print(response.data)

        self.assertEqual('', response.data)
