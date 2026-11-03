#!/usr/bin/env python3
"""Count gender-coded words in a job ad.

A port of the word lists and scoring in Kat Matfield's Gender Decoder
(https://github.com/lovedaybrooke/gender-decoder), which in turn come from
Gaucher, Friesen and Kay (2011). Matching is by word stem: "lead" matches
"leader" and "leadership".

Usage: decode.py FILE   (or pipe text on stdin)
Prints JSON: the verdict, the counts, and every hit with its line number,
so a reader (human or model) can check each one in context.

Word lists: Copyright (c) 2016 lovedaybrooke, MIT licence. See NOTICE.
"""
import json
import re
import sys

NON_CODED_EXCEPTIONS = {"sharepoint"}

FEMININE = [
    "agree", "affectionate", "child", "cheer", "collab", "commit", "communal",
    "compassion", "connect", "considerate", "cooperat", "co-operat", "depend",
    "emotiona", "empath", "feel", "flatterable", "gentle", "honest",
    "interpersonal", "interdependen", "interpersona", "inter-personal",
    "inter-dependen", "inter-persona", "kind", "kinship", "loyal", "modesty",
    "nag", "nurtur", "pleasant", "polite", "quiet", "respon", "sensitiv",
    "submissive", "support", "sympath", "tender", "together", "trust",
    "understand", "warm", "whin", "enthusias", "inclusive", "yield", "share",
    "sharin",
]

MASCULINE = [
    "active", "adventurous", "aggress", "ambitio", "analy", "assert", "athlet",
    "autonom", "battle", "boast", "challeng", "champion", "compet", "confident",
    "courag", "decid", "decision", "decisive", "defend", "determin", "domina",
    "dominant", "driven", "fearless", "fight", "force", "greedy", "head-strong",
    "headstrong", "hierarch", "hostil", "impulsive", "independen", "individual",
    "intellect", "lead", "logic", "objective", "opinion", "outspoken", "persist",
    "principle", "reckless", "self-confiden", "self-relian", "self-sufficien",
    "selfconfiden", "selfrelian", "selfsufficien", "stubborn", "superior",
    "unreasonab",
]

HYPHENATED = [s for s in FEMININE + MASCULINE if "-" in s]
SPLIT = re.compile(r"[^a-z\-]+")


def words(line):
    """Lower-case words; hyphenated words split unless the hyphen is coded."""
    out = []
    for w in SPLIT.split(line.lower()):
        w = w.strip("-")
        if not w:
            continue
        if "-" in w and not any(w.startswith(h) for h in HYPHENATED):
            out.extend(p for p in w.split("-") if p)
        else:
            out.append(w)
    return out


def hits(text, stems):
    found = []
    for n, line in enumerate(text.splitlines(), 1):
        for w in words(line):
            if w in NON_CODED_EXCEPTIONS:
                continue
            stem = next((s for s in stems if w.startswith(s)), None)
            if stem:
                found.append({"word": w, "stem": stem, "line": n})
    return found


def verdict(fem, masc):
    """Same thresholds as the Gender Decoder."""
    score = fem - masc
    if score == 0:
        return "neutral" if fem else "empty"
    if score > 3:
        return "strongly feminine-coded"
    if score > 0:
        return "feminine-coded"
    if score < -3:
        return "strongly masculine-coded"
    return "masculine-coded"


def main():
    text = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else sys.stdin.read()
    f, m = hits(text, FEMININE), hits(text, MASCULINE)
    print(json.dumps({
        "verdict": verdict(len(f), len(m)),
        "feminine_count": len(f),
        "masculine_count": len(m),
        "feminine": f,
        "masculine": m,
    }, indent=2))


if __name__ == "__main__":
    main()
