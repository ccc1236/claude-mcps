# claude-mcps

Personal [MCP](https://modelcontextprotocol.io) servers for Claude Code —
one subfolder per server, each self-contained with its own README.

## Servers
| Folder | What it does |
|--------|--------------|
| [`jev/`](jev/) | TypeSafe Jev (System One) — typed, calibrated judgment tools (classify / check / score) |

## Layout
```
claude-mcps/
├── <server>/          # one folder per MCP server
│   ├── <server>.py    # the server
│   ├── requirements.txt
│   └── README.md      # its tools, env vars, install
└── .github/workflows/gitleaks.yml
```

## Adding a new server
1. Create `claude-mcps/<name>/` with the server, a `requirements.txt`, and a `README.md`.
2. Register it: `claude mcp add [-s user] <name> --env KEY=VALUE -- <command>`.
3. Commit and push — the scanners below run automatically.

## Secret hygiene
- **Keys come from environment variables only** — never hardcode or commit them.
- `.gitignore` blocks `.env`, `*.key`, `.mcp.json`, etc.
- **Local:** gitleaks pre-commit hook — `pip install pre-commit && pre-commit install`.
- **CI:** `.github/workflows/gitleaks.yml` scans every push and PR server-side.
- GitHub account-wide push protection is also on as a baseline.
