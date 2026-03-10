"""
Step 4: POST the answer to the hub; print response (flag or error).
"""
from pathlib import Path

import requests
from dotenv import load_dotenv

VERIFY_URL = "https://hub.ag3nts.org/verify"
TASK_NAME = "people"

# Load .env from Task directory (parent of src)
_env_path = Path(__file__).parent.parent / ".env"
load_dotenv(_env_path)


def step_submit(answer: list[dict], apikey: str | None = None, task: str | None = None) -> dict:
    """POST answer to hub; return response JSON. Raises on HTTP errors."""
    if apikey is None:
        import os
        apikey = os.environ.get("apikey")
    if not apikey:
        raise ValueError("apikey not set: add apikey=... to .env or pass step_submit(..., apikey=...)")
    if task is None:
        task = TASK_NAME

    payload = {
        "apikey": apikey,
        "task": task,
        "answer": answer,
    }
    response = requests.post(VERIFY_URL, json=payload, timeout=30)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        body = response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text
        raise RuntimeError(f"Hub {response.status_code}: {body}") from None
    return response.json()
