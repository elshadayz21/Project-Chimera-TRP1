# Publisher Skill

Purpose
-------
Publish generated content to external channels (CMS, social, RSS) and record publication metadata for downstream tracking.

Primary skill: `skill_publisher`

Input contract
--------------
JSON object with the following fields:

- `content_id` (string, optional): Identifier referencing stored content. Either `content_id` or `content_body` required.
- `content_body` (string, optional): Raw content to publish if not using an existing `content_id`.
- `channels` (array, required): List of channel objects to publish to. Each channel object:
  - `type` (string): `cms` | `twitter` | `mastodon` | `rss` | `webhook`
  - `config` (object): Channel-specific configuration (e.g., `url`, `site_id`, `auth_ref`).
- `publish_options` (object, optional): Scheduling, tags, visibility.

Example
```json
{
  "content_id": "cg-20260205-0001",
  "channels": [
    {"type":"cms","config":{"site_id":"main-blog","path":"/posts/agentic-ai"}},
    {"type":"twitter","config":{"account":"@org_handle"}}
  ],
  "publish_options": {"scheduled_at": null, "visibility": "public"}
}
```

Output contract
---------------
JSON object with the following fields:

- `publication_id` (string): Unique id for this publish operation.
- `results` (array): One entry per channel with fields:
  - `channel` (string)
  - `status` (string): `success` | `partial` | `failed`
  - `post_id` (string|null)
  - `error` (string|null)
- `published_at` (ISO 8601 timestamp)

Example
```json
{
  "publication_id": "pub-20260205-0001",
  "results": [
    {"channel":"cms","status":"success","post_id":"12345","error":null},
    {"channel":"twitter","status":"partial","post_id":null,"error":"rate limited"}
  ],
  "published_at": "2026-02-05T12:10:00Z"
}
```

Notes
-----
- The skill should never embed secrets in logs; channel credentials must be provided via secure references (environment or secret store).
- Support dry-run mode for previewing publication results without performing network actions.
