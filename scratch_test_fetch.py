#!/usr/bin/env python3
"""
Scratch script to test fetching chicken rate endpoints safely.
"""
import sys
from typing import Optional
import requests

def test_fetch(url: str = "https://chickenratetoday.in/today-chicken-rate-hyderabad/") -> Optional[requests.Response]:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    r: Optional[requests.Response] = None
    try:
        r = requests.get(url, headers=headers, timeout=15)
        print(f"Status: {r.status_code}")
    except Exception as exc:
        print(f"Request failed: {exc}")

    if r is not None:
        print(f"Fetched {len(r.text)} characters")
    return r

if __name__ == "__main__":
    test_fetch()
