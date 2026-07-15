# Interrupt Capture — Pro Spec (v0.3.0)

Goal: ship the one paid feature both target-user interviews said would make them pay —
**reflexive capture** (a global hotkey that works anywhere, not "remember to run ic in a terminal")
— behind a simple license gate, while keeping the free CLI fully functional.

Constraint: Python 3 **stdlib only**, macOS-first, no network required at runtime.

## Tiers
- **Free** (unchanged): `ic "note"`, `ic` (stdin), `ic resume [--all] [kw]`, `ic list`, `ic --help`.
- **Pro** (license-gated): `ic quick`, `ic hotkey-setup`.

## New commands

### `ic quick`  (Pro)
Reflexive capture that works when NO terminal is focused — the thing a hotkey triggers.
- On macOS: use `osascript` `display dialog` to pop a native text box:
  `display dialog "What are you doing?" default answer "" with title "Interrupt Capture"`
- Read the entered text; if non-empty, capture it via the SAME code path as `ic "note"`
  (so cwd/branch/window metadata still attaches — note: when launched from a hotkey the cwd
  will be $HOME or the launcher's dir; that's acceptable, window title is the useful signal here).
- Empty / cancel → capture nothing, exit 0 quietly.
- Non-macOS fallback: behave like `ic` (stdin prompt).

### `ic hotkey-setup`  (Pro)
Make `ic quick` reachable from a global hotkey. Do NOT require third-party tools; detect & offer:
1. If `skhd` is on PATH: print the exact line to add to `~/.skhdrc`
   (e.g. `cmd + shift - space : /opt/homebrew/bin/ic quick`) and offer to append it (ask via a
   `--write` flag; default just prints).
2. Always also print a **macOS Shortcuts / Automator Quick Action** recipe that runs
   `"$(command -v ic)" quick` (absolute path, PATH-safe), plus how to assign a keyboard shortcut.
3. Explain that GUI-launched shells don't inherit PATH → always use the absolute path.

## License gate

### `ic activate <KEY>`
- Store the key in `~/.interrupt-capture/license` (chmod 600).
- Validate STRUCTURE offline: key format `IC-PRO-XXXXXXXXXX-XXXX` where the payload is base32
  and the last group is a check segment (see keygen). On structural pass, print "Pro activated".
- On fail: print "invalid license key" and exit 1.
- `ic activate --status` (or `ic license`): show activated / not activated.

### Gating
- `quick` and `hotkey-setup` first call `require_pro()`:
  - if a valid license file exists → proceed.
  - else → print a short upsell:
    "This is a Pro feature. Get a key: https://<gumroad-or-lemonsqueezy-url> (set later)"
    and exit code 2. Do NOT crash; free features must never be affected.
- `IC_PRO_LICENSE` env var may override the file (for testing / CI).

### Honesty note (document in code + README)
This is a purchase **funnel gate**, not DRM. The client verifies key STRUCTURE only; a public
open-source client cannot hold a mint secret. Real validation will be wired to the payment
provider's license API (LemonSqueezy/Gumroad) once the seller account exists. Keys are minted by
`tools/keygen.py`, which reads the mint secret from `$IC_MINT_SECRET` (never committed).

## `tools/keygen.py`  (seller-side, NOT shipped to users)
- Input: buyer email + `$IC_MINT_SECRET`.
- `payload = base32( hmac_sha256(secret, normalized_email) )[:10]`
- `check   = base32( sha256(payload+secret) )[:4]`
- Output key: `IC-PRO-<payload>-<check>` (uppercase).
- Print the key. This lets us fulfil a sale manually today, before any payment integration.
- Add `tools/keygen.py`'s secret handling such that running without `$IC_MINT_SECRET` errors clearly.
- Ensure `.gitignore` covers any local secret files; keygen.py itself is fine to commit (no secret inside).

## Versioning / docs
- Bump internal version constant to `0.3.0`.
- Update `--help` to list Pro commands with a "(Pro)" marker.
- Update `README.md`: Free vs Pro table, activation, hotkey setup, the honesty note.

## Acceptance (codex must run under throwaway HOME)
1. Free path unaffected: capture + `resume` still work.
2. `ic quick` and `ic hotkey-setup` WITHOUT license → upsell + exit code 2.
3. `tools/keygen.py` with `IC_MINT_SECRET=test` for `a@b.com` → prints a key.
4. `ic activate <that key>` → "Pro activated"; `ic license` → activated.
5. After activation, `ic hotkey-setup` prints the skhd + Shortcuts recipe (exit 0).
6. `ic activate GARBAGE` → invalid, exit 1.
Paste outputs; report changes under 250 words.
