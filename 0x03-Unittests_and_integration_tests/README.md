# ALX Backend Python - 0x03: Unittests and Integration Tests

This repository contains exercises and projects related to backend development in Python, with a focus on unit testing and integration testing.

## Project: Test `utils.access_nested_map`

### Overview

In this task, we write our first unit test for the function `access_nested_map` located in `utils.py`. This function is used to access nested dictionaries using a tuple path.

### Objective

- Understand the purpose of `utils.access_nested_map`.
- Write unit tests to validate that it behaves as expected for different input cases.

### Instructions

1. Create a `TestAccessNestedMap` class inheriting from `unittest.TestCase`.
2. Implement the method `test_access_nested_map` to test `access_nested_map`.
3. Use `@parameterized.expand` to test the following cases:

   | Nested Map        | Path         | Expected Result |
   | ----------------- | ------------ | --------------- |
   | `{"a": 1}`        | `("a",)`     | `1`             |
   | `{"a": {"b": 2}}` | `("a",)`     | `{"b": 2}`      |
   | `{"a": {"b": 2}}` | `("a", "b")` | `2`             |

4. Each test should use `assertEqual` to verify the expected result.
5. Keep the body of the test method concise (≤ 2 lines).

### File Structure
