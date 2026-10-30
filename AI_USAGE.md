# AI Usage

The brief allows AI and may review how it was used. Rule followed: **AI drafts or runs → result
checked against the live site or raw evidence → only then used.**

## Tools

| Tool                                   | Used for                                                                    |
| -------------------------------------- | --------------------------------------------------------------------------- |
| Claude Code (Claude Opus)              | Planning, scripts, first drafts, cross-checking documents                   |
| Playwright MCP (pinned in `.mcp.json`) | Let the AI drive Chrome: screenshots, keyboard, accessibility tree, console |
| opencode + Playwright MCP              | Re-ran the §1 journey on 29 Oct                                             |
| Postman · curl                         | API tests and raw responses                                                 |
| Python (no extra packages)             | Catalogue script and self-check                                             |
| Chrome DevTools                        | Manual checks                                                               |

## How each part was checked

| Part              | AI did                                      | Checked by                                                |
| ----------------- | ------------------------------------------- | --------------------------------------------------------- |
| Journey (§1)      | Drove Chrome, took screenshots              | Every screenshot reviewed; test account only; no order    |
| API (§2)          | Wrote Postman tests; curl for raw responses | Postman results compared with curl output                 |
| Technical (§2)    | Read `cart.js`, accessibility tree, console | Source files saved as evidence; each cause checked        |
| Frontend fix (§3) | Wrote the fix and demo; ran before/after    | Screenshots reviewed; cart emptied afterwards             |
| Catalogue (§4)    | Wrote the script and a fault self-check     | 2 products checked by hand; self-check 5/5; timed refresh |
| Write-up (§5–6)   | Drafted documents                           | All 180+ file links checked; numbers cross-checked        |

## AI mistakes caught and fixed

| Mistake                                                | Caught by                                  | Fix                           |
| ------------------------------------------------------ | ------------------------------------------ | ----------------------------- |
| Said the fonts loaded                                  | Doubted it; measured rendered text instead | Fonts don't load → DEF-11     |
| Logged "no maximum quantity" as a defect               | No documented rule exists                  | Withdrawn → IMP-01            |
| Demo screenshot had a hand-added log line              | Reviewing evidence                         | Screenshot retaken            |
| Script counted unreachable pages as "Fail"             | The fault self-check                       | Script fixed                  |
| Claimed arrow keys were tested; stated a guess as fact | Reading the draft against evidence         | Wording corrected             |
| Name check would skip "T-Shirt"                        | Reading the code before running            | Rule simplified               |
| DEF-08 blamed the search field too                     | A screenshot showed the field's focus      | Re-tested; narrowed to button |
| Said the mobile cart total was visible                 | Screenshot showed it cut off               | TR-24 changed; IMP-09 added   |

## Safety

Own test account only · no orders · no load testing (≈ 70 read-only requests, one at a time) · AI
transcripts saved under `%USERPROFILE%\.claude\projects\` and available on request.
