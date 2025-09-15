#!/usr/bin/env python3
"""Unit tests for client module:
- GithubOrgClient
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value"""
        expected_payload = {"org": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org  # no parentheses because @memoize caches the dict

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct URL from mocked org"""
        mock_org_payload = {
            "repos_url": "https://api.github.com/orgs/test/repos"}

        client = GithubOrgClient("test")
        with patch.object(
            type(client), "org", new_callable=patch.PropertyMock
        ) as mock_org:
            mock_org.return_value = mock_org_payload
            result = client._public_repos_url

        self.assertEqual(result, mock_org_payload["repos_url"])
