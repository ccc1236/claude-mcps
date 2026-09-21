# jev - TypeSafe Jev (System One) MCP server

Exposes TypeSafe's **Jev** model as typed-judgment tools for Claude Code. Jev
returns typed, calibrated decisions (not text), so code can branch on them.

## Tools
| Tool | Primitive | Returns |
|------|-----------|---------|
| `jev_classify(state, options, instructions)` | Choice | `choice`, `probabilities`, `confidence` |
| `jev_check(state, condition)` | Noul | `noul` (0-1 probability the answer is yes) |
| `jev_score(state, dimension, levels)` | Score | `score`, `legend`, `probabilities`, `confidence` |

## Requirements
```bash
pip install -r requirements.txt   # pins mcp<2 (wrapper uses the FastMCP API)
```
> The wrapper targets the MCP SDK **v1** (`mcp.server.fastmcp`). `mcp` 2.x renamed
> `FastMCP`→`MCPServer`, so `mcp<2` is pinned. Also needs `typing_extensions>=4.15`.

## Env (required)
- `TYPESAFE_API_KEY` - your TypeSafe API key. **Never commit this.**
- `TYPESAFE_MODEL` - optional, defaults to `jev-latest`.

## Install (user scope = available in all sessions)
```bash
claude mcp add -s user jev --env TYPESAFE_API_KEY=YOUR_KEY -- python C:\Users\HakeemSese\claude-ws\mcp\jev\jev_mcp.py
```
Reload Claude Code afterward. Remove/replace anytime: `claude mcp remove jev`
(swap for an official TypeSafe MCP if one ships).

## Scope & notes
- Not a coding assistant - use for high-volume / confidence-gated classify,
  check, score inside pipelines, not one-off chat judgments.
- Default TypeSafe data retention is non-zero (ZDR is enterprise-only) - keep
  sensitive data out.
