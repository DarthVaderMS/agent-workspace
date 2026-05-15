---
name: komodo
description: Interact with the Komodo infrastructure management API (https://komo.do). Use when asked to manage servers, deployments, stacks (Docker Compose), builds, repos, procedures, actions, syncs, alerters, variables, or users on a Komodo instance. Covers read (query), write (create/update/delete), and execute (deploy, start, stop, restart, build, run) operations. Trigger on requests like "list deployments", "restart the stack", "run the build", "check server status", "create a procedure", etc.
metadata:
  {
    "openclaw":
      {
        "homepage": "https://komo.do",
        "requires": { "env": ["KOMODO_URL", "KOMODO_API_KEY", "KOMODO_API_SECRET"] },
        "primaryEnv": "KOMODO_API_KEY",
      },
  }
---

# Komodo v2 API

Komodo is an infrastructure management platform. Use this skill for Komodo Core v2 API calls only. API docs:
- Overview: https://komo.do/docs/ecosystem/api
- Request schemas: https://docs.rs/komodo_client/latest/komodo_client/api/index.html

## Auth & Config

Set exactly these three environment variables before calling Komodo:
```bash
export KOMODO_URL="https://komodo.example.com"
export KOMODO_API_KEY="your_key"
export KOMODO_API_SECRET="your_secret"
```

`KOMODO_API_KEY` and `KOMODO_API_SECRET` map directly to Komodo's required `X-Api-Key` and `X-Api-Secret` headers. Do not print them, commit them, or include them in logs.

Komodo v2 requests use **POST** to `/$path/$type` with the params object as the JSON body. Do not use the older wrapper body shape `{ "type": "...", "params": { ... } }`.

Headers:
```
Content-Type: application/json
X-Api-Key: derived from $KOMODO_API_KEY
X-Api-Secret: derived from $KOMODO_API_SECRET
```

## Helper Script

Use `scripts/komodo.sh` for all API calls:
```bash
bash ~/.openclaw/workspace/skills/komodo/scripts/komodo.sh <path> <type> [params_json]
```

- `path`: `read`, `write`, `execute`, `auth`, or `user`
- `type`: request type (e.g. `GetDeployment`, `Deploy`, `ListServers`)
- `params_json`: optional JSON string (default `{}`)

Examples:
```bash
# List all servers
bash ~/.openclaw/workspace/skills/komodo/scripts/komodo.sh read ListServers

# Get a specific deployment
bash ~/.openclaw/workspace/skills/komodo/scripts/komodo.sh read GetDeployment '{"deployment":"my-app"}'

# Deploy a deployment
bash ~/.openclaw/workspace/skills/komodo/scripts/komodo.sh execute Deploy '{"deployment":"my-app"}'

# Restart a stack
bash ~/.openclaw/workspace/skills/komodo/scripts/komodo.sh execute RestartStack '{"stack":"my-stack"}'

# Create a server
bash ~/.openclaw/workspace/skills/komodo/scripts/komodo.sh write CreateServer '{"name":"prod-01","config":{"address":"10.0.0.1"}}'
```

## API Modules

| Path | Purpose |
|------|---------|
| `read` | Query data — list/get resources, logs, stats |
| `write` | Mutate data — create/update/delete/rename resources |
| `execute` | Run actions — deploy, build, start, stop, restart |
| `auth` | Login, obtain JWT |
| `user` | Self-management, API key management |

For full request types and params, see:
- `references/read.md` — all read operations
- `references/write.md` — all write operations
- `references/execute.md` — all execute operations

## Error Format

```json
{ "error": "top level message", "trace": ["detail1", "detail2"] }
```
