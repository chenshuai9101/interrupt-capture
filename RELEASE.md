# Releasing a new version

The product repo and Homebrew tap are already live:
- Repo: https://github.com/chenshuai9101/interrupt-capture
- Tap:  https://github.com/chenshuai9101/homebrew-tap
- Install: `brew install chenshuai9101/tap/interrupt-capture`
- Landing: https://chenshuai9101.github.io/interrupt-capture/

The live tap currently ships **v0.2.0**. v0.3.1 (Pro features) is committed and tagged
locally but NOT yet pushed — pushing requires a fresh GitHub token (the previous one was
purged from the keyring after use and should be rotated).

## Steps to publish v0.3.1

```bash
export GH_TOKEN='<a FRESH fine-grained PAT with Contents:write on both repos>'
cd ~/Desktop/interrupt-capture
gh auth setup-git

# 1. push code + tag
git push origin master
git push origin v0.3.1

# 2. recompute the real sha256 of the GitHub tag tarball
SHA=$(curl -fsSL https://github.com/chenshuai9101/interrupt-capture/archive/refs/tags/v0.3.1.tar.gz | shasum -a 256 | awk '{print $1}')
echo "$SHA"

# 3. update the formula sha (both the repo copy and the tap) and remove the STALE note
#    then push the tap
TAP=~/path/to/homebrew-tap   # clone of chenshuai9101/homebrew-tap
sed -i '' -E "s#sha256 \"[a-f0-9]{64}\"#sha256 \"$SHA\"#" Formula/interrupt-capture.rb "$TAP/Formula/interrupt-capture.rb"
git -C "$TAP" commit -am "interrupt-capture 0.3.1" && git -C "$TAP" push

# 4. verify end-to-end from the public tap
brew update && brew upgrade interrupt-capture   # or reinstall
ic --version   # 0.3.1
```

## Selling Pro (funnel gate is already in the client)
- Pro features (`ic quick`, `ic hotkey-setup`) are gated behind `ic activate <KEY>`.
- Mint a key per buyer (seller-side, secret never committed):
  ```bash
  IC_MINT_SECRET='<your private secret>' python3 tools/keygen.py buyer@email.com
  ```
- Today you can fulfil sales manually (email the key). When you set up
  LemonSqueezy/Gumroad, wire real validation to their license API and replace the
  placeholder upsell URL in `interrupt_capture.py`.
