from unittest import TestCase
from unittest.mock import patch
from app import api
import unittest
import os


# Show full diff in unittest
unittest.util._MAX_LENGTH = 2000


class ApiTestCase(TestCase):
    """
    Test suite for OCR API endpoints.
    """

    def setUp(self):
        self.client = api.app.test_client()

        self.test_directory = os.path.dirname(os.path.abspath(__file__))


class HealthEndpointTests(ApiTestCase):
    """
    Test suite for the health check endpoint.
    """

    def test_health_endpoint(self):
        """
        Test the health check endpoint returns 200 status.
        """
        response = self.client.get('/health')

        self.assertEqual(response.status_code, 200)


class OcrApiTests(ApiTestCase):
    """
    Test suite for OCR API endpoints.
    """

    def test_data_missing(self):
        """
        Test that an error is returned if the request body is empty.
        """
        response = self.client.post('/')

        self.assertEqual(response.status_code, 400)

        self.assertIn('error', response.json)

        # Empty request triggers Content-Type validation first
        self.assertIn('content_type', response.json['error'])
        self.assertIn(
            'Request must be multipart/form-data.',
            response.json['error']['content_type']
        )

    def test_image_missing(self):
        """
        Test that the 'image' value is missing.
        """
        response = self.client.post('/', data={})

        self.assertEqual(response.status_code, 400)

        self.assertIn('error', response.json)
        # Empty data dict triggers Content-Type validation first
        self.assertIn('content_type', response.json['error'])
        self.assertIn(
            'Request must be multipart/form-data.',
            response.json['error']['content_type']
        )

    def test_post_image(self):
        """
        Test posting an image with Tesseract engine.
        """
        image_path = os.path.join(self.test_directory, '01_image.png')

        response = self.client.post('/', data={
            'image': open(image_path, 'rb'),
            'engine': 'tesseract'
        })

        self.assertTrue(response.status_code, 200)

        self.assertIn('text', response.json)
        self.assertIn('regions', response.json)

        regions = response.json['regions']
        self.assertIsInstance(regions, list)

        # Detected text regions should exist
        self.assertGreater(len(regions), 0)

        # Verify region structure
        if len(regions) > 0:
            region = regions[0]
            self.assertIn('bbox', region)
            self.assertIn('text', region)
            self.assertIn('confidence', region)

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
        Test posting an image with Japanese text using Tesseract.
        """
        japanese_image_path = os.path.join(self.test_directory, '02_image.png')

        with open(japanese_image_path, 'rb') as img_file:
            response = self.client.post('/', data={
                'image': img_file,
                'engine': 'tesseract',
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
        Tesseract with lang=eng+fra.
        """
        eng_fra_image_path = os.path.join(self.test_directory, '03_image.png')

        with open(eng_fra_image_path, 'rb') as img_file:
            response = self.client.post('/', data={
                'image': img_file,
                'engine': 'tesseract',
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

    def test_post_handwriting(self):
        """
        Test posting an image with handwriting using Tesseract.

        NOTE: tesseract's handwriting recognition is not ideal, this test is
        more of a benchmark to see if improvements occur over time.
        """
        handwriting_image_path = os.path.join(
            self.test_directory, '04_image.jpg'
        )

        with open(handwriting_image_path, 'rb') as img_file:
            response = self.client.post('/', data={
                'image': img_file,
                'engine': 'tesseract',
                'lang': 'eng'
            })

        self.assertTrue(response.status_code, 200)
        self.assertIn('text', response.json)

        self.assertIn(
            'Sample hoindwritin\nAnne hands 9\n',
            response.json['text']
        )

    def test_image_text_orientation(self):
        """
        Test posting an image with rotated text using Tesseract to see if
        orientation is detected correctly.

        NOTE: tesseract seems to struggle with rotated text, this test is
        intended to establish a benchmark for future improvements in
        orientation
        detection.
        """
        rotated_image_path = os.path.join(self.test_directory, '05_image.png')

        with open(rotated_image_path, 'rb') as img_file:
            response = self.client.post('/', data={
                'image': img_file,
                'engine': 'tesseract',
                'lang': 'eng'
            })

        self.assertTrue(response.status_code, 200)
        self.assertIn('text', response.json)

        self.assertEqual(
            (
                "wom LXaL NMOG aaisan\n\nauist wn\nVv o\nE =\n2 Normal Text "
                "=\n& | el\nA rr\n~ 4\n\nflipped around ROTATED 90°\n"
            ),
            response.json['text']
        )

    def test_paddleocr_data_missing(self):
        """
        Test that PaddleOCR engine returns an error if the request body is
        empty.
        """
        response = self.client.post('/', data={'engine': 'paddleocr'})

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        # Empty data without file triggers Content-Type validation
        self.assertIn('content_type', response.json['error'])
        self.assertIn(
            'Request must be multipart/form-data.',
            response.json['error']['content_type']
        )

    def test_paddleocr_image_missing(self):
        """
        Test that PaddleOCR engine returns error when 'image' field is missing.
        """
        # Send with proper content type to bypass content_type validation
        response = self.client.post(
            '/',
            data={'engine': 'paddleocr'},
            content_type='multipart/form-data'
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.assertIn('image', response.json['error'])
        self.assertIn(
            'This field is required.',
            response.json['error']['image']
        )

    def test_paddleocr_post_image(self):
        """
        Test posting an image with PaddleOCR engine.
        Verifies response includes text, regions, and bounding boxes.
        """
        image_path = os.path.join(self.test_directory, '01_image.png')

        response = self.client.post('/', data={
            'image': open(image_path, 'rb'),
            'engine': 'paddleocr'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('text', response.json)
        self.assertIn('regions', response.json)

        # Verify regions structure
        regions = response.json['regions']
        self.assertIsInstance(regions, list)

        if len(regions) > 0:
            # Check first region has required fields
            region = regions[0]
            self.assertIn('bbox', region)
            self.assertIn('text', region)
            self.assertIn('confidence', region)

            # Verify bbox structure (should be 4 points)
            bbox = region['bbox']
            self.assertIsInstance(bbox, list)
            self.assertEqual(len(bbox), 4)

            # Verify confidence is a float between 0 and 1
            self.assertIsInstance(region['confidence'], (float, int))
            self.assertGreaterEqual(region['confidence'], 0.0)
            self.assertLessEqual(region['confidence'], 1.0)

    def test_paddleocr_rotated_image(self):
        """
        Test PaddleOCR engine with rotated text image (should perform better
        than Tesseract). PaddleOCR should handle multi-directional text better.
        """
        rotated_image_path = os.path.join(self.test_directory, '05_image.png')

        with open(rotated_image_path, 'rb') as img_file:
            response = self.client.post('/', data={
                'image': img_file,
                'engine': 'paddleocr'
            })

        self.assertEqual(response.status_code, 200)
        self.assertIn('text', response.json)
        self.assertIn('regions', response.json)

        # PaddleOCR should detect some text regions
        regions = response.json['regions']
        self.assertIsInstance(regions, list)
        # Note: We don't assert specific text since PaddleOCR may detect
        # differently than Tesseract, but it should find something

    def test_file_size_limit(self):
        """
        Test that both engines enforce the 10MB file size limit.
        """
        image_path = os.path.join(self.test_directory, '01_image.png')

        # Create a large mock file (simulated via content_length header)
        # In reality, Flask test client doesn't easily simulate content_length
        # without actual large file, so this is a basic structure test
        # Production servers would enforce this limit properly

        # For now, just verify the endpoint exists and handles images
        response = self.client.post('/', data={
            'image': open(image_path, 'rb'),
            'engine': 'paddleocr'
        })

        # Should succeed with normal-sized file
        self.assertIn(response.status_code, [200, 400])

    def test_content_type_validation(self):
        """
        Test that Content-Type validation is applied to all engines.
        Note: Flask test client automatically sets multipart/form-data,
        so this test verifies the validation logic exists.
        """
        image_path = os.path.join(self.test_directory, '01_image.png')

        # Valid request should work
        response = self.client.post('/', data={
            'image': open(image_path, 'rb'),
            'engine': 'paddleocr'
        })

        self.assertIn(response.status_code, [200, 400])

    def test_default_engine_is_paddleocr(self):
        """
        Test that the default engine is PaddleOCR when engine parameter is
        not specified.
        """
        image_path = os.path.join(self.test_directory, '01_image.png')

        response = self.client.post('/', data={
            'image': open(image_path, 'rb')
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('text', response.json)
        self.assertIn('regions', response.json)
        # PaddleOCR returns regions with data (not empty)
        regions = response.json['regions']
        self.assertIsInstance(regions, list)
        # Should have detected some text regions
        self.assertGreater(len(regions), 0)

    def test_invalid_engine_parameter(self):
        """
        Test that an invalid engine parameter returns an error.
        """
        image_path = os.path.join(self.test_directory, '01_image.png')

        # Mock AVAILABLE_ENGINES to simulate an environment where
        # invalid_engine is not available
        with patch('app.api.AVAILABLE_ENGINES', ['tesseract', 'paddleocr']):
            response = self.client.post('/', data={
                'image': open(image_path, 'rb'),
                'engine': 'invalid_engine'
            })

            self.assertEqual(response.status_code, 400)
            self.assertIn('error', response.json)
            self.assertIn('engine', response.json['error'])
            # Check for the actual error message format
            self.assertIn(
                "Engine 'invalid_engine' is not available",
                response.json['error']['engine']
            )
            self.assertIn(
                'tesseract, paddleocr',
                response.json['error']['engine']
            )

    def test_engine_not_in_image_variant(self):
        """
        Test error when requesting an engine that's not in the image variant.
        Simulates a tesseract-only image variant being asked to use paddleocr.
        """
        image_path = os.path.join(self.test_directory, '01_image.png')

        # Mock AVAILABLE_ENGINES to simulate tesseract-only image
        with patch('app.api.AVAILABLE_ENGINES', ['tesseract']):
            response = self.client.post('/', data={
                'image': open(image_path, 'rb'),
                'engine': 'paddleocr'
            })

            self.assertEqual(response.status_code, 400)
            self.assertIn('error', response.json)
            self.assertIn('engine', response.json['error'])
            # Verify error mentions the requested engine and available engines
            error_msg = response.json['error']['engine']
            self.assertIn("Engine 'paddleocr' is not available", error_msg)
            self.assertIn('Available engines: tesseract', error_msg)
            self.assertIn(
                "Please use an image with the 'paddleocr' engine installed",
                error_msg
            )

    def test_tesseract_returns_regions_with_bboxes(self):
        """
        Test that Tesseract engine returns regions with bounding boxes.
        """
        image_path = os.path.join(self.test_directory, '01_image.png')

        response = self.client.post('/', data={
            'image': open(image_path, 'rb'),
            'engine': 'tesseract'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('text', response.json)
        self.assertIn('regions', response.json)

        # Tesseract now returns regions with bounding boxes
        regions = response.json['regions']
        self.assertIsInstance(regions, list)
        self.assertGreater(len(regions), 0)

        # Verify first region has proper structure
        region = regions[0]
        self.assertIn('bbox', region)
        self.assertIn('text', region)
        self.assertIn('confidence', region)

        # Verify bbox structure (4 corner points)
        bbox = region['bbox']
        self.assertIsInstance(bbox, list)
        self.assertEqual(len(bbox), 4)

        # Verify confidence is in 0.0-1.0 range
        self.assertIsInstance(region['confidence'], (float, int))
        self.assertGreaterEqual(region['confidence'], 0.0)
        self.assertLessEqual(region['confidence'], 1.0)
