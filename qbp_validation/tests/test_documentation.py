"""Offline documentation integrity checks; no quantum backend is required."""
from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})(.*)$")
INLINE_LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*(<[^>\n]*>|[^\s)]+)(?:\s+[^)\n]*)?\)")
REFERENCE_LINK = re.compile(r"^\s{0,3}\[[^\]\n]+\]:\s*(<[^>\n]*>|\S+)", re.MULTILINE)


def markdown_errors(root: Path) -> list[str]:
    """Check UTF-8, controls, fences, and local *file* link targets.

    This deliberately does not fetch external links or validate heading fragments.
    Link-shaped examples in fenced blocks and inline code are ignored.
    """
    root = root.resolve()
    errors: list[str] = []
    paths = sorted(root.rglob("*.md"))
    for path in paths:
        rel = path.relative_to(root)
        if any(part.startswith(".") or part == "__pycache__" for part in rel.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError) as exc:
            errors.append(f"{rel}: unreadable UTF-8: {exc}")
            continue
        for number, line in enumerate(text.split("\n"), 1):
            bad = sorted({ord(c) for c in line if
                          (ord(c) < 32 and c not in "\t\r") or
                          127 <= ord(c) < 160 or c == "\ufffd"})
            if bad:
                errors.append(f"{rel}:{number}: invalid characters {bad}")
        visible: list[str] = []
        opened: tuple[str, int] | None = None
        for line in text.splitlines():
            match = FENCE.match(line)
            if match:
                marker, tail = match.groups()
                if opened is None:
                    opened = (marker[0], len(marker))
                elif marker[0] == opened[0] and len(marker) >= opened[1] and not tail.strip():
                    opened = None
                visible.append("")
            else:
                visible.append(line if opened is None else "")
        if opened is not None:
            errors.append(f"{rel}: unclosed fenced block")
        prose = "\n".join(visible)
        prose = re.sub(r"(`+)[^`\n]*\1", "", prose)
        targets = [m.group(1) for m in INLINE_LINK.finditer(prose)]
        targets += [m.group(1) for m in REFERENCE_LINK.finditer(prose)]
        for target in targets:
            parsed = urlsplit(target.strip("<>"))
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            name = unquote(parsed.path)
            candidate = ((root / name.lstrip("/")) if name.startswith("/")
                         else (path.parent / name)).resolve()
            if not candidate.is_relative_to(root):
                errors.append(f"{rel}: local link escapes repository: {target}")
            elif not candidate.exists():
                errors.append(f"{rel}: missing local link target: {target}")
    return errors


class DocumentationTests(unittest.TestCase):
    def test_repository_markdown(self) -> None:
        self.assertTrue((ROOT / "README.md").is_file())
        errors = markdown_errors(ROOT)
        self.assertEqual(errors, [], "\n".join(errors))

    def test_claim_map_has_one_scope_and_unique_audit_rows(self) -> None:
        text = (ROOT / "docs" / "CLAIM_SUPPORT.md").read_text(encoding="utf-8")
        self.assertEqual(text.count("## Scope relative to the first paper"), 1)
        self.assertNotIn("SHATISTICAL_ACCURACY.md", text)
        summary = text.split("## Audit summary\n", 1)[1].split("\n## ", 1)[0]
        rows = [line for line in summary.splitlines() if line.startswith("| ")][1:]
        names = [line.split("|", 2)[1].strip() for line in rows]
        self.assertTrue(names)
        self.assertEqual(len(names), len(set(names)))

    def test_valid_local_links_and_code_examples(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "figure.png").write_bytes(b"fixture")
            (root / "README.md").write_text("# Root\n", encoding="utf-8")
            (root / "docs" / "guide.md").write_text(
                "# Guide\n[parent](../README.md#root)\n![image](/figure.png)\n"
                "[external](https://example.invalid/not-fetched)\n[local](#guide)\n"
                "[ref]: ../README.md\n`[code](missing.md)`\n"
                "```text\n[example](missing.md)\n```\n", encoding="utf-8")
            self.assertEqual(markdown_errors(root), [])

    def test_rejects_controls_and_replacement_characters(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for bad in ("\x01", "\x10", "\x7f", "\x85", "\ufffd"):
                with self.subTest(character=repr(bad)):
                    (root / "README.md").write_text("broken" + bad, encoding="utf-8")
                    self.assertTrue(any("invalid characters" in e for e in markdown_errors(root)))

    def test_rejects_invalid_utf8(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_bytes(b"bad\xff")
            self.assertTrue(any("unreadable UTF-8" in e for e in markdown_errors(root)))

    def test_rejects_missing_inline_and_reference_targets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "[inline](missing.md)\n[ref]: absent.md\n", encoding="utf-8")
            self.assertEqual(sum("missing local link" in e for e in markdown_errors(root)), 2)

    def test_rejects_unclosed_fences_and_escaping_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("[bad](../../elsewhere)\n```\n", encoding="utf-8")
            errors = markdown_errors(root)
            self.assertTrue(any("unclosed" in e for e in errors))
            self.assertTrue(any("escapes" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
