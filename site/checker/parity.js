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
process.exit(bad ? 1 : 0);
