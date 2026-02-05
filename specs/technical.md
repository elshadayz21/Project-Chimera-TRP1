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

# Technical Specifications

## API Contracts

- **GET /trends**: Fetch current trends.
  - **Input**: None
  - **Output**: JSON array of trends.

## Database Schema

- **Video Metadata**: Store information about videos.
  - Fields: ID, Title, Description, URL, CreatedAt, UpdatedAt

![ERD Diagram](link_to_erd_diagram)
