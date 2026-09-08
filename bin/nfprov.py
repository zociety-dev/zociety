#!/usr/bin/env python3
"""nfprov.py -- zociety's `mark-added` front end for the nerd-fonts provenance tool.

Implements only the `mark-added` subcommand described in
delano/nerd-fonts#15, so zociety can demo provenance marking over its own
git history. Everything about the *encoding* is delegated to the verbatim
vendored copy of upstream's reference tool in bin/nfprov-upstream.py (with
bin/nfprov-mapping.json), so the output is byte-compatible with what the
fork's P+ fonts render and what `nfprov-upstream.py inspect` reports.

    nfprov.py mark-added --base BLOB_OR_FILE [--mode=vs|pua] FILE
    nfprov.py --selftest

Marking rule (from the issue): compare base and current at line level.
Within each changed line, mark only the span between the common prefix and
common suffix of the old and new line -- a character-level diff is
deliberately not used, since it would leave shared letters inside a
rewritten sentence unmarked. Marking is idempotent and whitespace is never
marked. Only .md, .mdx, .txt, .rst are eligible; other files pass through
unchanged.

Encoding (upstream src/glyphs/provenance/README.md, mapping.json v1):
  - vs:  every non-whitespace grapheme cluster in a marked span is followed
         by U+E0101 (VARIATION SELECTOR-18, the "ai" selector). One selector
         per cluster, placed after combining marks / emoji sequences.
  - pua: single-code-point bases listed in mapping.json's `pua` table
         (roughly U+0021..U+00FF) are *replaced* by U+100000 + codepoint,
         a plane-16 PUA character the fonts carry as an AI-styled glyph.
         Bases outside the table keep the VS encoding. There are no span
         sentinels in either mode.
"""
import argparse
import difflib
import importlib.util
import sys
from functools import lru_cache
from pathlib import Path

PROSE_SUFFIXES = {".md", ".mdx", ".txt", ".rst"}
UPSTREAM_PATH = Path(__file__).resolve().with_name("nfprov-upstream.py")


@lru_cache(maxsize=1)
def upstream():
    """Import bin/nfprov-upstream.py as a module (it has no importable name)."""
    spec = importlib.util.spec_from_file_location("nfprov_upstream", UPSTREAM_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {UPSTREAM_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.dont_write_bytecode = True  # keep bin/ free of __pycache__
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def tables():
    """(selectors, pua2base, base2pua) from the vendored mapping.json."""
    _, selectors, pua2base, base2pua = upstream().load_mapping()
    return selectors, pua2base, base2pua


def is_prose(filename: str) -> bool:
    return Path(filename).suffix.lower() in PROSE_SUFFIXES


def common_prefix_len(a: str, b: str) -> int:
    n = min(len(a), len(b))
    i = 0
    while i < n and a[i] == b[i]:
        i += 1
    return i


def common_suffix_len(a: str, b: str, prefix_len: int) -> int:
    n = min(len(a), len(b)) - prefix_len
    i = 0
    while i < n and a[len(a) - 1 - i] == b[len(b) - 1 - i]:
        i += 1
    return i


def mark_span(text: str, mode: str) -> str:
    """Encode a span as AI-authored via upstream's do_mark.

    do_mark already skips whitespace, leaves existing selectors / PUA
    characters alone, and applies the per-mode encoding, so no trimming or
    sentinel handling is needed here.
    """
    if not text:
        return text
    selectors, pua2base, base2pua = tables()
    return upstream().do_mark(text, "ai", mode, selectors, pua2base, base2pua)


def mark_line_diff(old: str, new: str, mode: str) -> str:
    """Mark only the span between common prefix/suffix of old vs new."""
    if old == new:
        return new
    prefix_len = common_prefix_len(old, new)
    suffix_len = common_suffix_len(old, new, prefix_len)
    # Guard against prefix/suffix overlap on short strings.
    suffix_len = min(suffix_len, len(new) - prefix_len)
    head = new[:prefix_len]
    middle = new[prefix_len: len(new) - suffix_len]
    tail = new[len(new) - suffix_len:] if suffix_len else ""
    return head + mark_span(middle, mode) + tail


def _split_body(line: str) -> tuple[str, str]:
    body = line.splitlines()[0] if line.splitlines() else line
    return body, line[len(body):]


def mark_added(base_text: str, current_text: str, mode: str) -> str:
    base_lines = base_text.splitlines(keepends=True)
    cur_lines = current_text.splitlines(keepends=True)
    sm = difflib.SequenceMatcher(a=base_lines, b=cur_lines, autojunk=False)

    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            out.extend(cur_lines[j1:j2])
        elif tag == "insert":
            for line in cur_lines[j1:j2]:
                body, newline = _split_body(line)
                out.append(mark_span(body, mode) + newline)
        elif tag == "delete":
            continue
        elif tag == "replace":
            old_block = base_lines[i1:i2]
            new_block = cur_lines[j1:j2]
            paired = min(len(old_block), len(new_block))
            for k in range(paired):
                old_body, _ = _split_body(old_block[k])
                new_body, newline = _split_body(new_block[k])
                out.append(mark_line_diff(old_body, new_body, mode) + newline)
            for extra in new_block[paired:]:
                body, newline = _split_body(extra)
                out.append(mark_span(body, mode) + newline)
    return "".join(out)


def process(filename: str, base_text: str, current_text: str, mode: str) -> str:
    """mark-added for one file; non-prose files pass through untouched."""
    if not is_prose(filename):
        return current_text
    return mark_added(base_text, current_text, mode)


def cmd_mark_added(args: argparse.Namespace) -> int:
    up = upstream()
    current_text = up.read_input(args.file)

    if args.base in ("", "-", None):
        base_text = ""
    else:
        base_path = Path(args.base)
        base_text = up.read_input(args.base) if base_path.exists() else args.base

    up.write_output(process(args.file, base_text, current_text, args.mode), None)
    return 0


def strip_marks(text: str) -> str:
    selectors, pua2base, _ = tables()
    return upstream().do_strip(text, selectors, pua2base)


def inspect_counts(text: str) -> dict[str, int]:
    """Parse upstream `inspect` output into {key: count}."""
    selectors, pua2base, _ = tables()
    report = upstream().do_inspect(text, selectors, pua2base)
    counts = {}
    for line in report.splitlines():
        key, _, value = line.partition(": ")
        if value.isdigit():
            counts[key] = int(value)
    return counts


def count_marked_chars(text: str) -> int:
    """AI-marked characters in either encoding, as upstream inspect sees them."""
    counts = inspect_counts(text)
    return counts["ai_vs"] + counts["ai_pua"]


def selftest() -> int:
    selectors, pua2base, base2pua = tables()
    ai = chr(selectors["ai"])
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    def pua(s: str) -> str:
        return "".join(chr(base2pua[ord(c)]) if not c.isspace() else c for c in s)

    check(ai == "\U000E0101", "ai selector must be U+E0101 (VARIATION SELECTOR-18)")
    check(base2pua[ord("a")] == 0x100061, "PUA_AI(cp) must be 0x100000 + cp")

    # (name, base, current, vs_expected, pua_expected, ai_count, human_count)
    cases = [
        (
            "whole-file add",
            "",
            "hello world\n",
            "h" + ai + "e" + ai + "l" + ai + "l" + ai + "o" + ai + " "
            + "w" + ai + "o" + ai + "r" + ai + "l" + ai + "d" + ai + "\n",
            pua("hello") + " " + pua("world") + "\n",
            10, 0,
        ),
        (
            "single-word change",
            "the cat sat\n",
            "the dog sat\n",
            "the d" + ai + "o" + ai + "g" + ai + " sat\n",
            "the " + pua("dog") + " sat\n",
            3, 6,
        ),
        (
            # Common prefix/suffix are both empty, so the whole line
            # (including the unchanged middle word) is marked -- by design.
            "two changes on one line",
            "alpha beta gamma\n",
            "ALPHA beta GAMMA\n",
            "".join(c + ai if not c.isspace() else c for c in "ALPHA beta GAMMA\n"),
            pua("ALPHA") + " " + pua("beta") + " " + pua("GAMMA") + "\n",
            14, 0,
        ),
        (
            "unchanged file",
            "no changes here\n",
            "no changes here\n",
            "no changes here\n",
            "no changes here\n",
            0, 13,
        ),
        (
            "edit inside a multi-line file",
            "# Title\n\nfirst para\nsecond para\n",
            "# Title\n\nfirst para edited\nsecond para\n",
            "# Title\n\nfirst para e" + ai + "d" + ai + "i" + ai + "t" + ai
            + "e" + ai + "d" + ai + "\nsecond para\n",
            "# Title\n\nfirst para " + pua("edited") + "\nsecond para\n",
            6, 25,
        ),
    ]

    for name, base, current, vs_expected, pua_expected, n_ai, n_human in cases:
        for mode, expected in (("vs", vs_expected), ("pua", pua_expected)):
            marked = mark_added(base, current, mode)
            check(marked == expected, f"{name} ({mode}): got {marked!r}")
            check(strip_marks(marked) == current, f"{name} ({mode}): strip != current")
            check(
                "\U0000E000" not in marked and "\U0000E001" not in marked
                and "︀" not in marked,
                f"{name} ({mode}): legacy placeholder codepoints present",
            )
            counts = inspect_counts(marked)
            key = "ai_vs" if mode == "vs" else "ai_pua"
            other = "ai_pua" if mode == "vs" else "ai_vs"
            check(counts[key] == n_ai, f"{name} ({mode}): inspect {key}={counts[key]} != {n_ai}")
            check(counts[other] == 0, f"{name} ({mode}): inspect {other} should be 0")
            check(
                counts["assumed_human"] == n_human,
                f"{name} ({mode}): inspect assumed_human={counts['assumed_human']} != {n_human}",
            )
            report = upstream().do_inspect(marked, selectors, pua2base)
            check(
                "unrecognised_selectors: -" in report and "unrecognised_pua: -" in report,
                f"{name} ({mode}): inspect saw unrecognised codepoints",
            )
            # Idempotence, two ways: nothing changed since the last pass, and
            # re-marking the marked output against the original base.
            check(mark_added(marked, marked, mode) == marked, f"{name} ({mode}): not idempotent")
            check(mark_added(base, marked, mode) == marked, f"{name} ({mode}): re-mark vs base")

    # Whitespace is never marked, in either mode.
    for mode in ("vs", "pua"):
        marked = mark_added("", "a\tb  c\r\n", mode)
        check(
            marked.count("\t") == 1 and marked.count("  ") == 1 and marked.endswith("\r\n"),
            f"whitespace ({mode}): whitespace altered: {marked!r}",
        )
        check(inspect_counts(marked)["whitespace"] == 5, f"whitespace ({mode}): count")

    # pua mode: bases outside the mapping table fall back to VS encoding.
    hybrid = mark_added("", "a日\n", "pua")
    check(hybrid == chr(base2pua[ord("a")]) + "日" + ai + "\n", f"pua fallback: {hybrid!r}")
    check(count_marked_chars(hybrid) == 2, "pua fallback: inspect count")

    # Non-prose files pass through unchanged regardless of mode.
    for mode in ("vs", "pua"):
        check(
            process("script.sh", "echo hi\n", "echo hello\n", mode) == "echo hello\n",
            f"non-prose ({mode}): passthrough broken",
        )
    check(process("notes.MD", "", "x\n", "vs") == "x" + ai + "\n", "prose suffix case-insensitive")

    if failures:
        for f in failures:
            print(f"FAIL: {f}", file=sys.stderr)
        return 1

    print(f"ok: nfprov selftest passed ({len(cases)} diff cases x 2 modes + edge cases)")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="nfprov.py")
    parser.add_argument("--selftest", action="store_true")
    sub = parser.add_subparsers(dest="command")

    mark_added_p = sub.add_parser("mark-added")
    mark_added_p.add_argument("--base", default="")
    mark_added_p.add_argument("--mode", choices=("vs", "pua"), default="vs")
    mark_added_p.add_argument("file")

    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()
    if args.command == "mark-added":
        return cmd_mark_added(args)

    parser.print_help(sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
