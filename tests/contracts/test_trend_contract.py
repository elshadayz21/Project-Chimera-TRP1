import json
from pathlib import Path
import jsonschema


def load_schema():
    schema_path = Path("specs/schemas/trend.schema.json")
    return json.loads(schema_path.read_text())


def test_trend_output_matches_schema():
    schema = load_schema()

    # Simulated future agent output
    agent_output = {
        "trends": [
            {
                "title": "AI Influencers 2026",
                "engagement_score": 0.92,
                "source_url": "https://example.com/trend"
            }
        ]
    }

    jsonschema.validate(agent_output, schema)
