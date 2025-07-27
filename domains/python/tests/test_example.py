"""
Example test module demonstrating testing patterns and best practices.

This module shows how to structure tests and use fixtures effectively.
Remove this file once you have actual tests for your project.
"""

import pytest


def test_example_basic():
    """Test basic assertions and patterns."""
    # Arrange
    expected = "Hello, World!"
    
    # Act
    result = "Hello, World!"
    
    # Assert
    assert result == expected


def test_example_with_fixture(sample_data):
    """Test using a fixture from conftest.py."""
    # Test can access fixture data
    assert sample_data["test_string"] == "Hello, World!"
    assert sample_data["test_number"] == 42
    assert len(sample_data["test_list"]) == 5


def test_example_parametrized():
    """Test with parametrized inputs."""
    test_cases = [
        (1, 1, 2),
        (2, 3, 5),
        (0, 0, 0),
        (-1, 1, 0),
    ]
    
    for a, b, expected in test_cases:
        result = a + b
        assert result == expected


@pytest.mark.parametrize("input_val,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
    ("MiXeD", "MIXED"),
])
def test_string_upper(input_val, expected):
    """Test string uppercase conversion."""
    result = input_val.upper()
    assert result == expected


def test_file_operations(temp_file):
    """Test file operations using temporary file fixture."""
    # Read content
    content = temp_file.read_text()
    assert content == "Test content"
    
    # Write new content
    new_content = "Updated content"
    temp_file.write_text(new_content)
    
    # Verify update
    assert temp_file.read_text() == new_content


def test_exception_handling():
    """Test exception handling patterns."""
    with pytest.raises(ValueError, match="invalid literal"):
        int("not_a_number")
    
    with pytest.raises(ZeroDivisionError):
        1 / 0


@pytest.mark.slow
def test_slow_operation():
    """Example of marking slow tests."""
    # This test would take a long time
    # Use: pytest -m "not slow" to skip slow tests
    import time
    time.sleep(0.1)  # Simulate slow operation
    assert True


class TestExampleClass:
    """Example test class for grouping related tests."""
    
    def test_class_method_one(self):
        """Test method in a class."""
        assert True
    
    def test_class_method_two(self, sample_data):
        """Another test method using fixture."""
        assert isinstance(sample_data["test_dict"], dict)