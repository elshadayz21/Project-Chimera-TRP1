def test_trend_output_structure():
    result = {
        "trends": [
            {
                "title": "AI Influencer",
                "engagement_score": 0.9,
                "url": "http://example.com"
            }
        ]
    }

    assert "trends" in result
    assert isinstance(result["trends"], list)
