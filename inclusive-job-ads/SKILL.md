---
name: inclusive-job-ads
description: Check a job ad or job spec for gender-coded wording and other things that quietly narrow who applies, then suggest specific rewrites. Use when someone shares a job ad, job description or role spec and asks to review it, check it for bias, make it more inclusive, or work out why every applicant looks the same.
---

# Inclusive job ads

Check a job ad for wording that tells some people "this job isn't for you",
and help fix it.

The core check comes from research. Gaucher, Friesen and Kay (2011) found that
masculine-coded wording made jobs less appealing to women and lowered their
sense of belonging. It did not change how capable they felt. The ad wasn't
saying "you can't do this". It was saying "you won't fit in".

"Masculine-coded" and "feminine-coded" describe the stereotypes a word
carries, not the people reading it. Say it that way in reports: "this wording
leans on masculine stereotypes", never "this ad is for men".

Feminine-coded wording had only a small effect on men. So the goal is balance,
not swapping one set of words for the other.

## Steps

### 1. Count the coded words

Save the ad to a file and run the script beside this skill:

```bash
python3 scripts/decode.py ad.txt
```

It prints a verdict (from "strongly masculine-coded" to "strongly
feminine-coded"), the counts, and every hit with its line number. The word
lists and thresholds match Kat Matfield's Gender Decoder, so the numbers agree
with hers.

Use the script for the counting. Don't count by eye.

### 2. Check each hit in context

The script matches word stems, so it can't tell meaning. Go through every hit
and mark it as one of these:

- **Coded:** it describes the person or the culture. "A competitive, driven
  self-starter" is coded.
- **Not coded:** it's a fixed term, a team or product name, or a job title.
  "Competitive salary", "customer support team", "Team Lead" and "analytics"
  (the function) are usually not coded.

Report both the raw verdict and your adjusted one, and say which hits you
discounted and why. Never hide a hit. The reader should be able to disagree
with you.

### 3. Look beyond single words

Word lists miss a lot. Check for the patterns below. Label each one with its
evidence level and don't overstate it.

| Pattern | What to look for | Evidence |
| --- | --- | --- |
| Masculine-coded wording | Step 1 and 2 | **Strong.** Gaucher et al. (2011), five studies |
| Long must-have lists | More than about six "must have" items; nice-to-haves listed as must-haves | **Weak.** The claim that women apply only if they meet 100% of criteria traces to an internal HP report that was never published. Say this if you raise it |
| Gendered terms | "He" or "his" for the candidate; "guys", "chairman", "salesman", "manpower" | **Practitioner advice**, widely adopted. Easy fix: "you", "they", or the role name |
| 'Rockstar', 'ninja', 'crush it', 'work hard, play hard' | Bro-culture and conquest language | **Practitioner advice**, not tested research. Overlaps with the coded list |
| Narrow proxies | Degree from a "top" university, years-of-experience floors | **Plausible.** These filter on background, not ability. Ask whether the job really needs them |
| No flexibility or pay | No mention of flexible or part-time working; no salary range | **Practitioner advice.** Often recommended for widening the pool. Don't cite figures you can't source |
| Perks that signal one crowd | Beer fridge, ping-pong, drinks culture as the only perks | **Practitioner advice** |

If you're unsure of a source, say "commonly advised" rather than inventing a
citation.

### 4. Suggest rewrites

For each coded phrase you kept, offer a concrete alternative that keeps the
meaning. Change the framing from what the person *is* to what the job *does*.

| Instead of | Try |
| --- | --- |
| A driven, competitive self-starter | Someone who enjoys setting their own goals and seeing them through |
| Lead the charge on our platform | Shape and look after our core platform |
| Defend your opinions | Make your case and change your mind when the evidence does |
| Dominate the market | Grow our share of the market |
| Must have 8+ years | Experience building distributed systems at scale |

Don't strip out every masculine-coded word. "Lead" in "lead a team of four" is
the job. Aim for balance and plain description.

Ask before rewriting the whole ad. Some people want the review, not a
ghostwriter.

### 5. Report

Use this shape:

```
Verdict: strongly masculine-coded (raw 0 feminine / 15 masculine)
Adjusted: masculine-coded (13 kept; "competitive salary" and one "lead" in a job title discounted)

Biggest issues
1. ...
2. ...

Rewrites
- "..." → "..."

Beyond the word list
- Must-have list of 7 items (evidence: weak; see note)
- ...

Worth asking
- Has anyone outside the hiring team read this ad?
```

End with the question that started this skill: **has anyone who isn't like
you read the ad?** Tools catch words. People catch what the words imply.

## Limits

Say these when they matter:

- The research was done in North America with English-language ads. It
  measured appeal and belonging, not who actually applied.
- The study recruited men and women and compared the two groups. It tells us
  nothing about how non-binary or trans people read these ads. Don't
  extrapolate from it, and don't present the word lists as covering them.
- It says nothing about age, disability, race or class, which ads can also
  signal.
- A balanced score doesn't make an ad good. A fair ad for a badly defined job
  is still a bad ad.
