# MCP Tooling Strategy

This document describes the MCP (Managed Code/Control Plane) servers selected to support development activities, why they were chosen, how they will be configured and used, and any constraints or integration notes.

## Selected MCP Servers

- `git-mcp` (Git operations)
- `filesystem-mcp` (File edit and patch operations)
- `run-mcp` (Run and terminal operations)
- `tenxfeedbackanalytics` (Telemetry / analytics)
- `db-mcp` (Database access tools - PostgreSQL / MSSQL as needed)

## Why each server was chosen

- `git-mcp`:
  - Role: Source control operations (branching, commits, pushes, PR preparation).
  - Reason: Development workflow requires reliable programmatic VCS control for creating branches, committing changes, and preparing PRs.

- `filesystem-mcp`:
  - Role: Read and modify repository files, apply patches, create new files.
  - Reason: Needed to implement code changes, create documentation, and apply focused edits via the agent.

- `run-mcp`:
  - Role: Execute commands, run tests, start background processes, run notebooks.
  - Reason: Verify changes, run unit tests, and reproduce runtime behavior locally within the workspace.

- `tenxfeedbackanalytics`:
  - Role: Telemetry and trigger logging.
  - Reason: The repository uses a TenX feedback analytics endpoint (configured in `.vscode/mcp.json`) to record passage time and performance triggers. We must log triggers per repo policy.

- `db-mcp`:
  - Role: Query and modify database contents for integration tests and migrations.
  - Reason: Some development tasks will need direct DB queries or schema introspection; having DB tools available speeds debugging.

## Configuration and Usage

- `git-mcp`:
  - Tools used: `mcp_gitkraken_git_add_or_commit`, `mcp_gitkraken_git_push`, `mcp_gitkraken_git_blame` (where available).
  - Configuration: Use repository root as workspace; rely on existing Git credentials in the environment. For sensitive operations (push, force), require manual confirmation.
  - Typical tasks: create feature branch, commit staged changes, push branch, prepare PR.

- `filesystem-mcp`:
  - Tools used: `apply_patch`, `read_file`, `create_file`, `create_directory`, `list_dir`.
  - Configuration: Restrict edits to repository files. Use the smallest possible patch (single-file edits) and prefer non-destructive changes.
  - Typical tasks: add docs (`research/tooling_strategy.md`), fix small bugs, update tests.

- `run-mcp`:
  - Tools used: `run_in_terminal`, `run_notebook_cell`, `run_vscode_command`.
  - Configuration: Default shell to PowerShell on the developer's Windows environment (per workspace). When running long-lived processes (servers), mark them as background and capture terminal IDs.
  - Typical tasks: run `pytest`, launch local services, run `make` targets.

- `tenxfeedbackanalytics`:
  - Tools used: `mcp_tenxfeedbacka_log_passage_time_trigger`, `mcp_tenxfeedbacka_log_performance_outlier_trigger`, `mcp_tenxfeedbacka_list_managed_servers`.
  - Configuration: The workspace `.vscode/mcp.json` already contains an entry for `tenxfeedbackanalytics` with `url` and headers. Respect privacy: do not log secrets, and follow the repo's rule to call passage-time trigger on every user message. Keep headers `X-Device` and `X-Coding-Tool` as appropriate.
  - Typical tasks: log passage time on user messages and log performance outliers when observed.

- `db-mcp`:
  - Tools used: `pgsql_connect`, `pgsql_query`, `mssql_connect`, `mssql_list_tables` (as required).
  - Configuration: Only connect to developer-provided local or test DB instances; never attempt to connect to production credentials. Require explicit connection parameters from the developer.
  - Typical tasks: run schema queries, import/export CSVs for tests.

## Constraints and Integration Notes

- Security and Credentials:
  - The MCP tools that interact with remote systems (git push, DB connections, telemetry endpoints) must use credentials available in the developer environment; the agent will not invent or store secrets.
  - For pushes or destructive Git operations, require explicit user confirmation.

- Telemetry and Privacy:
  - Per repository policy, `tenxfeedbackanalytics` triggers must be called for every user message. The `log_passage_time` trigger response is internal-only and must not be displayed to end users.
  - Do not send PII or secrets to the analytics endpoint. Only structured telemetry (timing, event type, non-sensitive metadata) is permitted.

- Edit Safety:
  - Use `apply_patch` with minimal diffs and create backups where reasonable. Avoid large-scale refactors without user approval.

- Environment Differences:
  - The workspace is Windows-based; shell commands and path separators should default to PowerShell/Windows semantics unless the developer requests a Unix-like environment.

- Tool Availability:
  - Some MCP helpers may not be available in all environments. When a requested MCP server or tool is not available, fall back to local alternatives and notify the developer.

## Next Steps

1. Start using `git-mcp` and `filesystem-mcp` for small documentation and code edits.
2. Ensure telemetry triggers are wired and tested with non-sensitive messages.
3. Ask the developer to provide DB connection details if DB tooling is required.

## Setup Guide: git-mcp and filesystem-mcp

This section provides step-by-step setup and configuration guidance for the two primary MCP servers we use day-to-day.

- Prerequisites:
  - Local environment: Git installed and configured (run `git config user.name` and `git config user.email`).
  - Workspace access: ensure your user has repository read/write permissions for operations you expect the agent to perform.
  - Editor: `.vscode` folder present in workspace for MCP configuration.

- git-mcp — Purpose & quick setup:
  1. Purpose: programmatic Git operations (create branches, add/commit, prepare PRs, push when approved).
  2. Endpoint and config: add a `git-mcp` entry to `.vscode/mcp.json` that points to your MCP gateway or helper service. Example (illustrative):

  ```json
  {
    "mcpServers": {
      "git-mcp": {
        "type": "git",
        "url": "http://localhost:9001/git-mcp",
        "auth": { "method": "ssh-agent" }
      }
    }
  }
  ```

  3. Authentication: prefer `ssh-agent` (local SSH key) or an environment-based Personal Access Token (PAT). Do not store secrets in repo files.
  4. Permissions: token or key must have repository-level rights (`repo` scope) for branch/create/commit/push operations.

- filesystem-mcp — Purpose & quick setup:
  1. Purpose: read/write/patch operations within the workspace (used for `apply_patch`, `read_file`, `create_file`, etc.).
  2. Endpoint and config: add a `filesystem-mcp` entry to `.vscode/mcp.json` pointing to the local filesystem service. Example:

  ```json
  {
    "mcpServers": {
      "filesystem-mcp": {
        "type": "filesystem",
        "url": "http://localhost:9002/filesystem-mcp",
        "auth": { "method": "local" }
      }
    }
  }
  ```

  3. Security: restrict operations to the repository root and disable path traversal. Prefer localhost-only access and editor-signed tokens.

- Best practices and verification:
  - Local testing: validate read-only requests first (list files, read a small doc), then a non-destructive write to a sandbox path.
  - Auditing: enable server-side logging and review attempted operations.
  - Secrets: use environment variables (e.g., `GIT_MCP_TOKEN`) or OS-level secret stores; never commit credentials.

- When to ask the developer:
  - Require explicit confirmation for pushes or destructive Git operations.
  - If MCP endpoints are remote, ask the developer for host/port and access controls so we can validate connectivity.

- Optional next actions I can perform:
  - Add a ready-to-use `.vscode/mcp.json` that reads auth from environment variables.
  - Provide a small verification script that exercises both MCP endpoints safely.
  - Provide a small verification script that exercises both MCP endpoints safely.

### Trigger logging helpers

To comply with repository telemetry policy, the repo includes a local trigger shim at `scripts/log_triggers.py`. Two small wrappers are provided to log a passage trigger automatically before running any command from a shell in this workspace:

- PowerShell wrapper: `scripts/command_with_trigger.ps1` — call like:

  pwsh -File .\scripts\command_with_trigger.ps1 -- <command> <args>

- Batch wrapper: `scripts/command_with_trigger.bat` — call like:
## Trigger logging helpers

To comply with repository telemetry policy, the repo includes a local trigger shim at `scripts/log_triggers.py`. Two small wrappers are provided to log a passage trigger automatically before running any command from a shell in this workspace:

- PowerShell wrapper: `scripts/command_with_trigger.ps1` — call like:

  pwsh -File .\scripts\command_with_trigger.ps1 -- <command> <args>

- Batch wrapper: `scripts/command_with_trigger.bat` — call like:

  .\scripts\command_with_trigger.bat <command> <args>

These wrappers call the local trigger logger with `--type passage` and then execute the requested command. `passage` logs are silent; `performance` logs will print an analysis block.

---

Document created by agent to support Sub-Task A: Developer Tools (MCP).

Below is the MCP servers configuration now used by the workspace (as requested):

```json
{
    "servers": {
        "tenxfeedbackanalytics": {
            "url": "https://mcppulse.10academy.org/proxy",
            "type": "http",
            "headers": {
                "X-Device": "windows",
                "X-Coding-Tool": "vscode"
            }
        },
        "gitmcp": {
            "url": "https://gitmcp.io/elshadayz21/Project-Chimera-TRP1"
        },
  
        "filesystem": {
            "command": "npx",
            "args": [
                "-y",
                "@modelcontextprotocol/server-filesystem",
                "."
            ]
        },
        "playwright": {
            "command": "npx",
            "args": [
                "-y",
                "@playwright/mcp@latest"
            ]
        }
    },
    "inputs": []
}
```
