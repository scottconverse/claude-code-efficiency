"""Structural tests for the claude-code-efficiency skill.

A skill is markdown content, not executable code. These tests verify the
skill file is structurally valid, its frontmatter parses, its description
contains the trigger words users are expected to say, its body covers the
documented mechanisms, and it does not recommend any pattern on the
forbidden list.

Run directly: `python tests/test_skill.py`.
No external dependencies — stdlib only.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SKILL_PATH = Path(__file__).parent.parent / "SKILL.md"

REQUIRED_TRIGGERS = [
    "save tokens",
    "reduce context",
    "be concise",
    "permission mode",
    "effort level",
    "compaction",
]

REQUIRED_MECHANISMS = [
    "mcp",
    "subagent",
    "grep",
    "permission mode",
    "allowlist",
    "effort",
    "/clear",
    "/compact",
    "claude.md",
]

FORBIDDEN_RECOMMENDATIONS = [
    ("install", "posthog"),
    ("install", "sentry"),
    ("enable", "analytics"),
    ("recommend", "shell alias"),
]


def _split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Return (frontmatter_dict, body). Raises on malformed frontmatter."""
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter (---)")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("SKILL.md frontmatter is not closed with ---")
    fm_block = text[4:end]
    body = text[end + 5 :]
    fm: dict[str, str] = {}
    current_key: str | None = None
    current_val: list[str] = []
    for line in fm_block.split("\n"):
        match = re.match(r"^([a-zA-Z_][a-zA-Z0-9_-]*):\s*(.*)$", line)
        if match:
            if current_key is not None:
                fm[current_key] = " ".join(current_val).strip()
            current_key = match.group(1)
            current_val = [match.group(2)]
        else:
            if current_key is not None:
                current_val.append(line.strip())
    if current_key is not None:
        fm[current_key] = " ".join(current_val).strip()
    return fm, body


def test_skill_file_exists() -> None:
    assert SKILL_PATH.exists(), f"SKILL.md not found at {SKILL_PATH}"


def test_frontmatter_parses() -> None:
    text = SKILL_PATH.read_text(encoding="utf-8")
    fm, _ = _split_frontmatter(text)
    assert "name" in fm, "frontmatter missing 'name' field"
    assert "description" in fm, "frontmatter missing 'description' field"
    assert fm["name"] == "claude-code-efficiency", (
        f"skill name should be 'claude-code-efficiency', got {fm['name']!r}"
    )


def test_description_contains_trigger_words() -> None:
    text = SKILL_PATH.read_text(encoding="utf-8")
    fm, _ = _split_frontmatter(text)
    description = fm["description"].lower()
    missing = [t for t in REQUIRED_TRIGGERS if t.lower() not in description]
    assert not missing, f"trigger words missing from description: {missing}"


def test_body_mentions_core_mechanisms() -> None:
    """The core mechanisms must all appear in the body."""
    text = SKILL_PATH.read_text(encoding="utf-8")
    _, body = _split_frontmatter(text)
    body_lower = body.lower()
    missing = [m for m in REQUIRED_MECHANISMS if m.lower() not in body_lower]
    assert not missing, f"body missing core mechanisms: {missing}"


def test_no_forbidden_recommendations() -> None:
    """Scan for recommending verbs near forbidden terms.

    Heuristic: if a forbidden term appears and a recommending verb appears
    within 40 characters before it, and no negation word ('not', 'never',
    'don't', 'do not') appears in that window, flag it.
    """
    text = SKILL_PATH.read_text(encoding="utf-8")
    _, body = _split_frontmatter(text)
    body_lower = body.lower()
    failures = []
    negations = ("not", "never", "don't", "do not", "avoid", "reject")
    for verb, term in FORBIDDEN_RECOMMENDATIONS:
        for match in re.finditer(re.escape(term), body_lower):
            start = max(0, match.start() - 40)
            window = body_lower[start : match.start()]
            if verb in window and not any(n in window for n in negations):
                failures.append(
                    f"possible recommendation of {term!r} (verb={verb!r}) at offset {match.start()}"
                )
    assert not failures, f"forbidden recommendations detected: {failures}"


def test_explicitly_rejects_shell_alias_approach() -> None:
    """The skill must warn against global shell alias interceptors."""
    text = SKILL_PATH.read_text(encoding="utf-8")
    _, body = _split_frontmatter(text)
    body_lower = body.lower()
    assert "shell" in body_lower and "alias" in body_lower, (
        "skill should explicitly address shell aliases"
    )
    has_negation = (
        "do not install" in body_lower
        or "don't install" in body_lower
        or "never install" in body_lower
    )
    assert has_negation, "skill should explicitly reject installing shell alias interceptors"


def test_body_has_self_audit_checklist() -> None:
    """A self-audit or checklist section must be present."""
    text = SKILL_PATH.read_text(encoding="utf-8")
    _, body = _split_frontmatter(text)
    body_lower = body.lower()
    assert "self-audit" in body_lower or "checklist" in body_lower, (
        "skill should include a self-audit or checklist section"
    )


def main() -> int:
    tests = [
        test_skill_file_exists,
        test_frontmatter_parses,
        test_description_contains_trigger_words,
        test_body_mentions_core_mechanisms,
        test_no_forbidden_recommendations,
        test_explicitly_rejects_shell_alias_approach,
        test_body_has_self_audit_checklist,
    ]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
        except AssertionError as e:
            print(f"FAIL  {t.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"ERROR {t.__name__}: {type(e).__name__}: {e}")
            failed += 1
    total = len(tests)
    print(f"\n{total - failed}/{total} tests passed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
