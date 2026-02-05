## Trend Fetch API Contract

Input:
{
  "platform": "tiktok | youtube | twitter",
  "region": "string"
}

Output:
{
  "trends": [
    {
      "title": "string",
      "engagement_score": float,
      "url": "string"
    }
  ]
}
