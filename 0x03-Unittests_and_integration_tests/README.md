# 0x03. Unittests and Integration Tests

This project covers how to write unit tests and integration tests in Python using the `unittest` framework. It includes:

- Writing unit tests with `unittest.TestCase`
- Using `parameterized.expand` to test functions with multiple inputs
- Mocking HTTP calls and functions using `unittest.mock`
- Understanding the difference between unit and integration testing
- Testing decorators like `@memoize`

## Files

- `utils.py`: Contains utility functions like `access_nested_map`, `get_json`, and `memoize`.
- `test_utils.py`: Contains unit tests for the utility functions.
- `client.py`: Used later in integration tests.
- `fixtures.py`: Contains test data for integration testing.

## How to Run Tests

To execute the test file:

```bash
python3 -m unittest test_utils.py
