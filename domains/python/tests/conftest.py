"""
Pytest configuration and shared fixtures.

This file contains pytest configuration and fixtures that are
available to all test modules in the project.
"""

import pytest
from pathlib import Path


@pytest.fixture
def sample_data():
    """Provide sample data for testing."""
    return {
        "test_string": "Hello, World!",
        "test_number": 42,
        "test_list": [1, 2, 3, 4, 5],
        "test_dict": {"key": "value", "nested": {"inner": "data"}}
    }


@pytest.fixture
def temp_file(tmp_path):
    """Create a temporary file for testing."""
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("Test content")
    return file_path


@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for testing."""
    test_dir = tmp_path / "test_directory"
    test_dir.mkdir()
    return test_dir


@pytest.fixture(scope="session")
def project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent


# Add more fixtures as needed for your specific project