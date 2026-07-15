# Pivot: paywall -> sponsorship (v0.3.1)

Decision: an open-source client cannot enforce a license (the gate is trivially
bypassable), so drop the paywall pretense and switch to an honest "buy me a coffee"
sponsorship model via the author's WeChat Pay.

## Changes to interrupt_capture.py (stdlib only)
1. UN-GATE Pro features: `ic quick` and `ic hotkey-setup` now work for everyone, no license needed. Remove the require_pro() blocking; keep the functions.
2. NEW `ic sponsor`:
   - Print: project is free & open; if it saves you time, consider sponsoring.
   - Print the author handle: WeChat "陈帅".
   - On macOS, run `open` on the bundled QR at <repo>/assets/sponsor-wechat.jpg (resolve path relative to the script location, so it works when installed via brew too — fall back to printing the path if the file isn't found).
   - Exit 0.
3. Gentle nudge (non-annoying, suppressible): after a successful capture, if the user has NOT marked themselves a supporter, occasionally show one line: "❤  enjoying ic? support it: ic sponsor". Trigger deterministically e.g. when the day's capture count is a multiple of 20. Never on every capture.
4. Repurpose `ic activate <code>` + `ic license`: activating any structurally-valid code just records supporter status (silences the nudge) — a thank-you perk, NOT access control. Update wording ("supporter mode on"). `ic license` -> shows "supporter" / "not a supporter yet".
5. Update `--help`: list `sponsor`; drop the "(Pro)" locked framing; note quick/hotkey-setup are free.
6. Bump version constant to 0.3.1.

## README.md
Replace the Free-vs-Pro paywall table with: "100% free & open source. If it helps you, sponsor via WeChat (ic sponsor)." Keep the honesty note. Mention the QR is at assets/sponsor-wechat.jpg.

## Acceptance (run under throwaway HOME, paste outputs)
1. `ic quick </dev/null` and `ic hotkey-setup` work with NO license (no upsell, no exit 2).
2. `ic sponsor` prints the WeChat 陈帅 message (and the QR path if open unavailable).
3. Capture 20 notes -> the nudge line appears at the 20th; not on the others.
4. `ic activate SUPPORTER-CODE` (any structurally ok code) -> "supporter mode on"; nudge then suppressed.
5. `--version` -> 0.3.1.
Report changes under 220 words.
