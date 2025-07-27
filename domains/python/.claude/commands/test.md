Run comprehensive Python tests with coverage reporting.

## Test Execution

Run the full test suite:
1. Execute all tests with pytest
2. Generate coverage report (aim for 90%+)
3. Show detailed output for failures
4. Include doctests if present

## Test Discovery

Automatically discover and run:
- All test files matching `test_*.py` pattern
- All `*_test.py` files
- All test methods starting with `test_`
- Doctests in source files and markdown

## Coverage Analysis

Generate coverage reports:
- Terminal summary with missing lines
- HTML report for detailed analysis
- XML report for CI integration
- Fail if coverage below threshold

## Test Types

Execute different test categories:
- Unit tests (fast, isolated)
- Integration tests (database, external APIs)
- Property-based tests (hypothesis)
- Performance tests if present

## Options

Support common testing flags:
- `-v` for verbose output
- `-x` to stop on first failure
- `-k EXPRESSION` to run specific tests
- `--lf` to run last failed tests only
- `--tb=short` for concise tracebacks

Always ensure virtual environment is active before running tests.
Report test results clearly with actionable feedback for failures.