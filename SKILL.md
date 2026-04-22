---
name: claude-code-efficiency
description: Use when a Claude Code session is long, tool output is large, token-burn is a concern, or the user says "save tokens", "reduce context", "be concise", "speed this up", "stop wasting tokens", "this is expensive", or asks about permission modes, allowlists, effort levels, compaction, or context engineering. Covers the legitimate mechanisms that actually move the needle — MCP-sandboxed tool output, subagent context isolation, AST-shape reads, artifact-to-file patterns, permission-mode blast-radius matching, allowlist scoping, effort tuning, long-session hygiene, and prompt discipline. Explicitly excludes global shell-alias intercepts, analytics/telemetry, silent hooks, and marketing numbers without methodology.
---

# Claude Code Efficiency

The mechanisms that actually reduce token burn and keep long sessions healthy, ranked by leverage. Mechanism names current as of 2026-04. If a slash command or named mode doesn't exist in the current Claude Code version, fall back to the underlying primitive noted with it.

**Constraint for every recommendation in this skill: no global shell-alias intercepts, no analytics/telemetry, no hidden hooks, no pipes through third-party services, no "install this binary that rewrites your stdout." Every mechanism below is either native to Claude Code, an explicit MCP server the agent calls by name, or an edit to a config file the user owns.**

---

## Priority 1 — Keep raw tool output out of the main context window

This is the single highest-leverage move. Most "token burn" is raw command output piling into the transcript and getting re-read on every turn.

**Route large commands through a sandboxed MCP server.** If `context-mode` tools are loaded (`ctx_batch_execute`, `ctx_execute`, `ctx_execute_file`, `ctx_search`, `ctx_fetch_and_index`), use them instead of Bash for anything producing more than ~20 lines:

- Replace `cat large.log | grep ERROR` with `ctx_execute(language:"shell", code:"grep ERROR large.log")`. Output stays in the sandbox; only the summary returns.
- Replace `curl url | jq ...` with `ctx_fetch_and_index` — fetches, indexes, queryable afterward.
- For several questions against the same dataset: one `ctx_batch_execute` call with multiple queries beats N separate Bash greps.

**Write artifacts to files, not inline.** Plans, configs, generated code, reports, long lists — `Write` them to a file and tell the user the path. A 2000-line artifact returned in chat costs 2000 lines of context on every subsequent turn. A file path costs one line.

**Use subagents (`Agent` tool) for isolated research.** A subagent searches a large codebase, reads dozens of files, and returns a 200-word summary. The parent session never sees the raw reads. Rule of thumb: more than 3 rounds of Glob/Grep/Read → dispatch an `Explore` or `general-purpose` subagent instead.

**Guardrail:** if you catch yourself about to `cat` a log, `curl` a JSON response, or `Read` a file over 500 lines into main context, stop. Route it.

---

## Priority 2 — AST-shape reads, not full-file reads

Don't `Read` an entire source file when you need its shape. Get the outline first, then read the specific lines you need to edit.

- `Grep pattern:"^(export |async |function |class |def |impl |fn )" output_mode:"content"` returns declarations only.
- `Grep pattern:"^#+\s" path:file.md` returns the markdown header outline.
- `Grep pattern:"^(describe|it|test)\(" path:spec.ts` returns the test structure.
- Then `Read file_path:... offset:N limit:M` for just the region you'll edit.

This captures ~80% of what AST-skeletonization tools (LeanCTX, `ctags`, tree-sitter-based readers) provide, with zero install footprint and nothing rewriting your shell.

**Do not install global shell-alias interceptors** that rewrite `git`/`npm`/`cargo` stdout to "compress" it. They are invasive, hard to debug when they misbehave, pipe your command output through third-party logic, and tend to ship telemetry on their marketing sites. The `Grep`-shape + targeted-`Read` pattern is the clean equivalent.

---

## Priority 3 — Match permission mode to blast radius

Claude Code permission modes (current names; check `/help` if your version differs):

- **Plan mode** — read-only, no edits, no shell. Use for exploration, code review, and planning. Zero blast radius.
- **Default** — prompts on each risky action. Use this in your main checkout when you have uncommitted work.
- **Accept-edits** — auto-approves file edits but still prompts on shell. Reasonable inside a worktree.
- **Bypass-permissions / auto mode** — minimal prompts. Use **only** in a fresh worktree or throwaway sandbox.

Recent Claude Code versions ship a per-command safety classifier that auto-approves commands it classifies as safe. This is a convenience, not a guarantee. A "safe" classification from an automated check is never a substitute for a blast-radius check on your part.

**Never run auto/bypass mode over a checkout with any of the following:**
- Uncommitted changes you care about
- Live credentials in env (`.env`, shell exports, keychain bridges)
- Write access to shared infrastructure (prod DBs, deploy pipelines, published registries)
- A thin or empty `.gitignore`

When in doubt: `git worktree add ../sandbox` and run bypass mode there.

---

## Priority 4 — Build a scoped permission allowlist once

If the same prompts keep interrupting flow, invest 60 seconds once:

- Invoke the `less-permission-prompts` skill (slash name varies: `/less-permission-prompts` or `/fewer-permission-prompts`). It scans the transcript for repeated safe Bash/MCP calls and proposes entries for `settings.json`.
- **Scope matters more than the list itself.** Project-local (`.claude/settings.json`) for project-specific tools and anything that writes. Global (`~/.claude/settings.json`) only for genuinely universal, read-only commands: `git status`, `git log`, `git diff`, `ls`, `pwd`, `which`.
- **Never allowlist write operations globally.** `Bash(git push *)` at global scope means every project in every future session can push without asking.
- **Never allowlist destructive operations at all.** `rm -rf`, `git reset --hard`, `git push --force`, DROP — these should always prompt. The friction is the point.

---

## Priority 5 — Effort / thinking tuning

If the model is giving shallow answers on a hard problem, raise the effort level rather than reprompting three times. Each reprompt costs a full context read; one higher-effort pass is usually cheaper end-to-end.

Names vary by version — numeric thinking budgets in earlier releases, named tiers (low / high / x-high / max, or similar) in newer ones. The rule is the same: raise it when the problem is genuinely hard, drop it for boilerplate.

**Model choice is orthogonal to effort.** Sonnet-at-high and Opus-at-low are different trade-offs, not the same thing at different prices. Match model tier to intelligence need, match effort tier to problem depth, treat them independently.

**Max effort costs latency, not just tokens.** For interactive coding where you need to iterate, "fast answer you can correct" often beats "perfect answer you wait four minutes for."

---

## Priority 6 — Long-session hygiene

Long sessions compound: every turn re-processes the full transcript. Three tools:

- **`/clear`** — nuke the conversation and start fresh. Use when switching to unrelated work.
- **`/compact`** — summarize history in place, keep working. Use when the transcript is getting heavy but you need continuity.
- **Chapter marks** (`mcp__ccd_session__mark_chapter` if available) — make long sessions navigable and give compaction better boundaries. Mark at genuine phase transitions: exploration → implementation, implementation → verification, fix → new feature.

When kicking off a long-running task (test suite, build, scan), spawn it as a background subagent or `run_in_background` Bash call. Don't block the main session — you're paying for the full transcript of wait time.

---

## Priority 7 — Prompt discipline — the real levers

Most "prompting tips" are noise. These four actually change token spend:

- **Be specific with coordinates.** "Fix the auth bug" reprompts three times. "In `src/auth/login.ts:42`, the JWT expiry check compares `>` instead of `<` — fix it" runs once. Coordinates > descriptions.
- **Say "be concise"** when you don't need the full narration. Modern Claude adjusts response length based on this signal. Real lever, costs nothing.
- **Ask for files, not chat text** for anything over ~50 lines. "Write this to `plan.md`" beats "print the plan."
- **Don't paste large blobs.** If Claude needs to see a file, give it the path. It can read.

Dead weight that expands input without improving output: "please," "if you could," "make sure you really carefully," "I was wondering if maybe you could possibly." Cut them.

---

## Priority 8 — Durable instructions over repeated reminders

If you find yourself saying "remember to X" every session, you're paying for that reminder on every turn. Move it:

- **`CLAUDE.md` (project root)** — project-specific rules. Loaded into every session for that project.
- **`~/.claude/CLAUDE.md`** — global rules. Loaded into every session everywhere.
- **Memory files** — per-topic facts the model recalls via auto-memory (the `memory/` directory).
- **Hooks in `settings.json`** — for automated behaviors the harness should enforce. The harness runs these; they cost nothing in context. Use the `update-config` skill to wire them cleanly.

One `CLAUDE.md` line replaces a thousand in-session reminders.

---

## What NOT to do — patterns that look helpful but aren't

- **Global shell-alias rewriters** (LeanCTX-style `git`/`npm`/`cargo` intercepts). Invasive, hard to debug, pipe output through third-party logic, often ship telemetry on the project's marketing surface. If you want output compression, use an MCP server the agent calls **by name** — don't hook the shell behind the user's back.
- **Analytics / telemetry in "productivity" tooling.** A dev tool whose marketing site embeds PostHog or Sentry has a conflict of interest: it profits from knowing what you do. Block network egress and verify "zero telemetry" claims before trusting them.
- **Marketing numbers without methodology.** "99% token savings" / "$315/week saved" screenshots without a reproducible benchmark are marketing, not evidence. Run the vendor's own benchmark tool against your actual repo before believing the pitch. If they don't ship a benchmark, that itself is a signal.
- **`--no-verify` and hook bypasses.** If a pre-commit hook is in the way, fix the underlying issue or remove the hook deliberately. Bypassing hides problems that resurface later at worse times.
- **`test.skip()` and equivalents.** A skipped test lies to the suite — it reports "passing" while proving nothing. Fix the test, fix the design, or delete the test entirely. Never skip.
- **Installing things on the "guy who built X said so" principle.** Boris built Claude Code (the harness) — that credibility does not transfer to unrelated products citing him. Yves built LeanCTX — that's a separate claim to evaluate separately. Check what the code actually does before installing.

---

## Self-audit — run before declaring a session "efficient"

- [ ] Any raw tool output over ~20 lines went through an MCP server or subagent, not straight into main context
- [ ] Artifacts over ~50 lines were written to files, not returned inline
- [ ] Permission mode matches the blast radius of what's happening (auto mode only in a sandbox/worktree)
- [ ] Allowlist is scoped correctly — project for writes, global only for universal reads
- [ ] No global shell aliases were installed, no analytics added, no silent hooks wired
- [ ] Effort level matches task difficulty (not cranked for trivial, not starved for hard)
- [ ] Long session has been compacted or cleared at natural phase boundaries
- [ ] Recurring reminders have moved to `CLAUDE.md` / memory / hooks, not re-asserted each turn
- [ ] Any vendor productivity claim was verified with a reproducible benchmark against the actual workload, not trusted from a screenshot

---

## Source credit

This skill integrates the legitimate, verifiable portions of three sources:
1. Boris Cherny's Claude Code usage tips (permission modes, allowlist scans, effort levels, concise prompting) — kept where the mechanism is native to Claude Code, dropped where the claim couldn't be verified against the harness.
2. The LeanCTX approach (output compression, AST-shape reads, artifact externalization) — translated into native Claude Code primitives (`Grep`-shape, `Write` to file, subagents, context-mode MCP) instead of shell-alias intercepts.
3. Native Claude Code mechanisms Boris's post didn't cover: `CLAUDE.md`, subagents, chapter marks, hooks, memory files, `/clear` vs `/compact`.

No portion of this skill recommends installing software that rewrites your shell, ships analytics, or hides its behavior behind aliases.
