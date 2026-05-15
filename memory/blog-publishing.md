# Blog Publishing — Vader's Workflow

This file is the publishing pipeline only. Both the daily **Blog Auto-Publish** cron and any interactive "publish this post" request follow it.

**Writing quality is Vader's responsibility.** Drafts should arrive ready: em-dash free, byline + research credit present, description 150-160 chars, cross-links inlined using `postUrl`, social posts appended, no decorative `---` lines in the body. The single source of truth for writing is `workspace/memory/writing.md`. If a draft is structurally wrong, fix it directly before publishing.

Repo-side code rules (SEO, accessibility, performance, GDPR, TypeScript) live in the repo's own `CLAUDE.md` at `source/github.com/migueltvms/miguel-ms-website/CLAUDE.md`. Read that file when needed; do not duplicate it here.

## Paths

- **Obsidian drafts**: `/home/openclaw/Obsidian/Personal/My Website/Articles/*.md` (status: draft)
- **Obsidian published archive**: `/home/openclaw/Obsidian/Personal/My Website/Articles/Published/*.md`
- **Obsidian images**: `/home/openclaw/Obsidian/Personal/Files/Images/YYYY-MM-DD-<slug>.png`
- **Local repo**: `/home/openclaw/.openclaw/workspace/source/github.com/migueltvms/miguel-ms-website`
- **Site blog files**: `src/content/blog/YYYY-MM-DD-<slug>.md`
- **Site hero images**: `public/images/blog/YYYY-MM-DD-HH-MM-SS-<slug>.webp`

When scanning for drafts, ignore `Articles MOC.md` and the `Published/` subfolder.

## Draft eligibility

Publish a draft when frontmatter `status: draft` AND date (from `created` or filename prefix) is `<= $(date +%Y-%m-%d)`.

## Per-post pipeline

### Slug
Filename `YYYY-MM-DD <Title>.md` → slug is `<Title>` lowercased, kebab-cased, punctuation stripped.

### Hero image
1. Find the `![[YYYY-MM-DD-<something>.png]]` reference in the body and locate the matching file in `Files/Images/`.
2. Convert with Pillow: WebP, exact 1200×630, quality 85 (back off if output >200KB; target ≤200KB).
3. Save to `public/images/blog/YYYY-MM-DD-HH-MM-SS-<slug>.webp`.

### Site markdown
Write `src/content/blog/YYYY-MM-DD-<slug>.md`.

Frontmatter (rebuild from Vader's Obsidian frontmatter — do not carry his fields verbatim):

```yaml
title: "<title from filename>"
description: "<copy from Obsidian description>"
pubDate: YYYY-MM-DD
author: "Vader Calrissian"
research: "Vader"
heroImage: "/images/blog/<filename>.webp"
tags: ["miguel-ms", "blog", <other tags from Obsidian>]
```

The `author` and `research` fields are displayed in the hero section (under the title) as linked names:
`[Author Name] — Date — Research by [Researcher Name]`

Body: copy as-is from the Obsidian draft, with these mechanical strips:
- **Frontmatter block** — replaced by the schema above; do not carry Obsidian fields over
- **Byline and research lines** — DELETE any `**By [Name]...**` or `**Research by [Name]...**` lines from the body. Attribution now appears ONLY in the hero section via frontmatter fields
- **Hero image** — The **first image** in the draft (the first `![[file.png]]` after frontmatter) is the hero image. Convert it to WebP and set it in the `heroImage` frontmatter field. When publishing to the site, **omit this first image from the body markdown**—it's already displayed in the hero section via frontmatter. Do not include it twice. Subsequent images in the draft are body images.
- **Image embeds** `![[file.png]]` — for images in the body (after the first), replace with proper markdown image pointing to the converted WebP
- **Wikilinks** `[[Page]]` — Vader's drafts use absolute `https://miguel.ms/blog/<slug>/` URLs for cross-links via `postUrl`, so wikilinks should be rare; if present, remove or rewrite to prose
- **Social Posts section** — Vader appends `# Social Posts` (H1, sibling to the article title) separated from the body by a single `---` rule. Cut from that separator (inclusive) through end-of-file. The published body ends with Vader's last paragraph, no trailing rule. Older drafts may still use `## Social Posts` (H2) — strip from the same `---` separator either way.

**Team-page links in body** — wrap FIRST occurrence of every team member (other than author/researcher) in a markdown link when they appear in prose. Author and researcher are already linked in the hero section, so only link them in the body if they're mentioned again later in the article.

Team page mappings:
| Vader Calrissian | `https://miguel.ms/team/vader/` |
| Vader | `https://miguel.ms/team/vader/` |
| Vader | `https://miguel.ms/team/vader/` |
| Vader | `https://miguel.ms/team/vader/` |
| Vader | `https://miguel.ms/team/vader/` |
| Darth Vader | `https://miguel.ms/team/vader/` |

The body is otherwise untouched. No prose edits. No em-dash substitutions. No restructuring.

### Build
```bash
cd /home/openclaw/.openclaw/workspace/source/github.com/migueltvms/miguel-ms-website
npm run build
```
If build fails, revert the new blog file and image, abort, report.

## Git workflow — dual-branch publish

The blog is served from `main`. Posts MUST land on BOTH `develop` AND `main`. Never leave one branch ahead.

```bash
git checkout develop
git config user.name 'Vader'
git config user.email 'vader@miguel.ms'
git add -A
git commit -m 'feat(blog): auto-publish <N> article(s) from Obsidian'
git push git@github-vader:MiguelTVMS/miguel-ms-website.git develop
git checkout main
git merge --no-ff develop -m 'Merge develop: auto-publish'
git push git@github-vader:MiguelTVMS/miguel-ms-website.git main
git checkout develop

# Verify
git log --oneline -1 develop
git log --oneline -1 origin/main
```

Both must show the auto-publish commit. If either doesn't, or any push fails (non-zero exit, auth error, rejected), the publish is incomplete — abort and report.

Remote: always `git@github-vader:` (SSH host alias). Never `git@github.com:` or HTTPS.

## Push-approval policy — and the one exception

**Default** (from MEMORY.md): never push to `develop` or `main` without explicit João approval. Applies to all interactive work, blog posts included.

**Exception — the Blog Auto-Publish cron only** (id `12f9a4e6-69bf-4129-8581-a964f753675d`, pre-approved by João 2026-04-16): push develop AND main autonomously as part of the cron flow. ONLY bypass. Interactive "publish this" requests still require explicit go-ahead.

**Interactive staging-only publish is allowed when explicitly requested.** On 2026-04-30, João requested publishing `2026-04-30 The AI Rebrand Selling the Perception of Transformation` to `develop` only; that flow is valid with explicit request, but it does **not** imply permission to push `main`.

## Post-publish cleanup

For each article whose commit landed on BOTH branches:

1. Move the Obsidian file from `Articles/` to `Articles/Published/`
2. Update the moved file's frontmatter:
   - `status: draft` → `status: published`
   - Add `postUrl: "https://miguel.ms/blog/<slug>/"` (camelCase, trailing slash)
3. Update `Articles MOC.md` (`/home/openclaw/Obsidian/Personal/My Website/Articles/Articles MOC.md`):
   - Remove the article's wikilink from the `## Drafts (Scheduled)` section
   - Add the same wikilink at the top of the `## Published` section (newest first)
   - Do NOT reorder other entries; only the moved article changes position

Skip cleanup for any article whose branches are out of sync. If the MOC update fails (file unreadable, wikilink not found in Drafts, etc.) treat it as a publish failure per Failure mode — the index must stay in sync.

## Failure mode

Any failure — build, push, dual-branch verify, post-publish cleanup, OR a structural defect in Vader's draft (missing byline, missing research credit, description outside 150-160 chars, em-dashes visible in body, decorative `---` lines in the body) — aborts the publish for that article. Don't paper over. Don't edit Vader's prose. Reply:

```
⚠️ **Blog Auto-Publish failed** — <article title>: <one-line cause, ≤200 chars>
```

Vader re-ships the draft on his next turn.

## Reply format

- **Cron, nothing to publish**: reply exactly `NO_REPLY`.
- **Cron, success (N≥1)**: `📝 Published N article(s): **<Title 1>** (/blog/<slug1>), **<Title 2>** (/blog/<slug2>). Live on miguel.ms.`
- **Cron, failure**: per Failure mode above.
- **Interactive request**: follow the user's preferred format; default to brief status report.
