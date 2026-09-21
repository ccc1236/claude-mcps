# jev — TypeSafe Jev (System One) MCP server

Exposes TypeSafe's **Jev** model as typed-judgment tools for Claude Code. Jev
returns typed, calibrated decisions (not text), so code can branch on them.

## Tools
| Tool | Primitive | Returns |
|------|-----------|---------|
| `jev_classify(state, options, instructions)` | Choice | `choice`, `probabilities`, `confidence` |
| `jev_check(state, condition)` | Noul | `noul` (0–1 probability the answer is yes) |
| `jev_score(state, dimension, levels)` | Score | `score`, `legend`, `probabilities`, `confidence` |

## Requirements
```bash
pip install -r requirements.txt   # pins mcp<2 (wrapper uses the FastMCP API)
```
> The wrapper targets the MCP SDK **v1** (`mcp.server.fastmcp`). `mcp` 2.x renamed
> `FastMCP`→`MCPServer`, so `mcp<2` is pinned. Also needs `typing_extensions>=4.15`.

## Env (required)
- `TYPESAFE_API_KEY` — your TypeSafe API key. **Never commit this.**
- `TYPESAFE_MODEL` — optional, defaults to `jev-latest`.

## Install (user scope = available in all sessions)
```bash
claude mcp add -s user jev --env TYPESAFE_API_KEY=YOUR_KEY -- python C:\Users\HakeemSese\claude-ws\mcp\jev\jev_mcp.py
```
Reload Claude Code afterward. Remove/replace anytime: `claude mcp remove jev`
(swap for an official TypeSafe MCP if one ships).

## Usage example

Once installed, Claude calls the tools directly. A `jev_classify` call:

```json
{
  "state": "Player joined an active NBA roster mid-season after the cache was built; user has not clicked Refresh.",
  "instructions": "Classify this situation for triage.",
  "options": {
    "known_limitation": "Documented expected behavior, not a bug",
    "bug": "A defect that violates intended behavior",
    "feature_request": "A request for new capability",
    "needs_investigation": "Unclear, requires more information"
  }
}
```

Returns a typed decision with a probability distribution and a confidence:

```json
{
  "type": "choice",
  "choice": "known_limitation",
  "confidence": 0.71,
  "probabilities": {
    "known_limitation": 0.78, "bug": 0.14,
    "needs_investigation": 0.06, "feature_request": 0.02
  }
}
```

Gate on `confidence` (e.g. act automatically above ~0.9, review in the middle,
escalate below ~0.5). `jev_check` returns `{ "noul": 0.0..1.0 }` (probability the
condition is yes); `jev_score` returns a `score` plus a `legend` for the levels.

## Scope & notes
- Not a coding assistant — use for high-volume / confidence-gated classify,
  check, score inside pipelines, not one-off chat judgments.
- Default TypeSafe data retention is non-zero (ZDR is enterprise-only) — keep
  sensitive data out.
