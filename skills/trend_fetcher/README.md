# Trend Fetcher Skill

Purpose
-------
Fetch and normalize trending topics, signals, and metrics from multiple sources (social, news, search) for research and alerting.

Primary skill: `skill_trend_fetcher`

Input contract
--------------
JSON object with the following fields:

- `query` (string, optional): Search term or topic to focus on. If omitted, returns global/top trends.
- `sources` (array, optional): List of sources to query, e.g. `twitter`, `newsapi`, `google_trends`. Default: all available.
- `timeframe` (string, optional): `24h` | `7d` | `30d` | custom ISO range.
- `limit` (integer, optional): Max number of trends to return (default 20).
- `filters` (object, optional): Additional filters (language, region, min_score).

Example
```json
{
  "query": "agentic AI",
  "sources": ["twitter","newsapi"],
  "timeframe": "7d",
  "limit": 10,
  "filters": {"language":"en"}
}
```

Output contract
---------------
JSON object with the following fields:

- `request_id` (string): Unique id for this fetch request.
- `generated_at` (ISO 8601 timestamp)
- `trends` (array): Each trend object contains:
  - `title` (string)
  - `score` (number): Normalized score across sources
  - `source` (string)
  - `url` (string|null)
  - `sample_items` (array): Small list of example posts/articles
  - `metadata` (object): e.g., `region`, `language`, `volume_estimate`

Example
```json
{
  "request_id": "tf-20260205-0001",
  "generated_at": "2026-02-05T12:20:00Z",
  "trends": [
    {
      "title": "agentic AI",
      "score": 0.87,
      "source": "twitter",
      "url": null,
      "sample_items": ["Tweet A...","Tweet B..."],
      "metadata": {"region":"global","language":"en","volume_estimate":12000}
    }
  ]
}
```

Notes
-----
- The skill should normalize scores across heterogeneous sources and annotate provenance for each trend.
- Rate limiting and API quotas must be respected; support cached results and graceful degradation.
