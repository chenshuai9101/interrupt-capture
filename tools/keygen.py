#!/usr/bin/env python3
"""Seller-side Interrupt Capture Pro key generator."""

from __future__ import annotations

import base64
import hashlib
import hmac
import os
import sys


def base32_no_padding(data: bytes) -> str:
    return base64.b32encode(data).decode("ascii").rstrip("=")


def normalize_email(email: str) -> str:
    return email.strip().lower()


def make_key(email: str, secret: str) -> str:
    normalized = normalize_email(email)
    payload = base32_no_padding(
        hmac.new(secret.encode("utf-8"), normalized.encode("utf-8"), hashlib.sha256).digest()
    )[:10]
    check = base32_no_padding(hashlib.sha256((payload + secret).encode("utf-8")).digest())[:4]
    return f"IC-PRO-{payload}-{check}"


def main(argv: list[str]) -> int:
    secret = os.environ.get("IC_MINT_SECRET")
    if not secret:
        print("IC_MINT_SECRET is required", file=sys.stderr)
        return 1

    if len(argv) != 1:
        print("usage: tools/keygen.py buyer@example.com", file=sys.stderr)
        return 1

    print(make_key(argv[0], secret))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
