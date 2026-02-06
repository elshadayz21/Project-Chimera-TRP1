import pytest


def test_trend_output_structure():
    """The trend fetcher must implement `fetch_trends(input)` and return the contract defined in `specs/technical.md`.

    Expected output:
    {
      "trends": [
         {"title": str, "engagement_score": float, "url": str}
      ]
    }
    """

    from skills.trend_fetcher import skill

    # This should raise or fail because the implementation is missing — test defines the empty slot.
    input_payload = {"platform": "twitter", "region": "global"}

    result = skill.fetch_trends(input_payload)

    assert isinstance(result, dict)
    assert "trends" in result
    assert isinstance(result["trends"], list)

    item = result["trends"][0]
    assert isinstance(item.get("title"), str)
    assert isinstance(item.get("engagement_score"), float)
    assert isinstance(item.get("url"), str)
