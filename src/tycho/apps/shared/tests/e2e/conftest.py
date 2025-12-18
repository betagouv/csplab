"""Pytest configuration for E2E tests."""

import os

import pytest


def pytest_configure(config):
    """Configure pytest for E2E tests."""
    # Set Django settings module for pytest
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tycho.settings")


@pytest.fixture(scope="session", autouse=True)
def enable_mocks():
    """Enable mock services for E2E tests by default."""
    os.environ.setdefault("TYCHO_USE_MOCK_ALBERT", "true")
    os.environ.setdefault("TYCHO_USE_MOCK_OPENROUTER", "true")
    yield
