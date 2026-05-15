# memory/ci.md — CI/CD Pipeline Notes

## tplink-omada-mcp

### check-readme-sync.mjs — Table Format Requirement (CRITICAL)

**Script**: `scripts/check-readme-sync.mjs`
**CI step**: "Check README sync" in "Build and Check Code Style" workflow
**Regex**: `/^\| \`([^\`]+)\` \|/gm`

The script requires tight table row format — **no padding between backtick and pipe**:
- ✅ `| \`toolName\` | Description here. |`
- ❌ `| \`toolName\`              | Description here.           |`

Sub-agents (Claude Code included) tend to write padded aligned tables. These silently pass local `npm test` but fail the CI README sync check.

**Fix pattern** (run after subprocess commits):
```js
content.replace(/^\| \`([^\`]+)\`\s{2,}\| (.+?)\s*\|?\s*$/gm,
  (_, tool, desc) => `| \`${tool}\` | ${desc.trim()} |`)
```

**Lesson**: Always run `node scripts/check-readme-sync.mjs` locally before pushing any branch that adds new tools. If subprocess updated READMEs, verify format manually.

---

### Pre-commit checklist (mandatory, all must pass)
1. `npm run check` — Biome lint + TypeScript type check
2. `npm run build` — TypeScript compilation
3. `npm test` — full test suite (314 files, ~1895 tests as of v0.12.0)

### Coverage thresholds
- Per-file: 90% lines, functions, statements
- Global: 70% branches

### Docker build (multi-arch: linux/amd64, linux/arm64)
- **Previous failure**: `npm install --omit=dev` still runs lifecycle hooks; husky (devDep) not installed → exit code 127
- **Fix**: `--ignore-scripts` in runtime stage Dockerfile (committed dc8782d)
- Tags: `ghcr.io/migueltvms/tplink-omada-mcp` + `jmtvms/tplink-omada-mcp` (latest + version)

### Release workflow
- Bump `package.json` version → update `CHANGELOG.md` → `git tag vX.Y.Z` → push tag
- GitHub Actions: npm publish + Docker multi-arch build/push triggered by tag push
- Semantic versioning: minor bump per issue/category completion (e.g., v0.11.0 → v0.12.0 for network tools)

### Node.js deprecation warning
- GitHub Actions running Node.js 20 — future update to Node.js 24 actions may be needed (non-blocking)

---

## miguel-ms-website — Blog Auto-Publish Cron

### Overview
**Cron job**: `12f9a4e6-69bf-4129-8581-a964f753675d` (Blog Auto-Publish: Confluence → miguel.ms)
**Frequency**: Daily at 08:00 WEST (Europe/Lisbon)
**Purpose**: Sync unpublished Confluence articles (page ID 99026, "Articles") to `/src/content/blog/`
**Published articles** (as of 2026-04-15): Karpathy Loop (2026-04-10), Axios Supply Chain Attack (2026-04-10), Rogue AI Agents (2026-04-13)

### Date Matching Rules
- Article title format: `YYYY-MM-DD <title>`
- Skip if date > today (future-dated)
- Publish if date ≤ today AND file not in `/src/content/blog/`

### Timeout Issue (2026-04-14 / 2026-04-15)
**Symptom**: Cron job timed out at 600s (10m default) while fetching Confluence articles.
**Root cause**: `mcp-atlassian-miguelms` (mcporter) hung on Confluence API calls due to fakeredis incompatibility (see memory/tools.md).
**Workaround**: Switched article discovery/fetching to direct Confluence REST API calls instead of mcporter.
**Timeout bumped**: 600s → 900s (15m) while the REST API workaround was integrated.

### Obsidian Blog Source Migration (2026-04-21)
- Blog source of truth moved from Confluence to Obsidian drafts under `/home/openclaw/Obsidian/Personal/My Website/Articles/`.
- Blog Auto-Publish cron `12f9a4e6-69bf-4129-8581-a964f753675d` now reads Obsidian drafts at 08:00 Lisbon, publishes eligible posts, then pushes both `develop` and `main` under the explicit cron carve-out.
- Interactive blog publishing still requires João approval before any push.

### Blog Post Requirements
- Hero images: WebP format, ≤200KB, 1200×630px (matches OG image dims)
- Description field: 150–160 chars, no em dashes
- Cross-linking: Links to related pieces (Machine That Does Its Own Research, Prediction Markets, Claude Code Source Leak, etc.)
- Build: Must pass clean (`npm run build`)
- Deployment: Commit → push to `develop` and `main` branches
