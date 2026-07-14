#!/usr/bin/env python3
"""Interrupt Capture: a tiny local CLI for recording interruption context."""

from __future__ import annotations

import datetime as _dt
import os
import platform
import re
import subprocess
import sys
from pathlib import Path


APP_DIR = Path.home() / ".interrupt-capture"


HELP = """Interrupt Capture

Usage:
  ic "note text"       Append a note to today's log.
  ic                  Read one note line from stdin, then append it.
  ic resume [kw]      Show today's log, or the most recent log; filter by kw.
  ic list             List available log dates.
  ic --help           Show this help.

Storage:
  ~/.interrupt-capture/YYYY-MM-DD.md
"""


PATH_LINE_RE = re.compile(r"(?P<path>(?:~|/|\.|[\w.-]+/)[^\s:]+):(?P<line>\d+)")
PATH_RE = re.compile(r"(?<![\w/.-])(?P<path>(?:~|/|\.|[\w.-]+/)[^\s:]+)")
CWD_RE = re.compile(r"(?:^|\s)::cwd=(?P<cwd>.*?)(?=\s::\w+=|$)")
TIME_RE = re.compile(r"^-\s+\[(?P<time>\d{2}:\d{2})\]")


def today_path() -> Path:
    return APP_DIR / f"{_dt.date.today().isoformat()}.md"


def ensure_app_dir() -> None:
    APP_DIR.mkdir(parents=True, exist_ok=True)


def clean_field(value: str) -> str:
    """Keep the one-line storage format grep-friendly."""
    return " ".join(value.replace("\n", " ").replace("\r", " ").split())


def current_branch(cwd: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=1.5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None

    branch = clean_field(result.stdout.strip())
    return branch or None


def frontmost_window_title() -> str | None:
    """Best-effort macOS frontmost window title; fail silently elsewhere."""
    if platform.system() != "Darwin":
        return None

    script = r'''
tell application "System Events"
  set frontApp to first application process whose frontmost is true
  set appName to name of frontApp
  set winTitle to ""
  try
    set winTitle to name of front window of frontApp
  end try
  if winTitle is "" then
    return appName
  else
    return appName & " - " & winTitle
  end if
end tell
'''
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=1.5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None

    title = clean_field(result.stdout.strip())
    return title or None


def append_note(note: str) -> int:
    note = clean_field(note)
    if not note:
        print("empty note, nothing captured", file=sys.stderr)
        return 1

    ensure_app_dir()
    now = _dt.datetime.now().strftime("%H:%M")
    cwd = Path.cwd()
    line = f"- [{now}] {note}  ::cwd={cwd}"

    branch = current_branch(cwd)
    if branch:
        line += f" ::branch={branch}"

    title = frontmost_window_title()
    if title:
        line += f" ::win={title}"

    path = today_path()
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")

    print(f"captured: {path}")
    return 0


def read_interactive_note() -> str:
    try:
        print("empty input cancels", file=sys.stderr)
        return input("note> ")
    except EOFError:
        return ""


def log_files() -> list[Path]:
    if not APP_DIR.exists():
        return []
    return sorted(APP_DIR.glob("*.md"))


def list_logs() -> int:
    for path in log_files():
        print(path.stem)
    return 0


def choose_resume_file() -> Path | None:
    path = today_path()
    if path.exists():
        return path

    files = log_files()
    return files[-1] if files else None


def color(text: str, code: str) -> str:
    if not sys.stdout.isatty():
        return text
    return f"\033[{code}m{text}\033[0m"


def expand_path(raw: str) -> Path:
    return Path(os.path.expanduser(raw)).resolve()


def find_open_hints(lines: list[str]) -> list[str]:
    hints: list[str] = []
    seen: set[str] = set()

    for line in lines:
        for match in PATH_LINE_RE.finditer(line):
            raw = match.group("path")
            line_no = match.group("line")
            path = expand_path(raw)
            if path.exists():
                cmd = f"${{EDITOR:-vi}} +{line_no} {quote_path(path)}"
                if cmd not in seen:
                    seen.add(cmd)
                    hints.append(cmd)

        for match in PATH_RE.finditer(line):
            raw = match.group("path").rstrip(".,);]")
            path = expand_path(raw)
            if path.exists():
                cmd = f"open {quote_path(path)}"
                if cmd not in seen:
                    seen.add(cmd)
                    hints.append(cmd)

    return hints


def quote_path(path: Path) -> str:
    text = str(path)
    return "'" + text.replace("'", "'\\''") + "'"


def cwd_for_line(line: str) -> str:
    match = CWD_RE.search(line)
    return match.group("cwd") if match else "(unknown cwd)"


def time_for_line(line: str) -> str:
    match = TIME_RE.search(line)
    return match.group("time") if match else "--:--"


def shorten_cwd(cwd: str) -> str:
    homes = [str(Path.home()), str(Path.home().resolve())]
    for home in dict.fromkeys(homes):
        if cwd == home:
            return "~"
        if cwd.startswith(home + os.sep):
            return "~" + cwd[len(home) :]
    return cwd


def highlight_paths(line: str) -> str:
    line = PATH_LINE_RE.sub(lambda m: color(m.group(0), "1;36"), line)
    return PATH_RE.sub(lambda m: color(m.group(0), "36"), line)


def resume(keyword: str | None) -> int:
    path = choose_resume_file()
    if path is None:
        print(f"no logs found in {APP_DIR}")
        return 0

    numbered_lines = list(enumerate(path.read_text(encoding="utf-8").splitlines(), start=1))
    if keyword:
        needle = keyword.lower()
        numbered_lines = [(n, line) for n, line in numbered_lines if needle in line.lower()]

    if not numbered_lines:
        print("no matching entries")
        return 0

    grouped: dict[str, list[tuple[int, str]]] = {}
    for line_no, line in numbered_lines:
        grouped.setdefault(cwd_for_line(line), []).append((line_no, line))

    for cwd, entries in grouped.items():
        last_time = time_for_line(entries[-1][1])
        count = len(entries)
        label = "entry" if count == 1 else "entries"
        header = f"📂 {shorten_cwd(cwd)} — {count} {label} · last {last_time}"
        print(color(header, "1;35"))

        for line_no, line in entries:
            location = color(str(path) + ":" + str(line_no), "1;35")
            print(f"  {location}: {highlight_paths(line)}")

        hints = find_open_hints([line for _, line in entries])
        if hints:
            print("  open hints:")
            for hint in hints:
                print(f"    {hint}")

    return 0


def main(argv: list[str]) -> int:
    if not argv or argv == ["--help"] or argv == ["-h"]:
        if argv and argv[0].startswith("-"):
            print(HELP.rstrip())
            return 0
        return append_note(read_interactive_note())

    command = argv[0]
    if command == "resume":
        keyword = " ".join(argv[1:]) if len(argv) > 1 else None
        return resume(keyword)
    if command == "list":
        return list_logs()

    return append_note(" ".join(argv))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
