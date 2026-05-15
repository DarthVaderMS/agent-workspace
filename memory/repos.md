# memory/repos.md — Active Repositories

## miguel-ms-website

- **Repo**: https://github.com/MiguelTVMS/miguel-ms-website
- **Site**: https://miguel.ms
- **Staging**: https://develop.miguel-ms-website.pages.dev
- **Stack**: Astro 5, Tailwind CSS, TypeScript, Cloudflare Pages
- **Default branch**: develop → main (prod) on explicit João approval only
- **SSH remote**: `git@github-vader:MiguelTVMS/miguel-ms-website.git`
- **Deploy**: Cloudflare Pages — auto-deploys develop and main branches

### Open GitHub Issues (as of 2026-03-12)
| # | Title | Status |
|---|-------|--------|
| #2 | SEO: JSON-LD, meta audit, internal linking | ✅ Done on develop (6fa75a1) — awaiting prod approval |
| #3 | Services / Capabilities page | ⏳ Blocked on João input |
| #4 | Booking link on Contact page | ✅ Done on develop (93b2aeb) — two-column card layout, direct link button |
| #5 | Social proof | ⏳ Blocked on assets from João |
| #6 | RSS feed + newsletter | ⏳ RSS ready to implement; newsletter awaiting decision |
| #7 | OSS cards — activity signals | ✅ Done on develop (6fa75a1) — awaiting prod approval |
| #8 | Bevel Lemelisk hiring slot | ⏳ Awaiting João confirmation |
| #9 | CTA improvements | ⏳ Depends on #3, #4 |

### Key CLAUDE.md Rules (always re-read the file itself)
- SEO checklist mandatory on every page create/update
- Sitemap: verify after every page add/remove/update; auto-generated — never edit manually
- Confluence docs must be read/updated before any stack/tech change
- No consulting language; banned words: "clients", "we offer", "our services", "consulting" (as service), "we" (corporate)
- Star Wars disclaimer required in footer (via BaseLayout)
- OG images must be PNG (SVG not supported by LinkedIn crawlers)
- GDPR: consent defaults denied before GTM loads
- JSON-LD: server-side in `<head>`, never client-side

### Architecture Notes
- Blog content: `src/content/blog/` (Astro Content Collections)
- Blog schema: `src/content.config.ts` — `heroImage` is `z.string().optional()`
- GitHub API fetch at build time only (no runtime calls) — `index.astro` for OSS section
- GTM container: `GTM-T6BGMSJ5` | GA4: `G-VCP2Z36BFT`
- BaseLayout `head` slot available for page-level JSON-LD injection
- Team profiles: Dynamic `/team/[id].md.ts` endpoint (Astro routing) — returns clean markdown with frontmatter stripped (LLM-crawler-friendly)

### Completed Features (Recent)
- **Team Pages** (2026-04-14): 6 agent profiles (`/team/vader.md`, `/team/vader.md`, `/team/vader.md`, `/team/vader.md`, `/team/vader.md`, `/team/vader.md`)
  - Each profile includes: name, role, description, specialization, clearance level, status, tagline, full bio
  - OG image: Falls back to site default (portrait avatars cause 1200×630 stretch)
  - llms.txt: Added "Team Profiles" section with all 6 links
  - Production: https://miguel.ms/team (live after João's "push prod" on 2026-04-14)
- **Blog workflow source migration** (2026-04-21): publishing now starts from Obsidian drafts and images instead of Confluence; cron and manual publishing follow the same Obsidian-backed pipeline.
- **AI Rebrand article staged on develop** (2026-04-30): published `2026-04-30 The AI Rebrand Selling the Perception of Transformation` to `develop` only by explicit request, then added the later hero image in a follow-up fix. Staging URL: `https://develop.miguel-ms-website.pages.dev/blog/2026-04-30-the-ai-rebrand-selling-the-perception-of-transformation/`.

---

## tplink-omada-mcp

- **Repo**: https://github.com/MiguelTVMS/tplink-omada-mcp
- **Stack**: TypeScript, Node.js, MCP SDK
- **SSH remote**: `git@github-vader:MiguelTVMS/tplink-omada-mcp.git`
- **GitFlow**: feature/fix/hotfix off develop; never commit to develop or main directly
- **Coverage requirement**: 90% per-file lines/functions/statements; 70% branches globally
- **Pre-commit**: `npm run check` (Biome + tsc) → `npm run build` → `npm test`
- **Confluence roadmap**: https://miguelms.atlassian.net/wiki/spaces/AIM/pages/2654211
- **Public repo**: NEVER link to Confluence or internal URLs in issues/PRs/code

### Phase 2 progress (as of 2026-03-29)
| Issue | Title | Status |
|-------|-------|--------|
| #73 | Device read tools | ✅ Merged v0.11.0 (PR #79) |
| #74 | Network read tools | ✅ Merged v0.12.0 (PR #81) |
| #75 | Security & VPN read tools | 🔄 PR #82 open, CI in progress |
| #76 | Medium-priority read tools | ⏳ Not started |

- **Tool count**: 281 (as of issue #75 feature branch)
- **Tests**: 1895 passing (314 test files)
- **Coverage**: 99.05% statements, 92.83% branches, 100% functions
