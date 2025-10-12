#!/usr/bin/env python3
"""Fixtures for integration tests."""

org_payload = {
    "login": "testorg",
    "id": 1,
    "repos_url": "https://api.github.com/orgs/testorg/repos",
}

repos_payload = [
    {"id": 1, "name": "repo1", "license": {"key": "apache-2.0"}},
    {"id": 2, "name": "repo2", "license": {"key": "mit"}},
    {"id": 3, "name": "repo3", "license": {"key": "apache-2.0"}},
]

expected_repos = ["repo1", "repo2", "repo3"]

apache2_repos = ["repo1", "repo3"]
