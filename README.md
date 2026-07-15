# Interrupt Capture

A tiny local CLI for recording what you were doing when you get interrupted.
It stores plain-text daily logs in `~/.interrupt-capture/` and is meant to be
searched with `grep`, `ic resume`, or your editor.

## Install

```sh
chmod +x install.sh
./install.sh
```

The installer creates `~/bin` if needed and symlinks:

```text
~/bin/ic -> ./interrupt_capture.py
```

Make sure `~/bin` is on your `PATH`:

```sh
export PATH="$HOME/bin:$PATH"
```

## Sponsorship

Interrupt Capture is 100% free & open source. If it helps you, sponsor via
WeChat:

```sh
ic sponsor
```

The bundled QR is also available at `assets/sponsor-wechat.jpg`.

## Usage

```sh
ic "reviewing parser bug in src/parser.py:42"
ic
ic resume
ic resume parser
ic resume --all
ic list
ic quick
ic hotkey-setup
ic sponsor
ic --help
```

`ic resume` shows the most recent entry for each project directory, so it works
as a "where I left off" view. Each entry includes a copy-pasteable re-entry
command prefixed with `↩`, for example:

```sh
↩  cd ~/code/app && git switch fix-login && ${EDITOR:-vim} +42 src/app.py
```

Use `ic resume --all` to show every entry grouped by project. Keyword filters
still work with either view, such as `ic resume parser` or
`ic resume --all parser`.

Each capture appends one line to `~/.interrupt-capture/YYYY-MM-DD.md`:

```text
- [HH:MM] {note}  ::cwd={path} ::branch={b} ::win={title}
```

`::branch=` is included when the current directory is inside a Git repository.
On macOS, `::win=` is included when `osascript` can read the frontmost app or
window title. If that fails, capture continues silently.

## Supporter Status

Mark this install as a supporter:

```sh
ic activate SUPPORTER-CODE
```

Check status:

```sh
ic license
ic activate --status
```

The supporter marker is stored at `~/.interrupt-capture/supporter` with mode
`600`. `IC_SUPPORTER_CODE` can override the file for testing or CI. Supporter
status is a thank-you perk that silences the occasional sponsorship nudge; it
does not unlock features.

## Quick Capture And Hotkey Setup

`ic quick` captures through a native macOS dialog:

```sh
ic quick
```

Empty input or cancel captures nothing and exits quietly. On non-macOS systems,
`ic quick` falls back to the normal stdin prompt.

Print setup instructions:

```sh
ic hotkey-setup
```

If `skhd` is on `PATH`, this prints the exact line to add to `~/.skhdrc`.
Use `--write` to append it automatically:

```sh
ic hotkey-setup --write
```

The command also prints a macOS Shortcuts / Automator Quick Action recipe.
GUI-launched shells do not inherit `PATH`, so the recipe always uses the
absolute `ic` path.

## Honesty Note

An open-source client cannot enforce a license: any local gate is trivially
bypassable. Interrupt Capture is therefore free and open; sponsorship is an
honest "buy me a coffee" model, not access control.
