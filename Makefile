setup:
	uv sync

test:
	pytest

run:
	uv run python main.py
