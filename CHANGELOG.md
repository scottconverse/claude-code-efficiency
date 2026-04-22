# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] — 2026-04-22

### Added
- Initial release of the `claude-code-efficiency` skill.
- Eight priority sections covering the mechanisms that move token spend:
  1. Route tool output through MCP sandboxes or subagents
  2. AST-shape reads via `Grep` + targeted `Read` instead of full-file reads
  3. Permission-mode blast-radius matching with explicit guardrails
  4. Scoped permission allowlists (project vs global, reads vs writes)
  5. Effort and thinking tuning
  6. Long-session hygiene (`/clear`, `/compact`, chapter marks)
  7. Prompt discipline (coordinates, conciseness, files over inline output)
  8. Durable instructions via `CLAUDE.md`, memory files, and harness hooks
- Self-audit checklist.
- Explicit anti-pattern list: global shell-alias interceptors, analytics/telemetry in dev tooling, `--no-verify`, `test.skip()`, marketing numbers without methodology, and trust-by-credential-association.
- README, CHANGELOG, CONTRIBUTING, LICENSE, .gitignore, USER-MANUAL, docs/index.html.
- Structural test suite covering frontmatter parse, trigger-word coverage, required mechanisms, and forbidden patterns.

### Security
- Skill content does not recommend any tool that ships analytics or telemetry.
- No hooks installed, no shell aliases rewired, no external binaries required, no network egress.
