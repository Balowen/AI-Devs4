"""
Step 3: Keep only people with tag "transport"; return the answer list for the hub.
"""
TRANSPORT_TAG = "transport"


def step_build_answer(tagged: list[dict]) -> list[dict]:
    """Filter to persons whose tags include "transport". Return list in answer format."""
    return [p for p in tagged if TRANSPORT_TAG in p.get("tags", [])]
