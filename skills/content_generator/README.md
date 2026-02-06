# Content Generator Skill

Purpose
-------
Produce high-quality textual content from structured prompts for downstream publishing or analysis workflows.

Primary skill: `skill_content_generator`

Input contract
--------------
JSON object with the following fields:

- `prompt` (string, required): The human-readable instruction or seed text to generate from.
- `format` (string, optional): Output format, e.g. `markdown`, `html`, `plain` (default `markdown`).
- `tone` (string, optional): Tone/style such as `professional`, `casual`, `technical`.
- `max_tokens` (integer, optional): Soft limit on generated length.
- `metadata` (object, optional): Free-form metadata (tags, language, audience).

Example
```json
{
  "prompt": "Write a 300-word introduction to agentic AI for product managers.",
  "format": "markdown",
  "tone": "professional",
  "max_tokens": 600,
  "metadata": {"language": "en", "audience": "product"}
}
```

Output contract
---------------
JSON object with the following fields:

- `id` (string): Unique identifier for the generated artifact.
- `content` (string): Generated text in the requested `format`.
- `summary` (string, optional): Short summary or excerpt.
- `tokens_used` (object, optional): {"prompt": n, "completion": m}
- `metadata` (object): Echoed or augmented metadata (language, word_count, generation_model).
- `generated_at` (ISO 8601 timestamp)

Example
```json
{
  "id": "cg-20260205-0001",
  "content": "# Introduction to Agentic AI\nAgentic AI refers to...",
  "summary": "Intro to agentic AI for product managers.",
  "tokens_used": {"prompt": 45, "completion": 320},
  "metadata": {"language":"en","word_count":312},
  "generated_at": "2026-02-05T12:00:00Z"
}
```

Notes
-----
- The skill should validate `prompt` and `format`, and return structured errors when inputs are invalid.
- Keep generated artifacts idempotent when given the same `prompt`+`metadata` and deterministic settings.
