// Checks the browser checker counts trait words and salary figures the same way
// as the skill's script, on every example ad. Run: node site/checker/parity.js
const fs = require('fs'), cp = require('child_process'), path = require('path');
const root = path.resolve(__dirname, '../..');
const lists = JSON.parse(cp.execFileSync('python3', [path.join(__dirname, 'wordlists.py'), '--json']));
const check = require('./check.js')(lists);
const dir = path.join(root, 'examples');
let bad = 0;
for (const f of fs.readdirSync(dir).filter(f => !f.includes('review') && f.endsWith('.md'))) {
  const file = path.join(dir, f);
  const py = JSON.parse(cp.execFileSync('python3', [path.join(root, 'inclusive-job-ads/scripts/decode.py'), file]));
  const r = check(fs.readFileSync(file, 'utf8'));
  const want = `${py.script_adjusted.agentic} agentic and ${py.script_adjusted.communal} communal`;
  const words = r.results[5][2].startsWith(want);
  const figs = py.pay.salary_figures.length;
  const pay = figs === 0 ? /No salary figure|competitive salary/.test(r.results[0][1])
    : figs > 1 ? r.results[0][1].includes(`${figs} different figures`) : r.results[0][1].includes(py.pay.salary_figures[0]);
  const ok = words && pay;
  if (!ok) bad++;
  console.log(`${ok ? 'OK' : 'FAIL'}  ${f.padEnd(28)} ${want}, ${figs} salary figure(s)`);
}
// Single-line cases from the issues: both must find the same salary figures.
const CASES = [
  '£12.50 per hour, 16 to 24 hours a week', 'Pay: £11.44 an hour plus tips', '£12-£13/hour', '£95 a day', '£12.21ph',
  "Salary £30k, negotiable. You'll manage a £50k marketing budget.", "Salary £30k. You'll look after a budget of £50k.",
  '£28,000. A learning budget of £1,000 a year',
];
for (const t of CASES) {
  const py = JSON.parse(cp.execFileSync('python3', [path.join(root, 'inclusive-job-ads/scripts/decode.py')], { input: t }));
  const figs = py.pay.salary_figures, res = check(t).results[0][1];
  const ok = figs.length === 0 ? /No salary figure/.test(res) : figs.length > 1 ? res.includes(figs.length + ' different') : res.includes(figs[0]);
  if (!ok) bad++;
  console.log(`${ok ? 'OK' : 'FAIL'}  case: ${t.slice(0, 40).padEnd(40)} py ${JSON.stringify(figs)} | js ${res.slice(0, 50)}`);
}
process.exit(bad ? 1 : 0);
