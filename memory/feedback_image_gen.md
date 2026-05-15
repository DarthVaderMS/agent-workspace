---
name: Use native OpenClaw image generation
description: Image generation workflow — use native tool, not external scripts
type: feedback
---

**Use OpenClaw's native `mcp__openclaw__image_generate` tool for all image generation.**

**Why:** Native tool is the platform standard. Cleaner, simpler, avoids external script dependencies.

**How to apply:** When generating images for articles, use the native tool directly instead of nano-banana or other external scripts. Check available providers/models with `action="list"` first if unsure what's configured.

**Directive:** Miguel (2026-04-23) — explicit instruction to switch from nano-banana to native OpenClaw image generation.
