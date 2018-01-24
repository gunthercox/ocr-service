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

    def test_data_missing(self):
        """
        Test that an error is returned if the request body is empty.
        """
        response = self.client.post(
            '/',
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

    def test_image_missing(self):
        """
        Test that the 'image' value is missing.
        """
        response = self.client.post(
            '/',
            data=json.dumps({})
        )

        self.assertEqual(response.status_code, 400)

        response_json = json.loads(response.data)

        self.assertIn('error', response_json)
        self.assertIn('image', response_json['error'])
        self.assertIn(
            'This field is required.',
            response_json['error']['image']
        )

    def test_post_image(self):
        """
        Test that the 'image' value is missing.
        """
        response = self.client.post(
            '/',
            data=json.dumps({
                'image': self.base64_image
            })
        )

        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.data)

        self.assertIn('text', response_json)

        self.assertIn(
            'woke up this morning',
            response_json['text']
        )
        self.assertIn(
            'received an invoice from my Google Fi',
            response_json['text']
        )
        self.assertIn(
            'and headed off to work, listening to',
            response_json['text']
        )
