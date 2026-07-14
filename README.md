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

Optional alias:

```sh
alias resume='ic resume'
```

## Usage

```sh
ic "reviewing parser bug in src/parser.py:42"
ic
ic resume
ic resume parser
ic list
ic --help
```

Each capture appends one line to `~/.interrupt-capture/YYYY-MM-DD.md`:

```text
- [HH:MM] {note}  ::cwd={path} ::branch={b} ::win={title}
```

`::branch=` is included when the current directory is inside a Git repository.
On macOS, `::win=` is included when `osascript` can read the frontmost app or
window title. If that fails, capture continues silently.

## macOS Hotkey

GUI-launched shells do not inherit the `PATH` from your interactive terminal.
Use the absolute `ic` path or export `PATH` inside the hotkey script.

### Automator Quick Action

1. Open Automator and create a new `Quick Action`.
2. Set `Workflow receives` to `no input` in `any application`.
3. Add `Run Shell Script`.
4. Use this script:

```sh
IC="$HOME/bin/ic"
note=$(/usr/bin/osascript -e 'text returned of (display dialog "Interrupt note:" default answer "" buttons {"Cancel", "Capture"} default button "Capture")')
[ -n "$note" ] && "$IC" "$note"
```

5. Save it as `Interrupt Capture`.
6. Open System Settings -> Keyboard -> Keyboard Shortcuts -> Services and bind
   a shortcut to `Interrupt Capture`.

### skhd

Install and configure `skhd`, then add a binding like:

```sh
cmd + shift - i : export PATH="$HOME/bin:$PATH"; note=$(/usr/bin/osascript -e 'text returned of (display dialog "Interrupt note:" default answer "" buttons {"Cancel", "Capture"} default button "Capture")'); [ -n "$note" ] && "$HOME/bin/ic" "$note"
```

Reload `skhd` after editing its config.
