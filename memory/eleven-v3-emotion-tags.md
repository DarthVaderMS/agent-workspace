# ElevenLabs eleven_v3 — Audio Emotion Tags

Embed tags **inline, before the words they affect**. One or two per sentence is enough.

**Emotional states:**
`[excited]` `[nervous]` `[frustrated]` `[sorrowful]` `[calm]` `[tired]` `[confident]`

**Reactions & sounds:**
`[sigh]` `[laughs]` `[gulps]` `[gasps]` `[chuckles]` `[sighs heavily]` `[sigh of relief]`

**Volume & energy:**
`[whispering]` `[shouting]` `[quietly]` `[loudly]`

**Pacing & delivery:**
`[pauses]` `[hesitates]` `[stammers]` `[resigned tone]` `[deadpan]` `[flatly]` `[playfully]`

**Rules:**
- Tags go BEFORE the words they affect, not after
- Multiple tags can stack: `[excited] [loudly]`
- Use `[pauses]` or `...` instead of `<break />` (not supported)
- Avoid overusing — one or two per sentence is enough

**Examples:**
```
[nervous] I found something in the data. [pauses] This changes everything.
[excited] The campaign is live! [cheerfully] Results are already coming in.
[whispering] Don't tell anyone yet — [hesitates] — I'm not sure it's safe to share.
[deadpan] The client asked for 47 revisions. I said yes to all of them.
[tired] I've been on this since midnight. [sigh] It's finally done. [quietly] I think it's good.
```
