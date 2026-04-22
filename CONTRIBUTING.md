# Contributing

Thanks for your interest.

## What this project is

`claude-code-efficiency` is a Claude Code skill — a single markdown file (`SKILL.md`) with YAML frontmatter and a body of instructions. There is no compiled code, no binary to build, no runtime beyond Claude Code itself.

## What changes are welcome

- Corrections to inaccurate claims about Claude Code features (slash commands, permission modes, tool names, etc.) — please cite the authoritative source
- New mechanisms that demonstrably reduce token spend, with a reproducible benchmark
- Improvements to trigger-word coverage in the frontmatter `description` (new phrases users actually say)
- Clarity edits to the body content
- Tests that catch regressions

## What changes are NOT welcome

- Recommendations that install shell-alias rewriters, analytics, telemetry, or hooks the user didn't explicitly request
- Marketing-style "X% savings" claims without reproducible methodology
- Features that require external binaries, network access, or phone-home behavior
- Padding, hedging, or vague advice ("prompt better," "use AI thoughtfully")
- Recommendations to bypass tests, skip verification, or silence warnings

## Development setup

```bash
git clone https://github.com/scottconverse/claude-code-efficiency.git
cd claude-code-efficiency
python tests/test_skill.py
```

Python 3.8 or later is the only dependency, and it's only needed to run the tests. The skill itself is pure markdown.

## Testing

The skill is markdown content, so tests are structural rather than behavioral:

- YAML frontmatter parses correctly
- Required fields (`name`, `description`) exist
- Description contains the documented trigger words
- Body mentions all eight core mechanisms
- Body does not recommend any pattern on the forbidden list
- Body explicitly rejects shell-alias interceptors

Run:

```bash
python tests/test_skill.py
```

All tests must pass before a PR is considered. If you add a new mechanism to the skill, add a corresponding assertion to `test_body_mentions_core_mechanisms`.

## Submitting changes

1. Fork the repo.
2. Create a feature branch: `git checkout -b improve-thing`.
3. Make your changes to `SKILL.md`. Keep edits targeted — don't regenerate the whole file.
4. Update corresponding documentation (see Documentation Sync Rule below).
5. Run tests. All must pass.
6. Update `CHANGELOG.md` under an `[Unreleased]` section.
7. Commit with a message that explains the "why," not just the "what."
8. Open a pull request.

## Documentation Sync Rule

Any change to `SKILL.md` that affects trigger words, recommended mechanisms, or anti-patterns must also update:

- `README.md` — if the overview or feature list changes
- `USER-MANUAL.md` — if behavior changes in a way a non-technical user would notice
- `docs/index.html` — if positioning or headline capabilities change
- `CHANGELOG.md` — every release, no exceptions

Changes without the matching doc updates will be asked to revise before merge.

## Versioning

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** for changes that would break an existing user's expectations (removed trigger words, removed sections, reversed recommendations)
- **MINOR** for new mechanisms, new sections, new trigger words
- **PATCH** for clarifications, typo fixes, or minor rewording that doesn't change meaning

When bumping the version, update it in every location that references it.

## Code of conduct

Be direct. Challenge claims with evidence. Disagree without being unkind. Cite authoritative sources when correcting a feature claim — "I think it's called X" is not a fix.

## License

By contributing, you agree your contributions are licensed under the MIT License (see [LICENSE](LICENSE)).
