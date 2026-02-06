# Project Chimera

Project Chimera is an agentic infrastructure for research and experimentation with autonomous content and trend workflows. The repository contains a small set of agent skills, tooling for trigger logging, test scaffolding, and CI configuration so the agent can be developed, tested, and reviewed reliably.

Quick overview
--------------
- Skills: `skills/content_generator`, `skills/publisher`, `skills/trend_fetcher` (each has a README describing input/output contracts).
- Trigger logging: `scripts/log_triggers.py` and shell wrappers in `scripts/` to record passage/performance triggers.
- Tests: `tests/` contains TDD-style failing tests that define required skill interfaces.
- CI: `.github/workflows/main.yml` runs tests on push; `.coderabbit.yaml` contains AI review guidance.

Prerequisites
-------------
- Docker (recommended for reproducible builds) or Python 3.11+ to run locally.
- Git for source control.
- Optional tools for local development: `make` (on Unix/WSL), `pytest`, `ruff`, `mypy`.

Quickstart (Docker) — recommended
---------------------------------
1. Build the developer image:

```bash
docker build -t chimera:dev .
```

2. Run the test-suite inside the container:

```bash
docker run --rm -v "$PWD:/app" -w /app chimera:dev pytest -q
```

Local development (Windows / PowerShell)
--------------------------------------
If you prefer to run natively on Windows without `make`, do the following:

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies (runtime + dev):

```powershell
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

3. Run tests:

```powershell
pytest -q
```

Makefile targets (Unix / WSL / CI)
---------------------------------
- `make build` — builds the Docker image (`chimera:dev`).
- `make setup` — builds the Docker image and prepares environment.
- `make test` — runs tests inside Docker.
- `make spec-check` — runs a lightweight spec verification script `scripts/spec_check.py`.

Trigger logging
---------------
To comply with repository policy, a small local trigger shim records events for every command you run via the provided wrappers:

- `scripts/log_triggers.py` — logs to `.tenx_triggers/logs.json` and prints performance feedback for `performance` triggers.
- PowerShell wrapper: `scripts/command_with_trigger.ps1` — calls the passage trigger then runs the command.

Example (PowerShell):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\command_with_trigger.ps1 -- python main.py
```

Project structure (high level)
------------------------------
- `skills/` — skill folders and README contracts
- `scripts/` — helper scripts (trigger logging, spec-check)
- `tests/` — TDD tests that define required behavior (intentionally failing until implemented)
- `research/`, `docs/` — documentation and design notes
- `.github/workflows/` — CI workflow

How to contribute
-----------------
1. Create a branch for your change: `git checkout -b feat/your-change`.
2. Run `make test` (or local `pytest`) and add tests that define the intended behavior.
3. Implement the change, run tests locally, and push a PR.

CI & AI Review
---------------
This repo includes a GitHub Actions workflow that runs tests on pushes to `main` and a simulated AI-review config `.coderabbit.yaml` that instructs automated checks for spec alignment and security issues. See `.github/workflows/main.yml` and `.coderabbit.yaml`.

Where to look next
------------------
- Skill contracts: `skills/content_generator/README.md`, `skills/publisher/README.md`, `skills/trend_fetcher/README.md`.
- Trigger wrapper docs: [docs/trigger_wrapper.md](docs/trigger_wrapper.md)
- Tests: `tests/test_trend_fetcher.py`, `tests/test_skills_interface.py` (define the empty slots to implement)

Contact / Maintainers
---------------------
For questions about the repository or to request CI access for external review tools, open an issue or contact the repository owner.

License
-------
See repository root or ask the maintainer for licensing details.

