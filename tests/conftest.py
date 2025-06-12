"""pytest configuration for async tests using anyio."""

import pytest


@pytest.fixture
def anyio_backend():
    """Return the backend to use for async tests."""
    return 'asyncio'
