# claude-code-efficiency

A [Claude Code](https://claude.com/claude-code) skill that teaches the model to handle long, expensive sessions without installing shell-alias rewriters, analytics, or hidden hooks.

## What this is

When you install this skill, Claude detects session-efficiency concerns (long transcripts, token-burn, allowlist questions, context-engineering topics) and auto-loads a structured set of instructions covering the mechanisms that actually reduce token spend.

The skill is a single markdown file with YAML frontmatter. No binary. No network access. No dependencies beyond Claude Code itself.

## What it does

Loads eight priority-ranked practices into Claude's working guidance:

1. Route large tool output through MCP sandboxes or subagents instead of main context
2. Use `Grep`-shape + targeted `Read` instead of full-file reads (native AST skeletonization)
3. Match permission modes to blast radius, with explicit guardrails against auto-approving in risky checkouts
4. Scope permission allowlists correctly (project vs global, reads vs writes)
5. Tune effort/thinking levels based on problem depth
6. Clean long sessions with `/clear`, `/compact`, and chapter marks
7. Prompt with coordinates, not descriptions — files over inline output
8. Move recurring reminders to `CLAUDE.md` and harness hooks

Plus an explicit anti-pattern list: global shell interceptors, telemetry-in-dev-tooling, `--no-verify`, `test.skip()`, and trust-by-credential-association.

## Quick start

**Install:**

```bash
cd ~/.claude/skills
git clone https://github.com/scottconverse/claude-code-efficiency.git
```

Or copy `SKILL.md` into `~/.claude/skills/claude-code-efficiency/SKILL.md` directly.

**Verify:**

Start a new Claude Code session. Run `/help` — `claude-code-efficiency` should appear in the available skills list.

**Use:**

The skill auto-triggers on phrases like "save tokens," "reduce context," "be concise," or can be invoked by name via the `Skill` tool.

## Requirements

- Claude Code 2.x, or compatible harness (Copilot CLI, Codex, Gemini CLI) with skill support
- Python 3.8+ only if you want to run the structural tests
- No other dependencies

## Configuration

None. The skill is a single markdown file (`SKILL.md`) with YAML frontmatter.

## Repository layout

```
claude-code-efficiency/
├── SKILL.md            The skill itself — frontmatter + 8 priority sections
├── README.md           You are here
├── CHANGELOG.md        Version history
├── CONTRIBUTING.md     How to propose changes
├── LICENSE             MIT
├── USER-MANUAL.md      Plain-language guide for non-technical users
├── .gitignore
├── docs/
│   └── index.html      GitHub Pages landing page
└── tests/
    └── test_skill.py   Structural validation
```

## Tests

```bash
python tests/test_skill.py
```

Structural tests only — a skill is markdown content, not code. Tests verify:

- YAML frontmatter parses
- Required fields present (`name`, `description`)
- Description contains documented trigger words
- Body mentions every core mechanism
- Body does not recommend any forbidden pattern (shell aliases, telemetry, bypasses)
- Body explicitly rejects shell-alias interceptors

## Design decisions

**Why no installer, no binary, no network?**
Because the mechanisms that actually save tokens in Claude Code are built into the harness (permission modes, MCP servers, subagents, compaction). A skill that teaches the model to use them effectively is strictly additive — it can't fail, can't phone home, can't be exploited. A dev tool that ships a binary with analytics to "save tokens" has a conflict of interest the skill approach doesn't.

**Why not a command-line tool?**
Because the agent is already running in Claude Code. Instructions are the right interface — anything else is a separate runtime to install, version, and trust.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE).
