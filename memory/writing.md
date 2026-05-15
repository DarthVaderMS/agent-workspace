---
name: Writing Rules & Instructions
description: Consolidated writing rules, tagging standards, voice, tone, and publishing workflow for Vader's articles
type: feedback
---

# Writing Rules

## Voice & Tone

- Warm but sharp. Approachable but never fluffy.
- Strong hooks — every piece earns the reader's attention in the first two sentences.
- Clear structure — readers should never wonder where they are.
- Active voice. Short paragraphs. Scannable without losing depth.
- No hedging ("perhaps", "could be argued", "it might be") — make claims and own the tone.
- No em-dashes in headers or body text.
- Confidence, always. Readers trust writers who sound like they know what they're talking about.

## Tagging in Obsidian

**MANDATORY BEFORE TAGGING:**
1. Use the Obsidian CLI to read all available tags in the vault
2. Check if existing tags fit your article's needs
3. Only create new tags if no appropriate existing tag matches
4. Follow the existing tag format and naming conventions

**Tag Format Rules:**
- Lowercase only
- Hyphens for multi-word tags (e.g., `competitive-analysis`, `miguel-ms`)
- Can use nested tags (e.g., `ai/agents/vader`)
- **Mandatory tags on every article:** `article`, `miguel-ms`, `blog`
- Topic tags: Use existing tags when possible (e.g., `ai`, `anthropic`, `github`, `openclaw`, `business`, `society`, `cybersecurity`, `hardware`)

**Example from existing article:**
```yaml
tags:
  - article
  - miguel-ms
  - blog
  - ai
  - business
  - anthropic
  - openai
  - competitive-analysis
```

## Publishing Workflow

1. **Write the article** in Markdown based on Miguel's brief + research
2. **Save to Obsidian** at `/home/openclaw/Obsidian/Personal/My Website/Articles/`
3. **Filename format:** `YYYY-MM-DD <Title>.md` (strip colons, angle brackets, pipes)
4. **Add required frontmatter:**
   - `tags:` (article, miguel-ms, blog + topic tags)
   - `created:` (ISO timestamp)
   - `status:` (draft or published)
   - `description:` (one-line hook)
   - `parent:` ([[Articles MOC]])
5. **Update Articles MOC.md** after every new article
6. **Add social posts** at the end (LinkedIn + X) before final handoff — keep them in the file for Vader's workflow only, never include when sending to others

## Social Posts Section Format

Always append after the article body, separated by two HR lines:

```
---
---

## Social Posts

### LinkedIn

[LinkedIn post — paragraph format, insight-led, ends with [link], hashtags]

---

### X

[Single post ≤280 chars, punchy, ends with [link]]
```

## Articles MOC

- **Location:** `/home/openclaw/Obsidian/Personal/My Website/Articles/Articles MOC.md`
- **Update after every new article** — add link under Drafts or Published, newest first
- **Frontmatter:** parent = "[[My Website]]", tags = moc + articles

## Images

Only generate when they add real value. Never more than 3 per article. Quality > Quantity.
- **Save to:** `/home/openclaw/Obsidian/Personal/Files/Images/` (canonical)
- **Embed:** Use Obsidian wikilink syntax: `![[filename.png]]` (not markdown `![alt](url)`)
- **Naming:** `YYYY-MM-DD-slug.png`
- **Placement:** Right after frontmatter

## SEO & Descriptions

- Description = one-line hook that makes someone click
- SEO-aware but never obvious — write for humans first
- Research must support all claims — no speculation published as fact
- Don't pad. If you've said what needs saying, stop.

## Byline & Research Credit

Include research credit format when appropriate (follow existing pattern from published articles).

---

*Last updated: 2026-04-23*

# Writing

Seed: **Single source of truth** for writing: voice, tone, em-dash ban, byline/credit format, description length, hedging ban, proven patterns, self-check before finalizing
