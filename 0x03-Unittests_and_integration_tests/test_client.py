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
        result = client.org  # access memoized property

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

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos returns expected list of repo names"""
        # Example payload returned by get_json
        repo_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": {"key": "mit"}},
        ]
        mock_get_json.return_value = repo_payload

        client = GithubOrgClient("test")

        # Patch the _public_repos_url property to return any URL
        with patch.object(
            type(client), "_public_repos_url", new_callable=patch.PropertyMock
        ) as mock_repos_url:
            mock_repos_url.return_value = "https://api.github.com/orgs/test/repos"
            result = client.public_repos()  # No license filter

            # Check that _public_repos_url was accessed once
            mock_repos_url.assert_called_once()

        # Check that get_json was called once (via repos_payload property)
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/test/repos")

        # Assert the result is list of repo names
        expected_repos = ["repo1", "repo2", "repo3"]
        self.assertEqual(result, expected_repos)
