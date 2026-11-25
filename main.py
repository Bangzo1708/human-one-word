#!/usr/bin/env python3
"""Your Human in One Word.

One word that describes the human we work for (a boss / client / manager).

The program holds three genuinely different candidate words, scores each
one 0-5 on the judge's five criteria in the kit's priority order, picks the
strongest by total (ties broken by the most important criterion first),
validates the gate (UTF-8 text, 1-30 characters, a single word), and writes
it to $ENTRY_OUTPUT or /output/entry.txt.

Python standard library only. Fully deterministic: the same word every run.
"""

import os
import sys

# ---------------------------------------------------------------------------
# The judge's criteria, most important first (from the kit's brief):
#   1. on_subject: one word describing the human we work for
#   2. funny:      a joke or wry observation, not a plain label
#   3. fitting:    reads as true of a boss / client / manager
#   4. vivid:      a word a reader remembers and repeats, not a flat one
#   5. lands:      the joke works on its own, no explanation needed
# ---------------------------------------------------------------------------
CRITERIA = ("on_subject", "funny", "fitting", "vivid", "lands")

# Three candidates, genuinely different from each other:
#   - a literal boss archetype, named head-on
#   - a force-of-nature metaphor for a chaotic boss
#   - a wry portrait of the boss who is never there when a decision is due
CANDIDATES = [
    {
        "word": "Micromanager",
        "why": "The boss who reviews every comma, approves every font "
               "choice, and still asks why the work is late.",
        "scores": {
            "on_subject": 5,  # literally a word for a kind of boss/manager
            "funny": 4,       # wry recognition laugh, every office knows one
            "fitting": 5,     # reads as true of a manager, not a random insult
            "vivid": 5,       # specific, memorable, instantly repeatable
            "lands": 5,       # needs no explanation at all
        },
    },
    {
        "word": "Hurricane",
        "why": "The boss who arrives without warning, rearranges "
               "everything, and leaves the team to rebuild.",
        "scores": {
            "on_subject": 4,  # a metaphor, but still a portrait of the human
            "funny": 4,       # a vivid, funny image of office chaos
            "fitting": 4,     # true of the chaotic boss, less so of a calm one
            "vivid": 5,       # a word readers picture and repeat
            "lands": 4,       # mostly self-explanatory, a beat of ambiguity
        },
    },
    {
        "word": "Ghost",
        "why": "The boss who vanishes the moment a decision is needed "
               "and reappears only to ask why nothing moved.",
        "scores": {
            "on_subject": 4,  # a metaphor for the absent boss
            "funny": 4,       # wry: everyone has chased one for a signature
            "fitting": 4,     # true of the unreachable boss, not of every boss
            "vivid": 3,       # memorable image, but a common everyday word
            "lands": 4,       # lands on its own, with a slight double meaning
        },
    },
]


def total_score(candidate):
    """Total of the five criterion scores (max 25)."""
    return sum(candidate["scores"][c] for c in CRITERIA)


def selection_key(candidate):
    """Sort key: highest total first; ties broken by the criteria in
    priority order (on_subject, then funny, then fitting, ...)."""
    return (
        total_score(candidate),
        tuple(candidate["scores"][c] for c in CRITERIA),
    )


def pick_winner(candidates):
    """Return the strongest candidate. max() keeps the first entry on a
    full tie, so candidate order is the final tie-break."""
    return max(candidates, key=selection_key)


def validate(word):
    """Gate check: 1-30 characters, UTF-8, not only whitespace, one word."""
    if not isinstance(word, str):
        raise ValueError("entry must be a string")
    if not word or word != word.strip():
        raise ValueError("entry must not be empty or padded with whitespace")
    if len(word) < 1 or len(word) > 30:
        raise ValueError("entry must be 1-30 characters, got %d" % len(word))
    if any(ch.isspace() for ch in word):
        raise ValueError("entry must be a single word, got %r" % word)
    word.encode("utf-8")  # must be valid UTF-8 text
    return word


def main():
    winner = pick_winner(CANDIDATES)
    word = validate(winner["word"])

    out_path = os.environ.get("ENTRY_OUTPUT") or "/output/entry.txt"
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    # No trailing newline: the word alone is the entry, and it keeps the
    # byte size minimal (an exact tie on win rate goes to the smaller text).
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(word)

    print("candidates:")
    for cand in CANDIDATES:
        print("  %-13s total %2d  scores %s"
              % (cand["word"], total_score(cand),
                 [cand["scores"][c] for c in CRITERIA]))
    print("winner: %s (%d characters)" % (word, len(word)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
