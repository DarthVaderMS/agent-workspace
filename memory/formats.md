# Formats & Workflow

Structural patterns and production workflows Miguel has confirmed. Follow these every time.

---

## Article Production Workflow (confirmed 2026-04-16 — Obsidian publishing)

Every article follows this sequence, in order. Do not skip steps.

### 1. Read the Research
- Fetch my research from Confluence: `mcporter call mcp-atlassian-miguelms.confluence_get_page --args '{"page_id": "<ID>"}'`
- Research lives under parent `164315` (Research space). Never write there.

### 2. Write the Article
- Identify the core insight and the angle that makes it interesting
- Write clean, publish-ready Markdown
- Apply all style rules: no em dashes, active voice, strong hook, byline + research credit

### 3. Generate the Hero Image (optional — only if valuable)
- **Default provider: Gemini Imagen 4.0** (via GEMINI_API_KEY env var, direct API call)
- **Aspect ratio: 16:9** (Imagen 4.0 supports: 1:1, 9:16, 16:9, 4:3, 3:4 -- NOT 3:2)
- Output size: 1408x768 at 16:9
- **Absolutely NO text, NO logos, NO brand names, NO letters anywhere in the image** -- always include this in the prompt
- Save to: `/home/openclaw/Obsidian/Personal/Files/Images/YYYY-MM-DD-slug.png`
- Imagen 4.0 API endpoint: `https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key=$GEMINI_API_KEY`
- Payload: `{"instances": [{"prompt": "..."}], "parameters": {"sampleCount": 1, "aspectRatio": "16:9"}}`

### 4. Publish to Obsidian (CURRENT PRIMARY — as of 2026-04-16)
- **Location:** `/home/openclaw/Obsidian/Personal/My Website/Articles/YYYY-MM-DD <Title>.md`
- **Filename format:** strip colons, angle brackets, pipe characters from title
- **Required frontmatter:**
  ```yaml
  ---
  tags:
    - article
    - miguel-ms
    - blog
    - (topic tags: ai, cybersecurity, hardware, ai-agents, business, society, openclaw)
  created: YYYY-MM-DD HH:MM
  status: published
  description: "One-line description"
  parent: "[[Articles MOC]]"
  ---
  ```
- **Mandatory tags:** Every article MUST have `miguel-ms` and `blog` tags
- **Images:** Embed with Obsidian wikilink syntax `![[filename.png]]` right after frontmatter
- Update `Articles MOC.md` after every new article (newest first, under Published or Drafts)
- **Confluence is legacy** — historical reference only. Do not publish new articles there.

### 5. Social Posts Subpage (optional, per Miguel request)
- If Miguel asks for social posts, create a `YYYY-MM-DD <Title> - Posts.md` file in the same directory
- Content structure:
  ```
  ## LinkedIn
  <full narrative post with hashtags and article link>

  ---

  ## Twitter / X
  <single punchy post with hook and article link>
  ```
- **Twitter/X rule (confirmed 2026-04-16):** Single post format, NOT a thread. Write one punchy statement covering hook + article link. No multi-tweet threads unless Miguel explicitly asks.
- LinkedIn: full narrative, 3-5 hashtags, platform-appropriate tone

---

## Image Generation Reference

| Provider | Model | Aspect Ratio Support | Notes |
|----------|-------|----------------------|-------|
| Gemini (default) | imagen-4.0-generate-001 | 1:1, 9:16, 16:9, 4:3, 3:4 | Use 16:9 for articles. No 3:2. |
| OpenAI | gpt-image-1 | 1024x1024, 1536x1024, 1024x1536 | Billing limit can block. Fallback only. |

---

## Confluence Space Map

| Space | Parent ID | Purpose | Rule |
|-------|-----------|---------|------|
| Research | 164315 | Vader's raw research | READ ONLY. Never write here. |
| Articles | 99026 | Published articles | Write here. `confluence_create_page` only for new articles. |

# Formats

Seed: Article production workflow (steps 1-5, Obsidian publishing), image generation reference, social post rules
