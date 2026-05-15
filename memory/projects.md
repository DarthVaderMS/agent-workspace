# Projects

Active projects Vader is involved in.

---

## Confluence + OpenClaw Integration

**Status:** In progress (as of 2026-03-18)
**Goal:** Route @agent mentions in Confluence (comments and pages) to the correct OpenClaw agent via Automation webhook.

**Done:**
- `confluence.js` transform handles both comment and page mention contexts
- Vader rule (UUID: 019d0162-a338-7210-8481-960dff8f80ad) configured and ENABLED
- Automation API limitations discovered: Vader can update rules but not create them (403)
- Import file ready for remaining 4 assistant: `workspace/tmp/confluence-rules-import.json`

**Pending:**
- Miguel to create/import Vader rules via Confluence UI
- End-to-end test: mention @Vader in a Confluence comment → confirm OpenClaw receives and routes correctly

**Key references:**
- API base: `https://api.atlassian.com/automation/public/confluence/f9e5089d-ef88-4b42-9b84-03e9c2886d6b/rest/v1/`
- Hooks endpoint: `https://openclaw.miguel.ms/hooks` (token: `OPENCLAW_HOOKS_TOKEN` in .env)
- Confluence admin automation: `https://miguelms.atlassian.net/wiki/admin/automation`
- Tracking page: https://miguelms.atlassian.net/wiki/spaces/AIM/pages/5898326

---

## Vader — New Agent Deployment

**Status:** Planning (as of 2026-03-18)
**Goal:** Deploy Vader as a web research and intelligence agent on OpenClaw.
**Slack manifest:** shared in #integrations on 2026-03-14; description: "Web research and intelligence. If it exists online, she finds it."
**Pending:** Slack app creation, OpenClaw wiring, workspace setup.
