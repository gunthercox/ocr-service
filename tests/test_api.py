from unittest import TestCase
from app import api
import os


class ApiTestCase(TestCase):
    """
    Test suite for OCR API endpoints.
    """

    def setUp(self):
        self.client = api.app.test_client()

        test_directory = os.path.dirname(os.path.abspath(__file__))

        self.image_path = os.path.join(test_directory, '01_image.png')

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

    def test_post_image_japanese_text(self):
        """
        Test posting an image with Japanese text.
        """
        japanese_image_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '02_image.png'
        )

        with open(japanese_image_path, 'rb') as img_file:
            response = self.client.post('/', data={
                'image': img_file,
                'lang': 'jpn'
            })

        self.assertTrue(response.status_code, 200)
        self.assertIn('text', response.json)
        self.assertEqual(
            (
                'これはOCRソフトウ\n\nェエアのテストテキス\nトです\n\nKore wa '
                'oshiarusofuto uea no\n\ntesuto tekisutodesu\n'
            ),
            response.json['text']
        )

    def test_post_image_english_french_text(self):
        """
        Test posting an image with both English and French text using
        lang=eng+fra.
        """
        eng_fra_image_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '03_image.png'
        )

        with open(eng_fra_image_path, 'rb') as img_file:
            response = self.client.post('/', data={
                'image': img_file,
                'lang': 'eng+fra'
            })

        self.assertTrue(response.status_code, 200)
        self.assertIn('text', response.json)

        self.assertIn(
            'The weather is beautiful today.',
            response.json['text']
        )
        self.assertIn(
            "Le temps est magnifique aujourd'hui.",
            response.json['text']
        )
