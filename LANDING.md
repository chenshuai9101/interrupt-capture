# Interrupt Capture — Landing Copy (v0.1, validated positioning)

> Positioning shifted per user-interview feedback: the paid hook is **resume = true context restore**, NOT sync/AI/analytics. Two target devs explicitly churned at "attention product / team analytics." Dev-first, privacy-first, one-time purchase.

---

## Hero

**A `git stash` for your brain.**

Get interrupted. Type one line. Get back to exactly where you were — `cd`, `git switch`, `nvim +line`, tab and all — in under 5 seconds.

`brew install muyunye/tap/interrupt-capture`

[Get it free →]   [Watch the 20s demo →]

---

## The problem (3 lines)

You're deep in a bug. Slack pings. A meeting. 40 minutes later you're staring at your editor thinking *"…what was I doing?"*
Screen recorders watch everything and creep you out. Note apps become another graveyard you forget to open.
You don't need surveillance. You need a fast way back in.

## How it works

1. **Capture** — one command (or a global hotkey). `ic "chasing the off-by-one in the parser"`
2. **Auto-context** — it grabs your cwd, git branch, active file:line, and window — no typing.
3. **Restore** — `ic resume` shows the *last session per project* and hands you the exact commands to jump back in.

```
📂 ~/work/api — 2m ago
  fixing 500 on /v2/users → handlers/users.go:88  (branch: hotfix/users-500)
  ↩  cd ~/work/api && git switch hotfix/users-500 && $EDITOR handlers/users.go:88
```

## Why it's different

- **Local & plain-text.** Your notes live in `~/.interrupt-capture/*.md`. Grep them. Own them. Delete them. Zero cloud.
- **No screen recording, no account, no telemetry.** Privacy-first by construction.
- **Terminal & git native.** Built for people who live in a shell, not a dashboard.
- **Zero to running in 10 seconds.** Python stdlib only, no dependencies to babysit.

## Pricing — 100% free, sponsor-supported

Every feature is free and open source: capture, one-command restore, project grouping, global-hotkey capture. No paywall, no subscription, no sync, no snooping.

If it saves you from a "…what was I doing?" moment, **sponsor via WeChat** (`ic sponsor`) — that's what keeps it maintained.

> An open-source client can't honestly enforce a license, so we don't pretend to. It's a tool you can trust, funded by the people it helps.

## FAQ
- **Does it phone home?** No. Ever. Read the source — it's one file.
- **Where's my data?** Plain markdown in `~/.interrupt-capture/`. That's the whole database.
- **Team features / dashboards?** Not planned. This is a personal tool by design.
