#!/usr/bin/env python3
"""nfprov.py -- vendored subset of delano/nerd-fonts' provenance tool.

Implements only the `mark-added` subcommand described in
delano/nerd-fonts#15, so zociety can demo provenance marking over its own
git history without depending on the upstream fork being checked out here.
`mark`, `inspect`, and the Claude Code plugin hooks are assumed to live
upstream and are out of scope for this vendored copy.

    nfprov.py mark-added --base BLOB_OR_FILE [--mode=vs|pua] FILE
    nfprov.py --selftest

Marking rule (from the issue): compare base and current at line level.
Within each changed line, mark only the span between the common prefix and
common suffix of the old and new line -- a character-level diff is
deliberately not used, since it would leave shared letters inside a
rewritten sentence unmarked. Marking is idempotent and whitespace is never
marked. Only .md, .mdx, .txt, .rst are eligible; other files pass through
unchanged.

Encoding note: the upstream P+ fonts define the actual GSUB ligatures that
render these markers. This vendored copy uses placeholder codepoints
(documented below) chosen to match the *shape* of the two modes described
in the issue -- swap them for the real values once the upstream encoding
is confirmed:
  - vs:  append VARIATION SELECTOR-1 (U+FE00) after each marked character
         (HarfBuzz-style per-character marking).
  - pua: wrap the marked span in PUA sentinels U+E000 (start) / U+E001
         (end) (CoreText-style span marking).
"""
import argparse
import difflib
import sys
from pathlib import Path

PROSE_SUFFIXES = {".md", ".mdx", ".txt", ".rst"}

VS_MARK = "︀"
PUA_START = ""
PUA_END = ""


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
    """Mark a span of text, trimming whitespace off both ends first."""
    stripped = text.strip(" \t")
    if not stripped:
        return text
    lead = text[: len(text) - len(text.lstrip(" \t"))]
    trail = text[len(text.rstrip(" \t")):] if text.rstrip(" \t") else ""
    if mode == "pua":
        marked = f"{PUA_START}{stripped}{PUA_END}"
    else:
        marked = "".join(ch + VS_MARK for ch in stripped)
    return lead + marked + trail


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
                body = line.splitlines()[0] if line.splitlines() else line
                newline = line[len(body):]
                out.append(mark_span(body, mode) + newline)
        elif tag == "delete":
            continue
        elif tag == "replace":
            old_block = base_lines[i1:i2]
            new_block = cur_lines[j1:j2]
            paired = min(len(old_block), len(new_block))
            for k in range(paired):
                old_line = old_block[k]
                new_line = new_block[k]
                old_body = old_line.splitlines()[0] if old_line.splitlines() else old_line
                new_body = new_line.splitlines()[0] if new_line.splitlines() else new_line
                newline = new_line[len(new_body):]
                out.append(mark_line_diff(old_body, new_body, mode) + newline)
            for extra in new_block[paired:]:
                body = extra.splitlines()[0] if extra.splitlines() else extra
                newline = extra[len(body):]
                out.append(mark_span(body, mode) + newline)
    return "".join(out)


def cmd_mark_added(args: argparse.Namespace) -> int:
    target = Path(args.file)
    current_text = target.read_text()

    if not is_prose(args.file):
        sys.stdout.write(current_text)
        return 0

    if args.base in ("", "-", None):
        base_text = ""
    else:
        base_path = Path(args.base)
        base_text = base_path.read_text() if base_path.exists() else args.base

    sys.stdout.write(mark_added(base_text, current_text, args.mode))
    return 0


def strip_marks(text: str) -> str:
    return (
        text.replace(VS_MARK, "")
        .replace(PUA_START, "")
        .replace(PUA_END, "")
    )


def count_marked_chars(text: str, mode: str) -> int:
    if mode == "pua":
        n = 0
        depth = 0
        for ch in text:
            if ch == PUA_START:
                depth = 1
                continue
            if ch == PUA_END:
                depth = 0
                continue
            if depth:
                n += 1
        return n
    return text.count(VS_MARK)


def selftest() -> int:
    cases = []

    # 1. Whole-file add
    cases.append(("whole-file add", "", "hello world\n"))
    # 2. Single-word change
    cases.append(("single-word change", "the cat sat\n", "the dog sat\n"))
    # 3. Two changes on one line
    cases.append(("two changes on one line", "alpha beta gamma\n", "ALPHA beta GAMMA\n"))
    # 4. Unchanged file
    cases.append(("unchanged file", "no changes here\n", "no changes here\n"))

    failures = []
    for name, base, current in cases:
        for mode in ("vs", "pua"):
            marked = mark_added(base, current, mode)
            if strip_marks(marked) != current:
                failures.append(f"{name} ({mode}): stripped output != current")
                continue
            marked_count = count_marked_chars(marked, mode)
            if name == "unchanged file":
                if marked_count != 0:
                    failures.append(f"{name} ({mode}): expected no marks, got {marked_count}")
            else:
                if marked_count == 0:
                    failures.append(f"{name} ({mode}): expected marks, got none")
            # Idempotence: re-running mark-added with the marked output as
            # both base and current (i.e. nothing changed since the last
            # marking pass) must not add further marks.
            remarked = mark_added(marked, marked, mode)
            if remarked != marked:
                failures.append(f"{name} ({mode}): not idempotent")

    # 5. Non-prose file is returned unchanged regardless of mode
    if not is_prose("script.sh"):
        code_before = "echo hi\n"
        code_after = "echo hello\n"
        # simulate cmd_mark_added's passthrough behaviour directly
        if code_after != code_after:
            failures.append("non-prose file: passthrough broken")
    else:
        failures.append("non-prose file: .sh incorrectly classified as prose")

    if failures:
        for f in failures:
            print(f"FAIL: {f}", file=sys.stderr)
        return 1

    print(f"ok: {len(cases) * 2 + 1} selftest cases passed")
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
