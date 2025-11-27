"""Unit tests for CorpsCleaner."""

import json
import unittest
from datetime import datetime
from pathlib import Path

import polars as pl

from apps.ingestion.infrastructure.adapters.services.corps_cleaner import CorpsCleaner
from apps.ingestion.infrastructure.adapters.services.logger import LoggerService
from apps.ingestion.tests.unit.pelage_checks import (
    has_no_minarm_ministry,
    has_valid_decree_format,
)
from core.entities.document import Document, DocumentType


class TestUnitCorpsCleaner(unittest.TestCase):
    """Unit tests for CorpsCleaner."""

    @classmethod
    def setUpClass(cls):
        """Load fixtures once for all tests."""
        fixture_data = cls._load_fixture("corps_ingres_20251117.json")
        cls.raw_corps_documents = fixture_data

    @classmethod
    def _load_fixture(cls, filename):
        """Load fixture from the shared fixtures directory."""
        fixtures_path = Path(__file__).parent.parent / "fixtures" / filename
        with open(fixtures_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def setUp(self):
        """Set up test dependencies."""
        logger_service = LoggerService()
        self.corps_cleaner = CorpsCleaner(logger_service)

    def _create_test_documents(self, raw_data_list):
        """Helper to create test documents."""
        documents = []
        for i, raw_data in enumerate(raw_data_list):
            document = Document(
                id=i + 1,
                raw_data=raw_data,
                type=DocumentType.CORPS,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            documents.append(document)
        return documents

    def test_parse_corps_data(self):
        """Test parsing corps data and validate structure with pelage."""
        documents = self._create_test_documents(self.raw_corps_documents[:3])

        corps_data = []
        for document in documents:
            parsed_data = self.corps_cleaner._parse_corps_data(document.raw_data)
            if parsed_data:
                corps_data.append(parsed_data)

        self.assertGreater(len(corps_data), 0)

        df = pl.DataFrame(corps_data)

        expected_columns = ["id", "category", "ministry", "fp_type", "population"]
        for col in expected_columns:
            self.assertIn(col, df.columns)

    def test_apply_filters(self):
        """Test filtering logic with pelage validation."""
        documents = self._create_test_documents(self.raw_corps_documents[:3])

        corps_data = []
        for document in documents:
            parsed_data = self.corps_cleaner._parse_corps_data(document.raw_data)
            if parsed_data:
                corps_data.append(parsed_data)

        df = pl.DataFrame(corps_data)
        df_filtered = self.corps_cleaner._apply_filters(df)

        if len(df_filtered) > 0:
            df_filtered.pipe(has_no_minarm_ministry, "ministry")

    def test_process_laws(self):
        """Test law processing with pelage validation."""
        documents = self._create_test_documents(self.raw_corps_documents[:2])

        corps_data = []
        for document in documents:
            parsed_data = self.corps_cleaner._parse_corps_data(document.raw_data)
            if parsed_data:
                corps_data.append(parsed_data)

        df = pl.DataFrame(corps_data)
        df_filtered = self.corps_cleaner._apply_filters(df)

        if len(df_filtered) > 0:
            df_processed = self.corps_cleaner._process_laws(df_filtered)

            if len(df_processed) > 0:
                df_processed.pipe(has_valid_decree_format, "selected_law_id")

    def test_clean_full_pipeline(self):
        """Test complete cleaning pipeline."""
        documents = self._create_test_documents(self.raw_corps_documents[:2])

        corps_entities = self.corps_cleaner.clean(documents)

        self.assertIsInstance(corps_entities, list)
        for corps in corps_entities:
            self.assertIsNotNone(corps.id)
            self.assertIsNotNone(corps.label)
            self.assertIsNotNone(corps.category)
