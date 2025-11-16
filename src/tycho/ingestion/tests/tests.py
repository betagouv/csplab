"""Tests for ingestion app."""

from django.test import TestCase
from rest_framework.test import APIClient


class CorpsETLTestCase(TestCase):
    """Test case for Corps ETL endpoint."""

    def setUp(self):
        """Set up test client."""
        self.client = APIClient()

    def test_corps_etl_endpoint(self):
        """Test corps ETL endpoint exists."""
        response = self.client.post("/ingestion/etl/corps/")
        self.assertEqual(response.status_code, 200)
