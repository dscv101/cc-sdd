"""Pytest configuration and fixtures."""

import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory for testing.

    Yields:
        Path to temporary directory
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_project_with_kiro(temp_project_dir):
    """Create a temporary project with .kiro directory structure.

    Args:
        temp_project_dir: Temporary project directory

    Yields:
        Path to temporary directory with .kiro structure
    """
    kiro_dir = temp_project_dir / ".kiro"
    kiro_dir.mkdir()
    (kiro_dir / "steering").mkdir()
    (kiro_dir / "specs").mkdir()
    yield temp_project_dir
