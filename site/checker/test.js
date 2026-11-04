// Tests for the checker's own rules (the ones decode.py doesn't have).
// Run: node site/checker/test.js
const cp = require('child_process'), path = require('path'), assert = require('assert');
const check = require('./check.js')(JSON.parse(cp.execFileSync('python3', [path.join(__dirname, 'wordlists.py'), '--json'])));
const r = t => check(t).results;
let n = 0;
function t(name, fn) { fn(); n++; console.log('OK  ' + name); }

t('#2 flexibility asked of the candidate is not an offer', () => {
  const x = r('Salary £30k.\nYou must have the flexibility to work evening shifts at short notice.')[1];
  assert.strictEqual(x[0], 'look');
  assert.match(x[1], /doesn’t say what flexibility the job offers/);
});
t('#2 an offer next to a demand still counts as an offer', () => {
  const x = r('Flexible hours, core hours 10 to 3.\nYou need to be willing to show flexibility at month end.\nMore.\nMore.')[1];
  assert.match(x[1], /Mentions “Flexible”/);
  assert.match(x[1], /demand, not an offer/);
});
t('#2 plain flexible working still counts', () => {
  assert.strictEqual(r('Flexible working from day one.\nMore.\nMore.')[1][0], 'ok');
});
t('#4 nine-day fortnight and friends count as flexibility', () => {
  for (const s of ['We work a nine-day fortnight.', 'Flexitime for everyone.', 'Flexi-time', 'School hours only', 'Annualised hours', 'Work from anywhere in the UK'])
    assert.doesNotMatch(r(s)[1][1], /No mention of flexibility/, s);
});
t('#5 experience floors in words are read', () => {
  assert.match(r('Fifteen years of experience in retail management.')[2][1], /long floor/);
  assert.strictEqual(r('Three years of experience.')[2][0], 'ok');
  assert.match(r('Requirements\n- Three years of experience\n')[4][2], /Three years/);
});
t('long numeric floor still flagged', () => {
  assert.match(r('8+ years building systems')[2][1], /long floor/);
});
t('#6 a plain degree requirement gets a question', () => {
  assert.match(r('Requirements\n- A degree in business or a related subject\n- Excel')[4][2], /Does the job need one/);
  assert.strictEqual(r('Requirements\n- Excel\n\nNice to have\n- A degree')[4][2], '');
});
t('coffee on shift is not drinks culture', () => {
  assert.doesNotMatch(r('Staff discount and free drinks on shift')[6][1], /drinks/);
  assert.match(r('Friday drinks and a beer fridge')[6][1], /Friday drinks/);
});
t('an adjustments offer split across lines still counts', () => {
  assert.strictEqual(r('£30k, negotiable.\nTell us what would\nhelp you at interview.')[3][0], 'ok');
});
t('"What we need" is a requirements heading', () => {
  assert.match(r('What we need\n- A\n- B\n- C\n- D\n- E\n- F')[4][1], /6 must-haves/);
});
console.log(n + ' checker tests passed');
