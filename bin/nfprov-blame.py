#!/usr/bin/env python3
"""nfprov-blame.py -- whole-history provenance attribution for one file.

Where bin/nfprov-diff.py marks the characters added by a *single* commit, this
tool walks every commit that touched FILE and attributes each character of
the final content to the commit that introduced it, so the zociety.dev site
can render a document with human-written and agent-written characters
visibly distinct.

    nfprov-blame.py [--ref REF] [--mode vs|pua] [--format marked|html|json] FILE
    nfprov-blame.py --selftest

Attribution walk. `git log --reverse REF -- FILE` gives the commits in
order. For each one the content before and after is compared with the SAME
span rule bin/nfprov-diff.py uses (its helpers are imported, not copied):
SequenceMatcher on lines; equal lines keep their prior attribution;
inserted lines are attributed wholly to the commit; replaced blocks pair
old/new lines index-wise, keep the attribution of the common prefix and
common suffix from the old line and attribute only the middle to the
commit; unpaired new lines are attributed wholly. If git's history
simplification leaves the walked result different from REF:FILE, one extra
step attributes the residue to REF's tip commit.

Who is an agent. Ground truth written by the harness is read first, commit
conventions after. The rungs, first match wins (kind "ai" unless the last):
  1. a refs/notes/agent note on the commit saying `kind: ai` (written by
     bin/zblind seal for every loop turn). Name: the note's `model:` line
     once bin/zblind reveal has added it, else "sealed" -- inside a live
     cycle the model is encrypted under refs/notes/blind and unknown here;
  2. an `Agent:` trailer in the body (.githooks/prepare-commit-msg adds
     `Agent: claude-code` or `claude-code/<model>` to commits made from a
     Claude Code shell). Name: the trailer value;
  3. a `Co-Authored-By: Claude ...` trailer. Name: "Claude Opus 4.5";
  4. legacy fallback, a subject matching `^\\[[a-z-]+\\] ` (bin/zevent
     commits before the notes existed, and by-hand `[fix]` prefixes). Name:
     the `"agent"` field of the bin/zevent JSON envelope in the body (the
     whole body, or a JSON object embedded in it); else the subject token
     between `] ` and the first `:` when it looks like a name -- a single
     word such as "opus", "system", "3", or a Title-Cased phrase such as
     "Claude Sonnet 4" -- and is not a revision marker like "rev66"; else
     the bracket word ("[evolve] rev66: stable ..." -> "evolve");
  5. everything else is human (kind "human").
Notes come from `git log --notes=agent` (`%N`); a repository without
refs/notes/agent behaves as if rung 1 never matches. Humans are reported
under the single name "human" (the same person commits as delano, zociety
and zociety-dev); the git author name is kept in each span's `author` field
and the html `data-author` attribute. Over-marking is the accepted failure
direction (delano/nerd-fonts#15): a human who commits with a `[fix]`
prefix is counted as an agent, a rewritten sentence is marked in full even
where letters happen to coincide, and nothing is ever un-marked.

Output formats:
  marked  final text; AI-attributed characters encoded by the vendored
          upstream do_mark (state "ai", chosen mode); whitespace and human
          characters untouched. do_strip of it equals the original file.
  html    the marked text html-escaped, each maximal same-commit run wrapped
          in <span class="prov prov-ai|prov-human" data-agent data-author
          data-sha data-date data-subject>, for insertion inside a <pre>.
  json    {"file","ref","commits","first_date","last_date",
           "chars":{"total","ai","human"}, "agents":[...], "spans":[...],
           "marked","html"} -- consumed by bin/zsite-generate via jq, so the
          key names are fixed. Character counts ignore whitespace; span
          offsets index the unmarked text.
"""
from __future__ import annotations

import argparse
import difflib
import html
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

sys.dont_write_bytecode = True  # keep bin/ free of __pycache__

# Load the front end by path: its file is bin/nfprov-diff.py (hyphen -> not
# importable), and a plain `import nfprov` would grab the vendored canonical
# tool at bin/nfprov.py instead. It lazily loads bin/nfprov.py in turn.
import importlib.util  # noqa: E402
_diff_path = Path(__file__).resolve().with_name("nfprov-diff.py")
_spec = importlib.util.spec_from_file_location("nfprov_diff", _diff_path)
if _spec is None or _spec.loader is None:
    raise ImportError(f"cannot load {_diff_path}")
nfprov = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(nfprov)

AGENT_SUBJECT = re.compile(r"^\[([a-z-]+)\] (.*)$")
AGENT_TOKEN = re.compile(r"^[A-Za-z0-9][\w.-]*$")
AGENT_PHRASE = re.compile(r"^[A-Z0-9][\w.-]*( [A-Z0-9][\w.-]*){1,3}$")
REVISION_TOKEN = re.compile(r"^rev\d+$", re.IGNORECASE)
COAUTHOR_TRAILER = re.compile(r"^Co-Authored-By:\s*(Claude[^<\n]*?)\s*(?:<|$)", re.IGNORECASE | re.MULTILINE)
AGENT_TRAILER = re.compile(r"^Agent:[ \t]*(\S[^\n]*?)[ \t]*$", re.IGNORECASE | re.MULTILINE)
NOTE_KIND_AI = re.compile(r"^kind:[ \t]*ai[ \t]*$", re.MULTILINE)
NOTE_MODEL = re.compile(r"^model:[ \t]*(\S[^\n]*?)[ \t]*$", re.MULTILINE)
ENVELOPE_OBJECT = re.compile(r"\{.*\}", re.DOTALL)
ENVELOPE_AGENT = re.compile(r'"agent"\s*:\s*"([^"\\]+)"')
NOTES_REF = "agent"  # refs/notes/agent, written by bin/zblind
LOG_FORMAT = "%H%x1f%an%x1f%ad%x1f%s%x1f%B%x1f%N"  # records are NUL-separated (-z)
SEALED_NAME = "sealed"
HUMAN_NAME = "human"
SUBJECT_ATTR_MAX = 120


@dataclass(frozen=True)
class Commit:
    sha: str
    author: str
    date: str
    subject: str
    kind: str  # "ai" | "human"
    agent: str


# --- attribution rule ------------------------------------------------------


def envelope_agent(body: str) -> str | None:
    """`agent` from a bin/zevent JSON envelope in the commit body, if any."""
    candidates = [body.strip()]
    embedded = ENVELOPE_OBJECT.search(body)
    if embedded:
        candidates.append(embedded.group(0))
    for candidate in candidates:
        try:
            data = json.loads(candidate)
        except ValueError:
            continue
        if isinstance(data, dict) and isinstance(data.get("agent"), str) and data["agent"].strip():
            return data["agent"].strip()
    loose = ENVELOPE_AGENT.search(body)
    return loose.group(1).strip() if loose else None


def subject_agent(subject: str) -> tuple[str, str | None] | None:
    """(bracket word, name-like token or None) for an agent-prefixed subject."""
    match = AGENT_SUBJECT.match(subject)
    if not match:
        return None
    bracket, rest = match.groups()
    token, sep, _ = rest.partition(":")
    token = token.strip()
    if (
        sep
        and token
        and not REVISION_TOKEN.match(token)
        and (AGENT_TOKEN.match(token) or AGENT_PHRASE.match(token))
    ):
        return bracket, token
    return bracket, None


def classify(subject: str, body: str, author: str, note: str = "") -> tuple[str, str]:
    """(kind, name) for a commit, per the module docstring.

    `note` is the commit's refs/notes/agent note ("" when absent)."""
    # 1. harness-written note (bin/zblind seal / reveal)
    if NOTE_KIND_AI.search(note):
        model = NOTE_MODEL.search(note)
        return "ai", model.group(1) if model else SEALED_NAME
    # 2. harness-written trailer (.githooks/prepare-commit-msg)
    trailer = AGENT_TRAILER.search(body)
    if trailer:
        return "ai", trailer.group(1)
    # 3. coding-agent co-author trailer
    coauthor = COAUTHOR_TRAILER.search(body)
    if coauthor:
        return "ai", coauthor.group(1).strip()
    # 4. legacy convention: [event] subject prefix
    prefixed = subject_agent(subject)
    if prefixed is None:
        return "human", author
    name = envelope_agent(body) or prefixed[1] or prefixed[0]
    return "ai", name or "ai"


def make_commit(
    sha: str, author: str, date: str, subject: str, body: str = "", note: str = ""
) -> Commit:
    kind, agent = classify(subject, body, author, note)
    return Commit(sha, author, date, subject, kind, agent)


# --- git access ------------------------------------------------------------


def run_git(repo: Path, *args: str, input_bytes: bytes | None = None) -> bytes:
    proc = subprocess.run(
        ["git", *args], cwd=repo, input=input_bytes, capture_output=True, check=False
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {proc.stderr.decode('utf-8', 'replace').strip()}")
    return proc.stdout


def parse_log(raw: bytes) -> list[Commit]:
    commits = []
    for record in raw.decode("utf-8", "replace").split("\x00"):
        if not record.strip():
            continue
        sha, author, date, subject, body, note = record.split("\x1f", 5)
        commits.append(make_commit(sha, author, date, subject, body, note))
    return commits


# --notes=agent fills %N from refs/notes/agent; an absent ref only costs a
# warning on stderr and leaves %N empty (rung 1 never matches).
LOG_ARGS = ("log", "-z", f"--format={LOG_FORMAT}", f"--notes={NOTES_REF}", "--date=short")


def file_history(repo: Path, path: str, ref: str) -> list[Commit]:
    raw = run_git(repo, *LOG_ARGS, "--reverse", ref, "--", path)
    return parse_log(raw)


def tip_commit(repo: Path, ref: str) -> Commit:
    raw = run_git(repo, *LOG_ARGS, "-1", ref)
    return parse_log(raw)[0]


def blob_contents(repo: Path, shas: list[str], path: str) -> list[str]:
    """Content of path at each sha via one `git cat-file --batch`; "" if absent."""
    if not shas:
        return []
    request = "".join(f"{sha}:{path}\n" for sha in shas).encode("utf-8")
    out = run_git(repo, "cat-file", "--batch", input_bytes=request)
    contents = []
    pos = 0
    for _ in shas:
        newline = out.index(b"\n", pos)
        header = out[pos:newline].decode("utf-8", "replace").split()
        pos = newline + 1
        if header[-1] in ("missing", "ambiguous") or header[1] != "blob":
            contents.append("")
            continue
        size = int(header[2])
        contents.append(out[pos : pos + size].decode("utf-8"))
        pos += size + 1  # trailing LF after each object
    return contents


def locate(file: str) -> tuple[Path, str]:
    """(repo toplevel, repo-relative path) for a file argument."""
    top = Path(run_git(Path.cwd(), "rev-parse", "--show-toplevel").decode().strip())
    abs_path = Path(file).resolve()
    try:
        rel = abs_path.relative_to(top)
    except ValueError:
        raise SystemExit(f"nfprov-blame: {file} is outside the git repository {top}") from None
    return top, rel.as_posix()


# --- attribution -----------------------------------------------------------

Lines = list[str]
Attr = list[list[int]]  # per line, one commit index per character


def line_diff_attr(old_line: str, old_attr: list[int], new_line: str, ci: int) -> list[int]:
    """Attribution for new_line given old_line's, marking only the changed middle."""
    old_body, old_nl = nfprov._split_body(old_line)
    new_body, new_nl = nfprov._split_body(new_line)
    if old_body == new_body:
        body_attr = old_attr[: len(old_body)]
    else:
        prefix_len = nfprov.common_prefix_len(old_body, new_body)
        suffix_len = nfprov.common_suffix_len(old_body, new_body, prefix_len)
        suffix_len = min(suffix_len, len(new_body) - prefix_len)
        body_attr = old_attr[:prefix_len] + [ci] * (len(new_body) - prefix_len - suffix_len)
        if suffix_len:
            body_attr += old_attr[len(old_body) - suffix_len : len(old_body)]
    nl_attr = old_attr[len(old_body) :] if old_nl == new_nl else [ci] * len(new_nl)
    return body_attr + nl_attr


def attribute_step(prev_lines: Lines, prev_attr: Attr, new_text: str, ci: int) -> tuple[Lines, Attr]:
    new_lines = new_text.splitlines(keepends=True)
    sm = difflib.SequenceMatcher(a=prev_lines, b=new_lines, autojunk=False)
    out_lines: Lines = []
    out_attr: Attr = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            out_lines.extend(new_lines[j1:j2])
            out_attr.extend(prev_attr[i1:i2])
        elif tag == "insert":
            for line in new_lines[j1:j2]:
                out_lines.append(line)
                out_attr.append([ci] * len(line))
        elif tag == "replace":
            paired = min(i2 - i1, j2 - j1)
            for k in range(paired):
                line = new_lines[j1 + k]
                out_lines.append(line)
                out_attr.append(line_diff_attr(prev_lines[i1 + k], prev_attr[i1 + k], line, ci))
            for line in new_lines[j1 + paired : j2]:
                out_lines.append(line)
                out_attr.append([ci] * len(line))
        # delete: nothing survives
    return out_lines, out_attr


@dataclass
class Blame:
    file: str
    ref: str
    commits: list[Commit]
    text: str
    attr: list[int]  # commit index per character of text

    def runs(self) -> list[tuple[int, int, int]]:
        """Maximal (start, end, commit index) runs over text."""
        out: list[tuple[int, int, int]] = []
        start = 0
        for i in range(1, len(self.attr) + 1):
            if i == len(self.attr) or self.attr[i] != self.attr[start]:
                out.append((start, i, self.attr[start]))
                start = i
        return out


def blame(repo: Path, path: str, ref: str) -> Blame:
    commits = file_history(repo, path, ref)
    if not commits:
        raise SystemExit(f"nfprov-blame: no commits touch {path} on {ref}")
    contents = blob_contents(repo, [c.sha for c in commits], path)
    final = blob_contents(repo, [ref], path)[0]
    if not final:
        raise SystemExit(f"nfprov-blame: {path} is absent at {ref}")

    lines: Lines = []
    attr: Attr = []
    for ci, content in enumerate(contents):
        lines, attr = attribute_step(lines, attr, content, ci)
    if "".join(lines) != final:
        commits = [*commits, tip_commit(repo, ref)]
        lines, attr = attribute_step(lines, attr, final, len(commits) - 1)

    flat = [ci for line_attr in attr for ci in line_attr]
    text = "".join(lines)
    assert len(flat) == len(text)
    return Blame(path, ref, commits, text, flat)


# --- rendering -------------------------------------------------------------


def render_marked(b: Blame, mode: str) -> tuple[str, list[str]]:
    """(marked text, marked segment per run) with AI runs encoded by upstream."""
    segments = []
    for start, end, ci in b.runs():
        segment = b.text[start:end]
        if b.commits[ci].kind == "ai":
            segment = nfprov.mark_span(segment, mode)
        segments.append(segment)
    return "".join(segments), segments


def span_open_tag(c: Commit) -> str:
    def attr(value: str) -> str:
        return html.escape(value, quote=True)

    return (
        f'<span class="prov prov-{c.kind}" data-agent="{attr(display_name(c))}"'
        f' data-author="{attr(c.author)}"'
        f' data-sha="{attr(c.sha[:7])}" data-date="{attr(c.date)}"'
        f' data-subject="{attr(c.subject[:SUBJECT_ATTR_MAX])}">'
    )


def display_name(c: Commit) -> str:
    """Agent name as reported: every human collapses to HUMAN_NAME."""
    return HUMAN_NAME if c.kind == "human" else c.agent


def render_html(b: Blame, segments: list[str]) -> str:
    parts = []
    for (start, end, ci), segment in zip(b.runs(), segments):
        escaped = html.escape(segment, quote=False)
        if b.text[start:end].isspace():
            parts.append(escaped)
        else:
            parts.append(span_open_tag(b.commits[ci]) + escaped + "</span>")
    return "".join(parts)


def render_json(b: Blame, marked: str, html_out: str) -> dict:
    ink = [not ch.isspace() for ch in b.text]
    by_commit = [0] * len(b.commits)
    for ci, is_ink in zip(b.attr, ink):
        if is_ink:
            by_commit[ci] += 1

    agents: dict[tuple[str, str], dict] = {}
    for c, count in zip(b.commits, by_commit):
        name = display_name(c)
        entry = agents.setdefault(
            (name, c.kind), {"name": name, "kind": c.kind, "chars": 0, "commits": 0}
        )
        entry["chars"] += count
        entry["commits"] += 1
    agent_list = sorted(agents.values(), key=lambda a: (-a["chars"], -a["commits"], a["name"]))

    ai_chars = sum(n for c, n in zip(b.commits, by_commit) if c.kind == "ai")
    total = sum(ink)
    spans = [
        {
            "start": start,
            "end": end,
            "kind": b.commits[ci].kind,
            "agent": display_name(b.commits[ci]),
            "author": b.commits[ci].author,
            "sha": b.commits[ci].sha[:7],
            "date": b.commits[ci].date,
            "subject": b.commits[ci].subject,
        }
        for start, end, ci in b.runs()
    ]
    dates = sorted(c.date for c in b.commits)
    return {
        "file": b.file,
        "ref": b.ref,
        "commits": len(b.commits),
        "first_date": dates[0],
        "last_date": dates[-1],
        "chars": {"total": total, "ai": ai_chars, "human": total - ai_chars},
        "agents": agent_list,
        "spans": spans,
        "marked": marked,
        "html": html_out,
    }


def render(b: Blame, mode: str, fmt: str) -> str:
    marked, segments = render_marked(b, mode)
    if fmt == "marked":
        return marked
    html_out = render_html(b, segments)
    if fmt == "html":
        return html_out
    return json.dumps(render_json(b, marked, html_out), ensure_ascii=False) + "\n"


# --- selftest --------------------------------------------------------------


def selftest() -> int:
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    # Attribution rule, straight from the docstring: one block per rung.
    envelope = '{\n  "z": 1,\n  "event": "vote",\n  "agent": "nova",\n  "state": {"members": 1}\n}\n'
    trailer = "notes\n\nCo-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>\n"
    agent_trailer = "Route git through the container\n\nAgent: claude-code\n"
    agent_model_trailer = "body\n\nAgent: claude-code/claude-opus-4-5\nCo-Authored-By: Claude Opus 4.5 <x>\n"
    sealed_note = "kind: ai\nrunner: local\n"
    revealed_note = "kind: ai\nrunner: github-actions\n\nmodel: claude-haiku-4-5\nclient: claude\n"
    for subject, body, author, note, expected in (
        # 1. refs/notes/agent beats every convention below
        ("[vote] 3: yes on rule 2", envelope, "zociety", sealed_note, ("ai", "sealed")),
        ("[vote] 3: yes on rule 2", envelope, "zociety", revealed_note, ("ai", "claude-haiku-4-5")),
        ("docs: plain subject", agent_trailer, "zociety", revealed_note, ("ai", "claude-haiku-4-5")),
        ("docs: plain subject", "", "delano", sealed_note, ("ai", "sealed")),
        ("docs: plain subject", "", "delano", "kind: human\n", ("human", "delano")),
        # 2. Agent: trailer beats Co-Authored-By and the subject prefix
        ("Route git through the container", agent_trailer, "zociety-dev", "", ("ai", "claude-code")),
        ("[fix] typo", agent_model_trailer, "delano", "", ("ai", "claude-code/claude-opus-4-5")),
        # 3. Co-Authored-By beats the subject prefix
        ("[evolve] rev66: stable PROMPT.md", trailer, "zociety", "", ("ai", "Claude Opus 4.5")),
        ("Improve zloop: add debug mode", trailer, "zociety", "", ("ai", "Claude Opus 4.5")),
        # 4. legacy [event] prefix: envelope > subject token > bracket word
        ("[stuff] opus: added stuff/index.md", "", "zociety", "", ("ai", "opus")),
        ("[direction] system: Cycle 35 produced stubs", "", "zociety", "", ("ai", "system")),
        ("[evolve] rev66: stable PROMPT.md", "", "zociety", "", ("ai", "evolve")),
        ("[fix] made bin scripts executable", "", "delano", "", ("ai", "fix")),
        ("[vote] 3: yes on rule 2", "", "zociety", "", ("ai", "3")),
        ("[vote] 3: yes on rule 2", envelope, "zociety", "", ("ai", "nova")),
        ("[vote] 3: yes on rule 2", "prose then " + envelope, "zociety", "", ("ai", "nova")),
        ("[join] Claude Sonnet 4: Hello!", "", "zociety", "", ("ai", "Claude Sonnet 4")),
        ("[evolve] fix self-sustaining loop: heap-death first", "", "delano", "", ("ai", "evolve")),
        # 5. human
        ("Primer founds Zociety", "", "delano", "", ("human", "delano")),
        ("docs: close spec gaps", "body without envelope", "zociety-dev", "", ("human", "zociety-dev")),
        ("docs: mentions Agent: inline, not a trailer", "see the Agent: field", "delano", "", ("human", "delano")),
    ):
        got = classify(subject, body, author, note)
        check(got == expected, f"classify({subject!r}, {body[:12]!r}, note={note[:8]!r}) = {got}, want {expected}")

    env = {
        **os.environ,
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_AUTHOR_DATE": "2026-01-02T00:00:00+00:00",
        "GIT_COMMITTER_DATE": "2026-01-02T00:00:00+00:00",
    }

    with tempfile.TemporaryDirectory(prefix="nfprov-blame-") as tmp:
        repo = Path(tmp)
        doc = repo / "doc.md"

        def git(*args: str, author: str = "delano") -> None:
            subprocess.run(
                [
                    "git",
                    "-c", f"user.name={author}",
                    "-c", "user.email=selftest@example.invalid",
                    "-c", "commit.gpgsign=false",
                    *args,
                ],
                cwd=repo, env=env, check=True, capture_output=True,
            )

        def commit(content: str, subject: str, author: str = "delano", body: str = "") -> None:
            doc.write_text(content, encoding="utf-8", newline="")
            git("add", "doc.md", author=author)
            git("commit", "-q", "-m", subject, *(["-m", body] if body else []), author=author)

        git("init", "-q", "-b", "main")
        # 1. human creates the file
        commit("# Title\nalpha beta gamma\nthe cat sat\nto be deleted\nx < y & z\n", "Primer founds doc")
        # 2. agent appends two lines (subject exercises attribute escaping)
        commit(
            "# Title\nalpha beta gamma\nthe cat sat\nto be deleted\nx < y & z\n"
            "opus wrote this\nand this\n",
            '[stuff] opus: add "quoted" <lines>',
            author="zociety",
        )
        # 3. human edits the middle of an agent line
        commit(
            "# Title\nalpha beta gamma\nthe cat sat\nto be deleted\nx < y & z\n"
            "opus typed this\nand this\n",
            "tweak wording",
            author="zociety-dev",  # same human, different git author name
        )
        # 4. agent rewrites one word of a human line; envelope beats the subject token
        commit(
            "# Title\nalpha beta gamma\nthe dog sat\nto be deleted\nx < y & z\n"
            "opus typed this\nand this\n",
            "[vote] 4: cat -> dog",
            author="zociety",
            body='{"z": 1, "event": "vote", "agent": "sonnet", "ts": "2026-01-02T00:00:00Z"}',
        )
        # 5. agent-prefixed commit with a revision token deletes a line
        final = "# Title\nalpha beta gamma\nthe dog sat\nx < y & z\nopus typed this\nand this\n"
        commit(final, "[evolve] rev9: drop the doomed line", author="zociety")

        # No refs/notes/agent yet: the legacy rungs classify commit 5 as "evolve".
        b = blame(repo, "doc.md", "HEAD")
        check(b.text == final, "reconstructed text != final content")
        check(len(b.commits) == 5, f"expected 5 commits, got {len(b.commits)}")
        check(b.commits[4].agent == "evolve", f"no notes ref: commit 5 agent {b.commits[4].agent}")

        # Rung 1 through git: bin/zblind seal writes the marker, reveal appends
        # the model. The noted commit is the 0-char [evolve] one, so the
        # character expectations below are unchanged.
        evolve_sha = b.commits[4].sha
        git("notes", "--ref=agent", "add", "-m", "kind: ai\nrunner: local", evolve_sha)
        sealed = blame(repo, "doc.md", "HEAD")
        check(sealed.commits[4].agent == SEALED_NAME, f"sealed note: agent {sealed.commits[4].agent}")
        git("notes", "--ref=agent", "append", "-m", "model: claude-haiku-4-5\nclient: claude", evolve_sha)
        b = blame(repo, "doc.md", "HEAD")

        # Per-character expectation. H=commit1 delano, O=opus, h=commit3 delano,
        # S=sonnet, E=evolve (nothing survives from it).
        expected = (
            "H" * len("# Title\n")
            + "H" * len("alpha beta gamma\n")
            + "H" * len("the ") + "S" * len("dog") + "H" * len(" sat\n")
            + "H" * len("x < y & z\n")
            + "O" * len("opus ") + "h" * len("typed") + "O" * len(" this\n")
            + "O" * len("and this\n")
        )
        labels = "HOhSE"
        got = "".join(labels[ci] for ci in b.attr)
        check(got == expected, f"attribution mismatch:\n got  {got}\n want {expected}")
        kinds = [c.kind for c in b.commits]
        check(kinds == ["human", "ai", "human", "ai", "ai"], f"kinds {kinds}")
        names = [c.agent for c in b.commits]
        check(names == ["delano", "opus", "zociety-dev", "sonnet", "claude-haiku-4-5"], f"agents {names}")

        for mode in ("vs", "pua"):
            marked, segments = render_marked(b, mode)
            check(nfprov.strip_marks(marked) == final, f"{mode}: strip(marked) != content")
            counts = nfprov.inspect_counts(marked)
            data = render_json(b, marked, render_html(b, segments))
            key = "ai_vs" if mode == "vs" else "ai_pua"
            check(data["chars"] == {"total": 54, "ai": 18, "human": 36}, f"{mode}: chars {data['chars']}")
            check(counts[key] == data["chars"]["ai"], f"{mode}: inspect {key}={counts[key]}")
            check(counts["assumed_human"] == data["chars"]["human"], f"{mode}: assumed_human")
            report = nfprov.upstream().do_inspect(marked, *nfprov.tables()[:2])
            check("unrecognised_selectors: -" in report, f"{mode}: unrecognised selectors")
            check("unrecognised_pua: -" in report, f"{mode}: unrecognised pua")

            html_out = data["html"]
            check('data-agent="opus"' in html_out, f"{mode}: opus span missing")
            check('data-agent="sonnet"' in html_out, f"{mode}: sonnet span missing")
            check('class="prov prov-human" data-agent="human" data-author="delano"' in html_out,
                  f"{mode}: human span")
            check('data-agent="human" data-author="zociety-dev"' in html_out, f"{mode}: author kept")
            check('data-agent="delano"' not in html_out, f"{mode}: human not collapsed")
            check("data-subject=\"[stuff] opus: add &quot;quoted&quot; &lt;lines&gt;\"" in html_out,
                  f"{mode}: subject attribute not escaped")
            check("x &lt; y &amp; z" in html_out, f"{mode}: content not escaped")
            stripped_tags = re.sub(r"</?span[^>]*>", "", html_out)
            check("<" not in stripped_tags and ">" not in stripped_tags, f"{mode}: raw angle bracket")
            check(nfprov.strip_marks(html.unescape(stripped_tags)) == final, f"{mode}: html round trip")
            check(data["agents"] == [
                {"name": "human", "kind": "human", "chars": 36, "commits": 2},
                {"name": "opus", "kind": "ai", "chars": 15, "commits": 1},
                {"name": "sonnet", "kind": "ai", "chars": 3, "commits": 1},
                {"name": "claude-haiku-4-5", "kind": "ai", "chars": 0, "commits": 1},
            ], f"{mode}: agents {data['agents']}")
            check(data["spans"][0] == {
                "start": 0, "end": len("# Title\nalpha beta gamma\nthe "), "kind": "human",
                "agent": "human", "author": "delano", "sha": b.commits[0].sha[:7],
                "date": "2026-01-02", "subject": "Primer founds doc",
            }, f"{mode}: first span {data['spans'][0]}")
            typed = next(s for s in data["spans"] if s["start"] == final.index("typed"))
            check(typed["agent"] == "human" and typed["author"] == "zociety-dev",
                  f"{mode}: typed span {typed}")
            check(data["spans"][-1]["end"] == len(final), f"{mode}: last span end")
            check(data["first_date"] == "2026-01-02" == data["last_date"], f"{mode}: dates")

            # Idempotence / determinism: a second full run is byte-identical.
            again = render(blame(repo, "doc.md", "HEAD"), mode, "json")
            check(again == render(b, mode, "json"), f"{mode}: second run differs")

    if failures:
        for f in failures:
            print(f"FAIL: {f}", file=sys.stderr)
        return 1
    print("ok: nfprov-blame selftest passed (5-commit repo with agent notes x 2 modes + classify rungs)")
    return 0


# --- CLI -------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="nfprov-blame.py", description=__doc__.split("\n\n")[0])
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--ref", default="HEAD")
    parser.add_argument("--mode", choices=("vs", "pua"), default="vs")
    parser.add_argument("--format", choices=("marked", "html", "json"), default="marked")
    parser.add_argument("file", nargs="?")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()
    if not args.file:
        parser.error("FILE is required")

    repo, path = locate(args.file)
    output = render(blame(repo, path, args.ref), args.mode, args.format)
    sys.stdout.buffer.write(output.encode("utf-8"))
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
