#!/usr/bin/env python3
"""Count agentic and communal trait words in a job ad, and list every pay mention.

The word lists come from Kat Matfield's Gender Decoder
(https://github.com/lovedaybrooke/gender-decoder), which in turn come from
Gaucher, Friesen and Kay (2011). The decoder calls the two lists
"masculine-coded" and "feminine-coded", after the stereotypes they carry. This
script calls them agentic and communal, the psychology terms underneath. Both
describe stereotypes, not people.

Matching is by word stem: "lead" matches "leader" and "leadership". Each word
counts once, even if two stems match it.

Some hits are usually fixed terms rather than trait words ("competitive
salary", "customer support", "lead generation"). They are tagged "check", never
dropped, so a reader can see them and disagree.

Usage: decode.py [--summary] FILE   (or pipe text on stdin)
Prints JSON, or a short text summary with --summary. Standard library only.

Word lists: Copyright (c) 2016 lovedaybrooke, MIT licence. See NOTICE.
"""
import json
import re
import sys
import unicodedata

NON_CODED_EXCEPTIONS = {"sharepoint"}

# The decoder's "feminine-coded" list.
COMMUNAL = [
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

# The decoder's "masculine-coded" list.
AGENTIC = [
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

HYPHENATED = [s for s in COMMUNAL + AGENTIC if "-" in s]

# Phrases where a hit is usually a fixed term, not a trait word.
# Each pattern is matched against the line. A hit inside a match is tagged,
# never removed.
LIKELY_FIXED = [
    r"competitive (?:salary|pay|package|rates?|benefits|remuneration|pension)",
    r"compet(?:ence|ent|encies|ency)\w*",
    r"competing priorities", r"\bcompetitors?\b", r"competitor (?:landscape|analysis)",
    r"(?:customer|technical|it|tech|product|user|client|desktop) support",
    r"support (?:team|desk|engineer|analyst|agent|role|tickets?|requests?)",
    r"lead generation", r"\bleads\b", r"\bteam lead\b", r"\btech lead\b",
    r"(?:market|industry|sector)[- ]leading", r"leading (?:provider|supplier|brand)",
    r"active directory", r"\banalytics\b", r"\banalysts?\b", r"data analy\w*",
    r"(?:business|product|team|company|key) objectives",
    r"(?:design|engineering|product) principles",
    r"trustpilot", r"foundation trust", r"\bnhs trust",
    r"responsibilit\w*", r"responsible for", r"\brespond\w*",
    r"depend(?:ing|ent) on", r"\bdependenc\w*",
    r"share options?", r"share scheme", r"market share",
    r"child ?care", r"tender(?:ing)? (?:process|bid)\w*", r"\btendering\b",
    r"feel free", r"decision[- ]?making", r"\bcommitted to\b",
    r"individual contributor", r"\bindividuals\b", r"\bdecisions\b",
    r"\bobjectives\b", r"understanding of",
    r"independent (?:caf\w*|shops?|retailers?|businesses|schools?|stores?|restaurants?|living|review\w*)",
    r"(?:salary|pay|package)\W+competitive", r"competitive\W+(?:depending|doe)\w*",
]
FIXED_RE = re.compile("|".join(LIKELY_FIXED), re.IGNORECASE)

PAY_RE = re.compile(
    r"[£$€]\s?\d[\d,]*(?:\.\d+)?\s?[kK]?"
    r"(?:\s?(?:-|–|—|to)\s?[£$€]?\s?\d[\d,]*(?:\.\d+)?\s?[kK]?)?"
    r"|\b\d{2,3}\s?[kK]\s?(?:-|–|—|to)\s?\d{2,3}\s?[kK]\b"
)
PAY_WORDS = re.compile(
    r"competitive (?:salary|pay|package)|\bnegotiable\b|\bDOE\b|"
    r"depending on experience|\bsalary\b|per annum|\bpro rata\b|\bOTE\b",
    re.IGNORECASE,
)
WORD_RE = re.compile(r"[a-z]+(?:-[a-z]+)*")


def normalise(text):
    """Fold Unicode forms so 'self‑reliant' (non-breaking hyphen) matches."""
    text = unicodedata.normalize("NFKC", text)
    for ch in "‐‑‒­":
        text = text.replace(ch, "-")
    return text


def tokens(line):
    """(word, start, end) for each lower-case word; hyphens split unless coded."""
    out = []
    for m in WORD_RE.finditer(line.lower()):
        w = m.group(0)
        if "-" in w and not any(w.startswith(h) for h in HYPHENATED):
            pos = m.start()
            for part in w.split("-"):
                out.append((part, pos, pos + len(part)))
                pos += len(part) + 1
        else:
            out.append((w, m.start(), m.end()))
    return out


def context(line, width=100):
    line = " ".join(line.split())
    return line if len(line) <= width else line[: width - 1] + "…"


def hits(lines, stems):
    found = []
    for n, line in enumerate(lines, 1):
        spans = [(m.start(), m.end(), m.group(0).lower()) for m in FIXED_RE.finditer(line)]
        for w, start, end in tokens(line):
            if w in NON_CODED_EXCEPTIONS:
                continue
            stem = next((s for s in stems if w.startswith(s)), None)
            if not stem:
                continue
            hit = {"word": w, "stem": stem, "line": n, "context": context(line)}
            fixed = next((t for s, e, t in spans if s <= start and end <= e), None)
            if fixed:
                hit["check"] = f"likely a fixed term: '{fixed}'"
            found.append(hit)
    return found


def lean(communal, agentic):
    """Plain-English lean, using the Gender Decoder's thresholds."""
    score = communal - agentic
    if communal == agentic == 0:
        return "no trait words found"
    if score == 0:
        return "balanced"
    side = "communal" if score > 0 else "agentic"
    return f"leans strongly {side}" if abs(score) > 3 else f"leans {side}"


def decoder_label(fem, masc):
    """The Gender Decoder's own label, for traceability."""
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


def salary_like(amount):
    """True if any number in it looks like annual pay (5,000+ or written with k)."""
    if re.search(r"\d\s?[kK]\b", amount):
        return True
    nums = [float(x.replace(",", "")) for x in re.findall(r"\d[\d,]*(?:\.\d+)?", amount)]
    return any(x >= 5000 for x in nums)


def canonical(amount):
    """Compare '£35–45K' and '£35k - £45k' as the same figure."""
    a = re.sub(r"\s|£|\$|€", "", amount.lower())
    return re.sub(r"to|–|—", "-", a)


def pay(lines):
    mentions, salaries = [], []
    for n, line in enumerate(lines, 1):
        found = [m.group(0).strip() for m in PAY_RE.finditer(line)]
        if found or PAY_WORDS.search(line):
            mention = {"line": n, "amounts": found, "context": context(line)}
            small = [a for a in found if not salary_like(a)]
            if small:
                mention["note"] = f"probably not salary: {', '.join(small)}"
            mentions.append(mention)
            salaries += [a for a in found if salary_like(a)]
    text = "\n".join(lines)
    distinct = {}
    for a in salaries:
        distinct.setdefault(canonical(a), a)
    return {
        "mentions": mentions,
        "salary_figures": list(distinct.values()),
        "more_than_one_salary_figure": len(distinct) > 1,
        # Ignore [placeholders], so a draft asking "is it negotiable?" doesn't count.
        "says_negotiable": bool(re.search(r"\bnegotiable\b", re.sub(r"\[[^\]]*\]", "", text), re.I)),
        "no_salary_figure": not salaries,
    }


def analyse(text):
    lines = normalise(text).splitlines()
    c, a = hits(lines, COMMUNAL), hits(lines, AGENTIC)
    c_kept = [h for h in c if "check" not in h]
    a_kept = [h for h in a if "check" not in h]
    n_words = sum(len(tokens(l)) for l in lines)

    def per100(k):
        return round(100 * len(k) / n_words, 1) if n_words else 0.0

    return {
        "covers": "Agentic and communal word lists, and pay figures, only. "
                  "Age, disability, gendered terms, culture and caring need reading.",
        "word_count": n_words,
        "script_adjusted": {
            "lean": lean(len(c_kept), len(a_kept)),
            "communal": len(c_kept),
            "agentic": len(a_kept),
            "communal_per_100_words": per100(c_kept),
            "agentic_per_100_words": per100(a_kept),
        },
        "raw": {
            "lean": lean(len(c), len(a)),
            "communal": len(c),
            "agentic": len(a),
            "gender_decoder_label": decoder_label(len(c), len(a)),
        },
        "communal_hits": c,
        "agentic_hits": a,
        "pay": pay(lines),
    }


def summary(r):
    """Short text version for long ads."""
    def group(hs):
        counts = {}
        for h in hs:
            counts[h["word"]] = counts.get(h["word"], 0) + 1
        return ", ".join(f"{w} x{n}" if n > 1 else w for w, n in counts.items()) or "none"

    out = [r["covers"], ""]
    sa, raw = r["script_adjusted"], r["raw"]
    out.append(f"Script-adjusted: {sa['communal']} communal, {sa['agentic']} agentic ({sa['lean']}).")
    out.append(f"Raw: {raw['communal']} communal, {raw['agentic']} agentic "
               f"(Gender Decoder label: {raw['gender_decoder_label']}).")
    for side in ("agentic", "communal"):
        hs = r[f"{side}_hits"]
        out.append(f"{side.capitalize()} kept: {group([h for h in hs if 'check' not in h])}")
        out.append(f"{side.capitalize()} tagged as likely fixed terms: {group([h for h in hs if 'check' in h])}")
    p = r["pay"]
    figs = ", ".join(p["salary_figures"]) or "none"
    out.append(f"Pay: salary figures {figs}"
               + ("; MORE THAN ONE FIGURE" if p["more_than_one_salary_figure"] else "")
               + ("; says negotiable" if p["says_negotiable"] else "; doesn't say if negotiable"))
    return "\n".join(out)


def read_input(argv):
    data = open(argv[1], "rb").read() if len(argv) > 1 else sys.stdin.buffer.read()
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("cp1252", errors="replace")


def main():
    args = [a for a in sys.argv if a != "--summary"]
    result = analyse(read_input(args))
    if "--summary" in sys.argv:
        print(summary(result))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
