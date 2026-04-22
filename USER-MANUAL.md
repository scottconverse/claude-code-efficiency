# User Manual

This guide is for people who are new to Claude Code, Claude Code skills, or both. No prior technical background is assumed.

## What is Claude Code?

**Claude Code** is a tool from Anthropic that lets you work with Claude (a large language model) while giving it the ability to read, write, and run commands on your computer. You use it to build software, automate tasks, and get work done faster than you could alone.

## What is a skill?

A **skill** is a small file that teaches Claude how to handle a specific kind of task. When you say certain words, the matching skill "wakes up" and Claude uses the instructions in it.

For example: if you say "help me write an Amazon listing," a listing-writing skill wakes up and Claude follows specific guidance about Amazon listings — instead of just giving generic advice.

## What does *this* skill do?

`claude-code-efficiency` wakes up when your Claude Code session is getting long, expensive, or cluttered. It teaches Claude to:

- Keep big command output out of the conversation, so your session stays fast
- Read just the parts of files it needs, not whole files every time
- Match its permission settings to how risky the current task is
- Use the right effort level for the task (not maximum effort on easy things)
- Clean up long sessions before they get sluggish

It also teaches Claude what **not** to do — mainly, don't install tools that quietly intercept your shell commands or send data somewhere.

## Installing

1. Open a terminal on your computer.
2. Run these two lines:

   ```
   cd ~/.claude/skills
   git clone https://github.com/scottconverse/claude-code-efficiency.git
   ```

3. Start a new Claude Code session. The skill is now available.

If you don't have `git` installed, you can also download the files manually from the repository's web page and copy the folder into `~/.claude/skills/`.

## Checking that it worked

Start a Claude Code session and type:

```
/help
```

You should see `claude-code-efficiency` somewhere in the list of available skills.

Or just say something like "this session is getting expensive, help me cut tokens." Claude should respond by invoking the skill.

## What you'll notice when it's working

You won't see the skill instructions themselves — those are internal to Claude. What you'll notice:

- Claude writes long results to files instead of pasting them into the chat
- Claude runs large searches through smaller, targeted tools
- Claude asks before letting itself auto-approve risky commands, and warns you when a checkout is risky
- Claude suggests `/clear` or `/compact` when the session has been going for a while
- Claude challenges dubious efficiency claims instead of just installing whatever you mention

## Troubleshooting

**The skill doesn't appear in `/help`.**
The file is probably not in the right place. Check that `~/.claude/skills/claude-code-efficiency/SKILL.md` exists and that the folder name is exactly `claude-code-efficiency` (no typos, all lowercase, with hyphens).

**Claude doesn't invoke the skill when I expect.**
Skills trigger on specific phrases in their description. Try saying one of these — they're all documented triggers:
- "save tokens"
- "reduce context"
- "be concise"
- "this session is expensive"
- "stop wasting tokens"

**I want to customize what the skill says.**
Open `SKILL.md` in any text editor. The content is human-readable markdown. Edit the sections you want to change. Claude will pick up your version on the next session.

**I want to update to a newer version.**
From inside the skill folder: `git pull`. That's it.

## Frequently asked questions

**Is this safe to install?**
Yes. The skill is a single markdown file with no executable code, no binaries, no network access, and no telemetry. You can read the entire thing before installing — it's only a few pages.

**Does it send my data anywhere?**
No. It contains no network calls of any kind. It's just text that Claude reads.

**Will it slow down Claude Code?**
No. The skill only loads when its trigger words are detected, and even then it adds a small amount of text to Claude's context. The whole point of the skill is to *reduce* context, not expand it.

**Does it work with every Claude Code version?**
It targets Claude Code 2.x. Older versions may not support all the mechanisms described (especially chapter marks and effort levels). The skill falls back gracefully — it recommends the underlying primitive when a specific slash command isn't available.

**Can I use this with Cursor, Copilot CLI, Codex, or Gemini CLI?**
Some of them, partially. The principles apply generally, but specific tool names (`Grep`, `Read`, `ctx_execute`) are Claude Code terms. Skill-loading mechanisms vary across harnesses — check your platform's skill documentation.

## Glossary

- **Claude Code** — Anthropic's command-line tool for working with Claude to build software.
- **Skill** — a file of instructions that Claude follows for specific kinds of tasks.
- **Markdown** — a simple plain-text format for documents. Readable in any text editor.
- **YAML frontmatter** — the block at the top of `SKILL.md` between `---` lines. Tells Claude what the skill is named and when to activate it.
- **Token** — roughly, a chunk of text. Claude charges by how much text it reads and writes. Long conversations mean more tokens and higher cost.
- **Context window** — Claude's working memory for a conversation. Big tool outputs fill it up and slow things down.
- **MCP server** — a helper tool that Claude can call to run commands in a sandbox and return summaries, keeping the raw output out of Claude's memory.
- **Subagent** — a separate Claude session the main one launches for a specific task. Keeps the main conversation clean.
- **Permission mode** — Claude Code's setting for how much it asks before running commands. Ranges from "ask every time" to "run anything without asking."
- **Hook** — a command the Claude Code harness runs automatically at certain events. This skill does *not* install any.
- **Allowlist** — a list of commands Claude is pre-approved to run without asking each time.
- **Blast radius** — how much damage an action could do if it went wrong. Low blast radius: reading a file. High blast radius: deleting a database.

## Getting help

- File an issue: https://github.com/scottconverse/claude-code-efficiency/issues
- Ask a question: https://github.com/scottconverse/claude-code-efficiency/discussions (once enabled)
