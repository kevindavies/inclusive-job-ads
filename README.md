# inclusive-job-ads

A Claude skill that helps you write a job ad, or reviews one the way a
thoughtful colleague would. It finds what draws people in and what quietly
tells some of them "you won't fit in", then suggests specific, kind fixes.

See it in action: https://kevindavies.github.io/inclusive-job-ads/

Download it for Claude: [inclusive-job-ads.zip](https://github.com/kevindavies/inclusive-job-ads/releases/latest/download/inclusive-job-ads.zip), then see
[Install](#install).

## Why

Several years ago every candidate for a role I'd posted was a man. A colleague
asked whether I'd shown the job spec to any women. I hadn't.

The research that explains it is about belonging. In [Gaucher, Friesen and
Kay's 2011 experiments](https://doi.org/10.1037/a0022530), masculine-coded wording made jobs less appealing to
women, and the reason wasn't ability. The ad wasn't saying "you can't do
this". It was saying "you won't fit in".

Word choice turned out to be only part of it. The strongest field evidence on
who actually applies is about other things: whether the ad states pay,
whether flexibility is [real and specific](https://doi.org/10.1086/711226),
and whether the wording [quietly says "young"](https://doi.org/10.1086/733492). So this skill checks those first.

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

## Install

### Claude, on the web or the desktop app

1. Download [inclusive-job-ads.zip](https://github.com/kevindavies/inclusive-job-ads/releases/latest/download/inclusive-job-ads.zip). Don't unzip it.
2. In Claude, open Customize > Skills. Click +, then Create skill > Upload a
   skill, and choose the zip.
3. Ask Claude to help you write a job ad, or paste one and ask for a review.

Skills need code execution, which is under Settings > Capabilities. On a Team
or Enterprise plan, whoever runs your Claude account turns it on. If the menus
have moved, see
[Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

### ChatGPT, Gemini and Copilot

Copy the long prompt from [PROMPT.md](PROMPT.md) and paste it into the
tool's standing instructions:

- **ChatGPT:** a Project's instructions, or a custom GPT.
- **Gemini:** a Gem, or a skill if your Gemini app has them.
- **Microsoft 365 Copilot:** an agent's instructions.

ChatGPT and the Gemini app are starting to take skill files too. Where yours
does, you can upload the same zip instead. We haven't tested either route
yet. If you try one, please
[tell us how it went](https://github.com/kevindavies/inclusive-job-ads/issues/new?template=tested-in.md).

### The AI in your applicant tracking system

Most of these write the ad for you, and offer a short "guidelines" or "tone"
box. Paste in the short prompt from [PROMPT.md](PROMPT.md). It's under 1,000
characters.

### For developers

Claude Code:

```bash
git clone https://github.com/kevindavies/inclusive-job-ads.git
cp -r inclusive-job-ads/inclusive-job-ads ~/.claude/skills/
```

Gemini CLI, GitHub Copilot and OpenAI Codex all read `~/.agents/skills/`:

```bash
mkdir -p ~/.agents/skills
cp -r inclusive-job-ads/inclusive-job-ads ~/.agents/skills/
```

Each also has its own folder if you prefer:
[`~/.gemini/skills/`](https://geminicli.com/docs/cli/skills/),
[`~/.copilot/skills/`](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)
or a repo's `.agents/skills/` for
[Codex](https://learn.chatgpt.com/docs/build-skills). These are untested so
far. The word-count script needs Python; without it, the skill says so and
does the reading checks only.

## A note on language

The word lists sort words into **agentic** (competing, leading, standing
alone) and **communal** (working with and looking after others). The Gender
Decoder calls these masculine-coded and feminine-coded, after the stereotypes
they carry. Both describe stereotypes, not people. Anyone can be either.

Caring words aren't a problem to balance away. The skill never suggests
cutting them to even a score. It asks whether each agentic trait is something
the job really needs.

Most of the research compared women and men. A [large 2025
study](https://doi.org/10.1073/pnas.2409854122) found the effect follows how strongly someone identifies with masculine stereotypes, not
sex alone. A [first study of trans and non-binary job
seekers](https://doi.org/10.1111/josi.70065) found inclusive wording read as a
sign of safety. That's a start, not a settled answer, and
the skill says so.

## How strong is the evidence?

Mixed, and the skill is honest about it.

- **Field evidence on real applications:** [stating pay and whether it's
  negotiable](https://doi.org/10.1287/mnsc.2014.1994), [advertising
  flexibility](https://www.gov.uk/government/publications/encouraging-employers-to-advertise-jobs-as-flexible),
  and [avoiding age-stereotyped wording](https://doi.org/10.1086/733492).
- **Contested:** gendered trait words. [One large
  study](https://doi.org/10.1073/pnas.2409854122) found swapping them raised
  applications from women. [Another, of about 300,000
  postings](https://doi.org/10.1287/mnsc.2023.4674), found negligible effects.
- **Untested:** many common tips, including "apply even if you don't meet
  every requirement". The popular claim that women only apply when they meet
  100% of requirements traces to an unpublished report, and [a UK
  trial](https://www.bi.team/wp-content/uploads/2022/03/Gender-differences-in-response-to-requirements-in-job-adverts-March-2022.pdf)
  found a much smaller gap.

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

## Run the script on its own

No dependencies:

```bash
python3 inclusive-job-ads/scripts/decode.py examples/before.md
python3 -m unittest discover tests
```

## For B Corps

[B Lab's Standards v2.1](https://www.bcorporation.net/en-us/standards/performance-requirements/)
include "The company implements inclusive hiring practices"
([JEDI2.g](https://kb.bimpactassessment.net/en/support/solutions/articles/43000760403)) as one of the actions a company can choose. If yours has
chosen it, this skill gives you a repeatable review of your job ads, and a
record you can keep. It's independent of B Lab and doesn't certify anything.

## Limits

- Much of the research measured appeal or intentions, not who applied, and
  most of it comes from North America and Europe.
- It's not legal advice. Where wording carries legal risk, the skill says so
  and points to the local regulator's guidance, such as
  [ACAS](https://www.acas.org.uk/recruitment/how-to-advertise-a-job) and
  [the EHRC](https://www.equalityhumanrights.com/guidance/guidance-discriminatory-adverts)
  in the UK or [the EEOC](https://www.eeoc.gov/prohibited-employment-policiespractices)
  in the US.
- The word lists are English only.
- A welcoming ad for a badly defined job is still a bad ad.
- This isn't designed to make a bad job sound good.
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

## Feedback

Used it? [Email inclusive-job-ads@beaks.co](mailto:inclusive-job-ads@beaks.co?subject=inclusive-job-ads%3A%20how%20it%20went&body=Which%20tool%20did%20you%20use%20%28Claude%2C%20ChatGPT%2C%20Gemini%2C%20Copilot%20or%20something%20else%29%3F%0A%0A%0AWhat%20worked%3F%0A%0A%0AWhat%20felt%20off%3F%0A%0A%0A%28Please%20only%20include%20ad%20text%20if%20the%20ad%20is%20already%20public.%29%0A) and say which tool you used,
what worked and what felt off. Please only include ad text if the ad is
already public. If you're on GitHub,
[an issue](https://github.com/kevindavies/inclusive-job-ads/issues/new?template=tested-in.md)
works too.

## Security

The skill treats the ad as data, never as instructions, and its script reads
one file, writes nothing and makes no network calls. See
[SECURITY.md](SECURITY.md) for the threat model and how to report a problem.

## Licence

MIT. See [LICENSE](LICENSE).
