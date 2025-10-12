# Unittests and Integration Tests

This project covers writing unit and integration tests in Python using `unittest`, `parameterized`, and `unittest.mock`.

## Tasks

### 0. Parameterize a unit test
- Implemented tests for `utils.access_nested_map`.
- Used `@parameterized.expand` to check multiple valid paths.
- Verified expected values are returned.

### 1. Parameterize a unit test (exceptions)
- Tested that `access_nested_map` raises `KeyError` for invalid paths.
- Used `assertRaises` and confirmed exception messages.

### 2. Mock HTTP calls
- Tested `utils.get_json` without making real HTTP requests.
- Used `unittest.mock.patch` to patch `requests.get`.
- Verified correct payload is returned and `requests.get` is called once per test.

### 3. Parameterize and patch (memoization)
- Tested the `utils.memoize` decorator.
- Verified that when accessing a memoized property twice:
  - The result is correct both times.
  - The underlying method is called only once (`assert_called_once`).

### 4. Memoization
   - Tested `utils.memoize` decorator.
   - Verified a method call is cached (called once, reused on subsequent calls).

### 5. Mocking a Property  

In this task, we wrote a unit test for the **`_public_repos_url`** property of the `GithubOrgClient` class.

#### What We Did
- Mocked the `org` property using **`patch.object`** with `new_callable=PropertyMock`.  
- Returned a fake payload containing a `repos_url`.  
- Verified that `_public_repos_url` correctly extracts the mocked value.  
- Ensured that the `org` property was called exactly once.  

---

````markdown
#### Example Test Case
```python
def test_public_repos_url(self):
    test_payload = {"repos_url": "https://api.github.com/orgs/testorg/repos"}
    with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
        mock_org.return_value = test_payload
        client = GithubOrgClient("testorg")
        self.assertEqual(client._public_repos_url, test_payload["repos_url"])
        mock_org.assert_called_once()
````

### 6. More Patching

#### Objective

Unit-test the `GithubOrgClient.public_repos` method by mocking both the API response and the `_public_repos_url` property.

##### What Was Done

* Implemented `test_public_repos` inside `test_client.py`.
* Patched:

  * `client.get_json` → mocked to return a fake repos payload.
  * `GithubOrgClient._public_repos_url` → mocked to return a fake API URL.
* Verified that:

  * The method `public_repos()` returns the expected list of repository names.
  * Both mocks (`_public_repos_url` and `get_json`) are called **exactly once**.

###### Example Test Payload

```python
test_payload = [
    {"name": "repo1"},
    {"name": "repo2"},
    {"name": "repo3"},
]
```
---
### 7. Parameterize `has_license`

#### Implemented `test_has_license` for `GithubOrgClient.has_license`
#### Used `@parameterized.expand` to test with multiple repo/license cases:
##### Repo with matching license: returns `True`.
##### Repowith different license: returns `False`.
#### Verified expected results with `assertEqual`

#### Example Test Cases
```python
@parameterized.expand([
    ({"license": {"key": "my_license"}}, "my_license", True),
    ({"license": {"key": "other_license"}}, "my_license", False),
])
def test_has_license(self, repo, license_key, expected):
    result = GithubOrgClient.has_license(repo, license_key)
    self.assertEqual(result, expected)

```

---

### `test_client.py`

Unit tests for `client.py`

1. **GithubOrgClient.org**

   * Tested `GithubOrgClient.org` returns correct payload.
   * Used `@patch("client.get_json")` to mock API calls.
   * Parametrized with `google` and `abc` organizations.
   * Verified `get_json` is called exactly once with the expected URL.

---

## Running Tests

Run tests individually:

```bash
python -m unittest 0x03-Unittests_and_integration_tests/test_utils.py -v
python -m unittest 0x03-Unittests_and_integration_tests/test_client.py -v
```

````

---
