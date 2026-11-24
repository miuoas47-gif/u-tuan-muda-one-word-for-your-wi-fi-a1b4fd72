#!/usr/bin/env python3
"""One Word for Your Wi-Fi (make.fun: u-tuan-muda-one-word-for-your-wi-fi-a1b4fd72).

Writes a single word to ``<MAKEFUN_OUTPUT_DIR>/entry.txt``.

The word is "Ghosted": home Wi-Fi ghosts you — full bars one second,
gone mid-sentence the next, back again like nothing happened. It is
funny at once, true to how home Wi-Fi actually behaves, and a fresh
angle on a familiar annoyance (not another "slow" or "buffering").
It works as a network name with no context needed.

Deterministic: no arguments, no network, no randomness, no clock.
Always writes the same bytes and exits 0.
"""

import os
import sys

WORD = "Ghosted"


def output_dir() -> str:
    """Output directory the grader provides, defaulting to /output."""
    for var in ("MAKEFUN_OUTPUT_DIR", "MAKEFUN_OUT_DIR"):
        value = os.environ.get(var)
        if value:
            return value
    return "/output"


def valid(word: str) -> bool:
    """The sealed gate, checked locally: 1-20 chars, not only white
    space, a single word with no whitespace anywhere in it."""
    if not (1 <= len(word) <= 20):
        return False
    if not word.strip():
        return False
    return len(word.split()) == 1 and all(not ch.isspace() for ch in word)


def main() -> int:
    word = WORD
    if not valid(word):
        print("entry word fails the gate", file=sys.stderr)
        return 1
    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    # Write atomically inside the output dir so a reader never sees a
    # half-written file, then confirm the bytes on disk are the word.
    tmp_path = out_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8", newline="") as f:
        f.write(word)
    os.replace(tmp_path, out_path)
    with open(out_path, "rb") as f:
        if f.read() != word.encode("utf-8"):
            print("entry.txt bytes do not match the word", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
