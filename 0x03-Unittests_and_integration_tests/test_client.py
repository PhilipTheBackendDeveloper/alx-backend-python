#!/usr/bin/env python3
"""
Unit and integration tests for the `client.py` module.
"""
import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from typing import Dict


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit test suite for the `GithubOrgClient` class.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json: Mock) -> None:
        """Tests that `GithubOrgClient.org` returns the correct value."""
        test_client = GithubOrgClient(org_name)
        test_client.org()
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self) -> None:
        """Tests the `_public_repos_url` property."""
        known_payload = {"repos_url": "http://example.com/repos"}
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = known_payload
            test_client = GithubOrgClient("test_org")
            result = test_client._public_repos_url
            self.assertEqual(result, "http://example.com/repos")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: Mock) -> None:
        """Tests the `public_repos` method with a mocked payload."""
        test_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = test_payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "http://example.com/repos"
            test_client = GithubOrgClient("test_org")
            self.assertEqual(test_client.public_repos(), ["repo1", "repo2"])
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://example.com/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self,
                         repo: Dict,
                         license_key: str,
                         expected: bool) -> None:
        """Tests the `has_license` static method."""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test suite for the `GithubOrgClient` class.
    This class mocks external HTTP calls using fixtures.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """Set up the class by patching `requests.get` with a side effect."""
        
        def side_effect(url):
            """
            Defines the side effect for the mock. It returns different
            payloads based on the URL that is requested.
            """
            mock_response = Mock()
            # The org name is hardcoded to 'google' in the fixture
            org_url = "https://api.github.com/orgs/google"
            
            if url == org_url:
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_response.json.return_value = cls.repos_payload
            else:
                # If any other URL is called, the test should fail
                mock_response.status_code = 404
            return mock_response

        cls.get_patcher = patch('requests.get', side_effect=side_effect)
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down the class by stopping the patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """
        Integration test for the `public_repos` method without a license.
        This method is part of Task 9.
        """
        # The org name must match what the setUpClass side_effect expects
        test_client = GithubOrgClient("google")
        repos = test_client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """
        Integration test for the `public_repos` method with a license filter.
        This method is part of Task 9.
        """
        test_client = GithubOrgClient("google")
        repos = test_client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)