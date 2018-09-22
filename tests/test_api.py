from unittest import TestCase
from app import api


class ApiTestCase(TestCase):

    def setUp(self):
        import os

        self.client = api.app.test_client()

        test_directory = os.path.dirname(os.path.abspath(__file__))

        self.image_path = os.path.join(test_directory, 'image.png')

    def test_data_missing(self):
        """
        Test that an error is returned if the request body is empty.
        """
        response = self.client.post('/')

        self.assertEqual(response.status_code, 400)

        self.assertIn('error', response.json)
        self.assertIn('image', response.json['error'])
        self.assertIn(
            'This field is required.',
            response.json['error']['image']
        )

    def test_image_missing(self):
        """
        Test that the 'image' value is missing.
        """
        response = self.client.post('/', data={})

        self.assertEqual(response.status_code, 400)

        self.assertIn('error', response.json)
        self.assertIn('image', response.json['error'])
        self.assertIn(
            'This field is required.',
            response.json['error']['image']
        )

    def test_post_image(self):
        """
        Test posting an image.
        """
        response = self.client.post('/', data={
            'image': open(self.image_path, 'rb')
        })

        self.assertTrue(response.status_code, 200)

        self.assertIn('text', response.json)

        self.assertIn(
            'woke up this morning',
            response.json['text']
        )
        self.assertIn(
            'received an invoice from my Google Fi',
            response.json['text']
        )
        self.assertIn(
            'and headed off to work, listening to',
            response.json['text']
        )
