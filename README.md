# claude-mcps

Personal MCP servers for Claude Code. One subfolder per server.

## Servers

### `jev/` — TypeSafe Jev (System One)
Exposes TypeSafe's Jev model as typed-judgment tools: `jev_classify` (Choice),
`jev_check` (Noul), `jev_score` (Score). Minimal wrapper — official `mcp` SDK +
stdlib only.

**Env (required):**
- `TYPESAFE_API_KEY` — your TypeSafe API key. **Never commit this.**
- `TYPESAFE_MODEL` — optional, defaults to `jev-latest`.

**Install:**
```bash
pip install mcp
claude mcp add jev --env TYPESAFE_API_KEY=YOUR_KEY -- python /full/path/to/jev/jev_mcp.py
```

**Remove / replace:** `claude mcp remove jev` (swap for an official MCP if one ships).

## Secret hygiene
- Keys come from environment variables only — never hardcode them.
- `.gitignore` blocks `.env`, `*.key`, `.mcp.json`, etc.
- Optional secret scanner: `pip install pre-commit && pre-commit install` (see `.pre-commit-config.yaml`).
