# inclusive-job-ads

A Claude skill that checks a job ad for gender-coded wording and other signals
that quietly narrow who applies, explains what it found, and suggests rewrites.

## Why

Several years ago every candidate for a role I'd posted was a man. A colleague
asked whether I'd shown the job spec to any women. I hadn't.

The research behind this is Gaucher, Friesen and Kay (2011). Masculine-coded
wording in job ads made the jobs less appealing to women and lowered their
sense of belonging. It didn't change how capable they felt. The ad just told
them the job wasn't for them.

A note on language. "Masculine-coded" and "feminine-coded" describe the
stereotypes a word carries, not the people reading it. The skill reports
"this wording leans on masculine stereotypes", never "this ad is for men".
And because the study only compared men and women, the skill doesn't claim
to know how non-binary or trans people read an ad.

Kat Matfield's [Gender Decoder](https://gender-decoder.katmatfield.com/)
already checks ads against the study's word lists, and it's great. This skill
uses the same lists and the same scoring, then does the parts a word list
can't:

- **Context.** "Competitive salary" isn't the same as "a competitive
  personality". The skill checks every hit and says which ones it discounted.
- **Rewrites.** It suggests plain alternatives that keep the meaning.
- **Beyond the word list.** It looks for gendered terms ("he" for the
  candidate, "guys", "chairman"), must-have lists, narrow proxies, missing pay
  and flexibility, and bro-culture perks. Each finding carries its evidence
  level, because some common advice rests on weak evidence.

## Install

Copy the `inclusive-job-ads` folder into your skills directory:

```bash
git clone https://github.com/kevindavies/inclusive-job-ads.git
cp -r inclusive-job-ads/inclusive-job-ads ~/.claude/skills/
```

In Claude.ai, zip the `inclusive-job-ads` folder and upload it under
Settings > Capabilities > Skills.

Then paste a job ad and ask Claude to check it.

## Run the script on its own

The counting is a small Python script with no dependencies:

```bash
python3 inclusive-job-ads/scripts/decode.py examples/sea-of-dudes.md
```

## Limits

- The research used North American, English-language ads. It measured appeal
  and belonging, not who actually applied.
- The study compared men and women. It tells us nothing about how non-binary
  or trans people read job ads, and the skill says so rather than guess.
- A balanced score doesn't make an ad good.

## Credits

- Danielle Gaucher, Justin Friesen and Aaron C. Kay (2011), "Evidence that
  gendered wording in job advertisements exists and sustains gender
  inequality", *Journal of Personality and Social Psychology* 101(1).
  https://psycnet.apa.org/record/2011-04642-001
- Kat Matfield, [Gender Decoder](https://github.com/lovedaybrooke/gender-decoder).
  The word lists and scoring are hers, used under the MIT licence. See
  [NOTICE](NOTICE).

## Licence

MIT. See [LICENSE](LICENSE).
