# inclusive-job-ads

A Claude skill that helps you write a job ad, or reviews one the way a
thoughtful colleague would. It finds what draws people in and what quietly
tells some of them "you won't fit in", then suggests specific, kind fixes.

## Why

Several years ago every candidate for a role I'd posted was a man. A colleague
asked whether I'd shown the job spec to any women. I hadn't.

The research that explains it is about belonging. In Gaucher, Friesen and
Kay's 2011 experiments, masculine-coded wording made jobs less appealing to
women, and the reason wasn't ability. The ad wasn't saying "you can't do
this". It was saying "you won't fit in".

Word choice turned out to be only part of it. The strongest field evidence on
who actually applies is about other things: whether the ad states pay,
whether flexibility is real and specific, and whether the wording quietly
says "young". So this skill checks those first.

It also looks for the opposite signal, the lines that tell someone they'd
belong. "Need to duck out for school pick-ups? We do too." does more than any
diversity statement.

## Who it's for

Anyone who writes job ads: a founder hiring their first employee, a charity,
a B Corp, or a global employer with a library of templates. Large employers
get the most from it, because fixing one template fixes every ad built on it.

## What it does

1. **Counts trait words.** A small script uses the word lists from Kat
   Matfield's [Gender Decoder](https://gender-decoder.katmatfield.com/), and
   tags likely false alarms like "competitive salary", "customer support" and
   "Active Directory" instead of silently counting them.
2. **Reads for signals, strongest evidence first:** pay, flexibility, age
   wording, disability, requirement lists, gendered terms, agentic trait
   words, culture and perks.
3. **Says what's working** before what isn't, and caps the changes at three.
4. **Reads the ad as different people:** a carer, someone over 50, someone
   who'd need an adjustment, someone who's never negotiated pay.
5. **Suggests rewrites** that describe the job, not the person.
6. **Labels every finding** with its evidence: field trial, legal risk,
   contested, lab study, guidance or untested.

It can also compare two versions of an ad, which catches trade-offs. An ad can
get warmer and lose its salary in the same edit.

Ask Claude to write a job ad and the skill kicks in there too, whether or not
you mention inclusion. It puts pay and flexibility near the top, keeps the
must-haves short, describes the job rather than the person, and uses
placeholders instead of inventing a salary. Then it checks its own draft.

## A note on language

The word lists sort words into **agentic** (competing, leading, standing
alone) and **communal** (working with and looking after others). The Gender
Decoder calls these masculine-coded and feminine-coded, after the stereotypes
they carry. Both describe stereotypes, not people. Anyone can be either.

Caring words aren't a problem to balance away. The skill never suggests
cutting them to even a score. It asks whether each agentic trait is something
the job really needs.

Most of the research compared women and men. A large 2025 study found the
effect follows how strongly someone identifies with masculine stereotypes, not
sex alone. A first study of trans and non-binary job seekers found inclusive
wording read as a sign of safety. That's a start, not a settled answer, and
the skill says so.

## How strong is the evidence?

Mixed, and the skill is honest about it.

- **Field evidence on real applications:** stating pay and whether it's
  negotiable, advertising flexibility, and avoiding age-stereotyped wording.
- **Contested:** gendered trait words. One large study found swapping them
  raised applications from women. Another, of about 300,000 postings, found
  negligible effects.
- **Untested:** many common tips, including "apply even if you don't meet
  every requirement". The popular claim that women only apply when they meet
  100% of requirements traces to an unpublished report, and a UK trial found
  a much smaller gap.

Every citation is in
[`references/evidence.md`](inclusive-job-ads/references/evidence.md), checked
against Crossref.

## Examples

| Ad | Review | What it shows |
| --- | --- | --- |
| [sea-of-dudes](examples/sea-of-dudes.md) | [review](examples/sea-of-dudes-review.md) | The obvious case |
| [before](examples/before.md) | [review](examples/before-review.md) | Two different salaries, twelve must-haves |
| [before](examples/before.md) and [after](examples/after.md) | [comparison](examples/before-after-review.md) | A rewrite that gets warmer and loses its salary |
| [false-alarms](examples/false-alarms.md) | [review](examples/false-alarms-review.md) | Leans communal on raw count, nearly empty after context |
| [balanced-but-not-fine](examples/balanced-but-not-fine.md) | [review](examples/balanced-but-not-fine-review.md) | A balanced word count on an ad with real problems |
| [injection](examples/injection.md) | [review](examples/injection-review.md) | Hidden instructions to the AI, flagged and ignored |
| [brief](examples/write-brief.md) | [written ad](examples/write-brief-ad.md) | A thin brief turned into an ad, with placeholders, not invented facts |

The reviews and the written ad were produced by Claude following the skill, with no other briefing.

## Install

Copy the `inclusive-job-ads` folder into your skills directory:

```bash
git clone https://github.com/kevindavies/inclusive-job-ads.git
cp -r inclusive-job-ads/inclusive-job-ads ~/.claude/skills/
```

In Claude.ai, zip the `inclusive-job-ads` folder and upload it under
Settings > Capabilities > Skills.

Then ask Claude to write a job ad, or paste one and ask it to review it.

## Run the script on its own

No dependencies:

```bash
python3 inclusive-job-ads/scripts/decode.py examples/before.md
python3 -m unittest discover tests
```

## For B Corps

B Lab's Standards v2.1 include "The company implements inclusive hiring
practices" (JEDI2.g) as one of the actions a company can choose. If yours has
chosen it, this skill gives you a repeatable review of your job ads, and a
record you can keep. It's independent of B Lab and doesn't certify anything.

## Limits

- Much of the research measured appeal or intentions, not who applied, and
  most of it comes from North America and Europe.
- It's not legal advice. Where wording carries legal risk, the skill says so
  and points to the local regulator's guidance, such as ACAS and the EHRC in
  the UK or the EEOC in the US.
- The word lists are English only.
- A welcoming ad for a badly defined job is still a bad ad.
- Tools catch words. People catch what the words imply. Ask someone who'd
  read it differently from you.

## Credits

- Kat Matfield, [Gender Decoder](https://github.com/lovedaybrooke/gender-decoder).
  The word lists and thresholds are hers, used under the MIT licence. See
  [NOTICE](NOTICE). This script counts each word once, so a few totals differ
  slightly from hers.
- Danielle Gaucher, Justin Friesen and Aaron C. Kay (2011), "Evidence that
  gendered wording in job advertisements exists and sustains gender
  inequality", *Journal of Personality and Social Psychology* 101(1),
  109-128. https://doi.org/10.1037/a0022530
- The other studies are listed in
  [`references/evidence.md`](inclusive-job-ads/references/evidence.md).

## Security

The skill treats the ad as data, never as instructions, and its script reads
one file, writes nothing and makes no network calls. See
[SECURITY.md](SECURITY.md) for the threat model and how to report a problem.

## Licence

MIT. See [LICENSE](LICENSE).
