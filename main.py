"""One-line office joke entry for make.fun.

Writes a single fresh joke about office life to /output/entry.txt.
The entry is one line, 92 characters, no trailing newline, and the
run is deterministic: every invocation writes the same bytes.
Python 3, standard library only, no network access.
"""

import os

JOKE = "My boss said we have unlimited PTO, which explains why nobody here has ever taken a day off."

MAX_CHARS = 200


def validate_utf8(text):
    """Return (ok, reason) for the UTF-8 requirement."""
    if not isinstance(text, str):
        return False, "not text"
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return False, "not valid UTF-8"
    return True, "ok"


def validate_length(text):
    """Return (ok, reason) for the 1..MAX_CHARS length requirement."""
    if not text.strip():
        return False, "only whitespace"
    if len(text) < 1 or len(text) > MAX_CHARS:
        return False, "length %d outside 1..%d" % (len(text), MAX_CHARS)
    return True, "ok"


def validate_single_line(text):
    """Return (ok, reason) for the single-line, no-padding requirement."""
    if "\n" in text or "\r" in text:
        return False, "not a single line"
    if text != text.strip():
        return False, "leading or trailing whitespace"
    return True, "ok"


def gate_check(text):
    """Enforce the kit's gate on a candidate entry text.

    Returns (ok, reason). The gate requires UTF-8 text of 1 to 200
    characters, not only whitespace, written as a single line.
    """
    for check in (validate_utf8, validate_length, validate_single_line):
        ok, reason = check(text)
        if not ok:
            return False, reason
    return True, "ok"


def self_test():
    """Self-test of the gate and the entry itself.

    Covers the gate on valid and invalid inputs, plus the entry's own
    invariants: 92 characters, a single line with no trailing newline,
    and a deterministic re-run (two runs write identical bytes).
    """
    cases = [
        (JOKE, True),
        ("", False),                       # empty
        ("   ", False),                     # only whitespace
        ("two\nlines", False),              # not single line
        (" padded ", False),                # leading/trailing whitespace
        ("x" * 201, False),                 # over 200 chars
        ("x" * 200, True),                  # exactly 200 chars
    ]
    for text, expected in cases:
        ok, _reason = gate_check(text)
        assert ok == expected, "self-test failed for %r: got %s, want %s" % (text[:30], ok, expected)
    # Entry invariants.
    assert len(JOKE) == 92, "entry length %d, want 92" % len(JOKE)
    assert "\n" not in JOKE and "\r" not in JOKE, "entry is not a single line"
    assert JOKE == JOKE.strip(), "entry has leading/trailing whitespace"
    assert not JOKE.endswith("\n"), "entry ends with a newline"
    # Deterministic re-run: writing the entry twice yields identical bytes.
    import tempfile
    written = []
    for _ in range(2):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(JOKE.encode("utf-8"))
            written.append(tmp.name)
    with open(written[0], "rb") as f:
        first = f.read()
    with open(written[1], "rb") as f:
        second = f.read()
    assert first == second, "re-run produced different bytes"
    assert not first.endswith(b"\n"), "written entry ends with a newline"
    print("self-test passed (%d cases)" % len(cases))


def main():
    self_test()
    ok, reason = gate_check(JOKE)
    if not ok:
        raise SystemExit("gate check failed: %s" % reason)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(JOKE)
    # Verify the round-trip: what landed on disk must be exactly the joke.
    with open("/output/entry.txt", "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != JOKE:
        raise SystemExit("round-trip check failed: file differs from joke")
    ok, reason = gate_check(written)
    if not ok:
        raise SystemExit("gate check failed on written file: %s" % reason)
    print("wrote %d characters to /output/entry.txt" % len(JOKE))


if __name__ == "__main__":
    main()
