"""Write decode.py's word lists and patterns into the page, so the browser checker
and the skill's script count the same way. Usage: wordlists.py PAGE"""
import importlib.util, json, pathlib, re, sys
repo = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('decode', repo / 'inclusive-job-ads/scripts/decode.py')
d = importlib.util.module_from_spec(spec); spec.loader.exec_module(d)
data = {
    "communal": d.COMMUNAL, "agentic": d.AGENTIC, "nonCoded": sorted(d.NON_CODED_EXCEPTIONS),
    "fixed": "|".join(d.LIKELY_FIXED), "pay": d.PAY_RE.pattern, "payWords": d.PAY_WORDS.pattern,
    "rate": d.RATE_AFTER.pattern, "notPayBefore": d.NOT_PAY_BEFORE.pattern, "notPayAfter": d.NOT_PAY_AFTER.pattern,
}
blob = json.dumps(data, ensure_ascii=False)
if sys.argv[1:] == ["--json"]:
    print(blob); sys.exit(0)
assert '</' not in blob
page = pathlib.Path(sys.argv[1]); s = page.read_text()
new, n = re.subn(r'(<script type="application/json" id="wordlists">).*?(</script>)',
                 lambda m: m.group(1) + blob + m.group(2), s, flags=re.S)
assert n == 1, 'marker not found'
js = (pathlib.Path(__file__).parent / 'check.js').read_text()
new, n = re.subn(r'/\*CHECKER\*/.*?/\*/CHECKER\*/', lambda m: '/*CHECKER*/\n' + js + '/*/CHECKER*/', new, flags=re.S)
assert n == 1, 'checker marker not found'
EXAMPLES = [("before", "A typical draft"), ("cafe-shifts", "Café shifts"),
            ("balanced-but-not-fine", "Warm but not fine"), ("after", "The rewrite"), ("good", "A good one")]
def plain(md):
    """Headings lose their #s and hard-wrapped paragraphs are joined, so it reads like a pasted ad."""
    md = re.sub(r'^#+\s*', '', md.strip(), flags=re.M)
    out = []
    for block in md.split('\n\n'):
        ls = block.split('\n')
        if any(re.match(r'\s*(?:[-*]|\d+\.)\s', l) for l in ls):
            joined = []
            for l in ls:
                if joined and re.match(r'\s+\S', l): joined[-1] += ' ' + l.strip()
                else: joined.append(l)
            out.append('\n'.join(joined))
        else:
            out.append(' '.join(l.strip() for l in ls))
    return '\n\n'.join(out)
ex = [{"id": i, "label": lab, "text": plain((repo / 'examples' / (i + '.md')).read_text())} for i, lab in EXAMPLES]
eblob = json.dumps(ex, ensure_ascii=False)
assert '</' not in eblob
new, n = re.subn(r'(<script type="application/json" id="examples">).*?(</script>)', lambda m: m.group(1) + eblob + m.group(2), new, flags=re.S)
assert n == 1, 'examples marker not found'
# The box starts empty: people come here with an ad to check.
new, n = re.subn(r'(<textarea id="chk-text"[^>]*>).*?(</textarea>)', lambda m: m.group(1) + m.group(2), new, flags=re.S)
assert n == 1
page.write_text(new)
print('wordlists written:', len(d.COMMUNAL), 'communal,', len(d.AGENTIC), 'agentic')
