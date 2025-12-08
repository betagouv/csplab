"""Utility for loading shared test fixtures."""

import json
from pathlib import Path


def load_fixture(filename: str):
    """Load fixture from the shared fixtures directory."""
    fixtures_path = Path(__file__).parent / filename
    with open(fixtures_path, "r", encoding="utf-8") as f:
        return json.load(f)
