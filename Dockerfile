FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1

WORKDIR /app
ENV PYTHONPATH=/app

# system deps needed for some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
	build-essential \
	gcc \
	git \
 && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install runtime + dev dependencies (as pinned in pyproject.toml)
RUN pip install --upgrade pip setuptools wheel

# Runtime dependencies
RUN pip install --no-cache-dir \
	fastapi>=0.110 \
	pydantic>=2.6 \
	pydantic-settings>=2.2 \
	httpx>=0.27 \
	redis>=5.0 \
	python-dotenv>=1.0 \
	loguru>=0.7 \
	tenacity>=8.2 \
	jsonschema>=4.26.0

# Dev / test dependencies
RUN pip install --no-cache-dir \
	pytest>=8.0 \
	pytest-asyncio>=0.23 \
	ruff>=0.3 \
	mypy>=1.8

# Copy project files
COPY . /app

# Default command runs tests so `docker run image` validates the environment
CMD ["pytest", "-q"]
