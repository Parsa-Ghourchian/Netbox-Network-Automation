#!/usr/bin/env python3
"""
NetBox REST API client for the automation lab.

This client is intentionally lightweight and dependency-minimal.
It supports:
- NetBox v2 API tokens using Bearer authentication.
- Legacy v1 tokens using Token authentication.
- Paginated list endpoints.
- Useful error output for troubleshooting.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import requests


class NetBoxClient:
    """Small NetBox REST API client."""

    def __init__(self, base_url: str, token: str, timeout: int = 30) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_base = f"{self.base_url}/api"
        self.token = token
        self.timeout = timeout

        self.headers = {
            "Authorization": self._build_auth_header(token),
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    @staticmethod
    def _build_auth_header(token: str) -> str:
        """Return the correct NetBox Authorization header value."""
        if token.startswith("nbt_"):
            return f"Bearer {token}"

        return f"Token {token}"

    def _url(self, endpoint: str) -> str:
        """Build a NetBox API URL from an endpoint."""
        endpoint = endpoint.strip("/")

        if not endpoint:
            return f"{self.api_base}/"

        return f"{self.api_base}/{endpoint}/"

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Send a GET request and return JSON data."""
        url = self._url(endpoint)
        response = requests.get(
            url,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )

        if response.status_code >= 400:
            print(f"ERROR: GET {response.url}")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            response.raise_for_status()

        return response.json()

    def list_all(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Return all objects from a paginated NetBox list endpoint."""
        query = dict(params or {})
        query.setdefault("limit", 100)

        url = self._url(endpoint)
        results: List[Dict[str, Any]] = []

        while url:
            response = requests.get(
                url,
                headers=self.headers,
                params=query if "?" not in url else None,
                timeout=self.timeout,
            )

            if response.status_code >= 400:
                print(f"ERROR: GET {response.url}")
                print(f"Status: {response.status_code}")
                print(f"Response: {response.text}")
                response.raise_for_status()

            data = response.json()
            results.extend(data.get("results", []))
            url = data.get("next")
            query = {}

        return results
