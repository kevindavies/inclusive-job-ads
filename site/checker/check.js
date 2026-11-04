// Ad checker: the skill's word count (ported from decode.py, same lists) plus
// simple pattern checks for each guideline. Runs entirely in the browser.
function makeChecker(L) {
  var HYPH = L.communal.concat(L.agentic).filter(function (s) { return s.indexOf('-') > -1; });
  var WORD = /[a-z]+(?:-[a-z]+)*/g;

  function norm(t) { return t.normalize('NFKC').replace(/[‐‑‒­]/g, '-'); }
  function tokens(line) {
    var out = [], m, low = line.toLowerCase();
    WORD.lastIndex = 0;
    while ((m = WORD.exec(low))) {
      var w = m[0];
      if (w.indexOf('-') > -1 && !HYPH.some(function (h) { return w.indexOf(h) === 0; })) {
        var pos = m.index;
        w.split('-').forEach(function (p) { out.push([p, pos, pos + p.length]); pos += p.length + 1; });
      } else out.push([w, m.index, m.index + w.length]);
    }
    return out;
  }
  function all(re, line) {
    var out = [], m; re.lastIndex = 0;
    while ((m = re.exec(line))) { out.push([m.index, m.index + m[0].length, m[0]]); if (!m[0].length) re.lastIndex++; }
    return out;
  }
  var FIXED = new RegExp(L.fixed.replace(/\\w/g, '[\\p{L}\\p{N}_]'), 'giu');
  var PAY = new RegExp(L.pay, 'g');
  var PAYW = new RegExp(L.payWords, 'i');

  function hits(lines, stems) {
    var found = [];
    lines.forEach(function (line, n) {
      var spans = all(FIXED, line);
      tokens(line).forEach(function (t) {
        if (L.nonCoded.indexOf(t[0]) > -1) return;
        var stem = stems.find(function (s) { return t[0].indexOf(s) === 0; });
        if (!stem) return;
        var fx = spans.find(function (s) { return s[0] <= t[1] && t[2] <= s[1]; });
        found.push({ word: t[0], line: n, start: t[1], end: t[2], fixed: fx ? fx[2].toLowerCase() : null });
      });
    });
    return found;
  }
  function salaryLike(a) {
    if (/\d\s?[kK]\b/.test(a)) return true;
    return (a.match(/\d[\d,]*(?:\.\d+)?/g) || []).some(function (x) { return parseFloat(x.replace(/,/g, '')) >= 5000; });
  }
  function canonical(a) { return a.toLowerCase().replace(/\s|£|\$|€/g, '').replace(/to|–|—/g, '-'); }

  // Reading checks: plain patterns, so each finding can point at the words.
  var R = {
    age: /\b(?:young|youthful|recent (?:graduate|grad)s?|new grads?|digital natives?|energetic|mature)\b/gi,
    years: /\b\d{1,2}\s?\+?\s?(?:years?|yrs)\b/gi,
    ceiling: /\b(?:no more than|up to|maximum of|max\.?)\s+\d{1,2}\s+(?:years?|yrs)\b/gi,
    gendered: /\b(?:salesm[ae]n|chairm[ae]n|foreman|manpower|craftsman|workman|he\/she|s\/he|he or she|his\/her|his or her|guys|he|him|his)\b/gi,
    physical: /\b(?:must be able to lift|heavy lifting|physically fit|fit and active|on your feet(?: a lot| all day)?|able[- ]bodied|stand for long periods|(?:full (?:uk )?|clean )?driving licen[cs]e|driver['’]?s licen[cs]e|own (?:car|transport))\b/gi,
    adjust: /\b(?:reasonable adjustments?|adjustments?|accommodations?|accessib\w*|access needs|what would help you|let us know (?:if|what) you need|tell us (?:if|what) you need)\b/i,
    flex: /\b(?:flexib\w*|part[- ]time|hybrid|remote(?:ly)?|compressed hours|job[- ]shar\w*|school (?:run|pick-?ups?)|core hours|work(?:ing)? from home|four[- ]day|4[- ]day|\d days? (?:a|per) week|term[- ]time)\b/gi,
    hype: /\b(?:rock ?stars?|ninjas?|gurus?|unicorns?|superstars?|wizards?|work hard,? play hard|beer fridge|beers?|drinks|ping[- ]pong|hit the ground running|crush(?:ing)? (?:it|targets)|smash(?:ing)? (?:it|targets))\b/gi,
    proxy: /\b(?:top (?:university|universities|tier university)|russell group|ivy league|oxbridge|first[- ]class degree|2:1)\b/gi,
    claim: /\b(?:we value diversity|equal opportunit\w*|diverse and inclusive|committed to diversity)\b/i,
    reqHead: /^\s*(?:#+\s*)?(?:requirements|what matters most|essential\w*|must[- ]haves?|what you(?:['’]ll)? need|you(?:['’]ll)? (?:have|need)|about you|skills and experience|what we(?:['’]re| are) looking for|who you are|experience)\b/i,
    niceHead: /\b(?:nice to have|nice-to-have|desirable|bonus|would be great|great if you)\b/i,
    bullet: /^\s*(?:[-*•]|\d+[.)])\s+/
  };

  return function check(text) {
    var lines = norm(text).split(/\r?\n/);
    var marks = [];
    function mark(line, s, e, g, why) { marks.push({ line: line, start: s, end: e, g: g, why: why }); }
    function scan(re, g, why) {
      var found = [];
      lines.forEach(function (l, n) { all(re, l).forEach(function (h) { found.push(h[2]); mark(n, h[0], h[1], g, why); }); });
      return found;
    }
    function uniq(a) { var o = [], k = []; a.forEach(function (x) { if (k.indexOf(x.toLowerCase()) < 0) { k.push(x.toLowerCase()); o.push(x); } }); return o; }
    function q(a) { return a.map(function (x) { return '“' + x + '”'; }).join(', '); }
    var nonEmpty = lines.map(function (l, i) { return l.trim() ? i : -1; }).filter(function (i) { return i > -1; });
    var words = lines.reduce(function (n, l) { return n + tokens(l).length; }, 0);
    var res = [];

    // 1 Pay
    var figs = {}, competitive = false;
    lines.forEach(function (l, n) {
      all(PAY, l).forEach(function (h) { if (salaryLike(h[2])) { figs[canonical(h[2])] = figs[canonical(h[2])] || h[2].trim(); mark(n, h[0], h[1], 1, 'pay'); } });
      if (/competitive (?:salary|pay|package)/i.test(l)) competitive = true;
    });
    var f = Object.keys(figs).map(function (k) { return figs[k]; });
    var negotiable = /\bnegotiable\b/i.test(lines.join('\n').replace(/\[[^\]]*\]/g, ''));
    if (!f.length) res.push(['look', competitive ? 'Says “competitive salary” but gives no figure.' : 'No salary figure.']);
    else if (f.length > 1) res.push(['look', 'Gives ' + f.length + ' different figures: ' + f.join(' and ') + '. Pick one range.']);
    else if (!negotiable) res.push(['look', 'Gives ' + f[0] + ', but doesn’t say whether it’s negotiable.']);
    else res.push(['ok', 'Gives ' + f[0] + ', and says whether it’s negotiable.']);

    // 2 Flexibility
    var firstFlex = -1, flexWords = [];
    lines.forEach(function (l, n) { all(R.flex, l).forEach(function (h) { if (firstFlex < 0) firstFlex = n; flexWords.push(h[2]); mark(n, h[0], h[1], 2, 'flex'); }); });
    if (firstFlex < 0) res.push(['look', 'No mention of flexibility: hours, location or how people work.']);
    else {
      var rank = nonEmpty.indexOf(firstFlex) / Math.max(1, nonEmpty.length);
      if (rank > 0.4) res.push(['look', 'Mentions ' + q(uniq(flexWords).slice(0, 2)) + ', but not until the bottom half. Say it near the top, and be specific.']);
      else res.push(['ok', 'Mentions ' + q(uniq(flexWords).slice(0, 2)) + ' near the top. Check it’s specific.']);
    }

    // 3 Age
    // Like the skill: age words, experience ceilings and long floors (7+ years). A short floor is a note under 5.
    var age = uniq(scan(R.age, 3, 'age')), ceil = uniq(scan(R.ceiling, 3, 'age'));
    var longYrs = [], shortYrs = [];
    lines.forEach(function (l, n) { all(R.years, l).forEach(function (h) {
      var long = parseInt(h[2], 10) >= 7;
      (long ? longYrs : shortYrs).push(h[2]); mark(n, h[0], h[1], long ? 3 : 5, long ? 'age' : 'years');
    }); });
    longYrs = uniq(longYrs); shortYrs = uniq(shortYrs);
    var p3 = [];
    if (age.length) p3.push('Age-coded words: ' + q(age) + '.');
    if (ceil.length) p3.push('An experience ceiling: ' + q(ceil) + '. It can shut out older applicants.');
    if (longYrs.length) p3.push('Asks for ' + q(longYrs) + '. A long floor can shut out younger applicants. Say what those years should prove.');
    res.push(p3.length ? ['look', p3.join(' ')] : ['ok', 'No age-coded words, experience ceilings or long experience floors found.']);

    // 4 Adjustments
    var phys = uniq(scan(R.physical, 4, 'physical'));
    var adj = R.adjust.test(lines.join('\n'));
    var p4 = [];
    if (phys.length) p4.push('Asks for ' + q(phys) + '. Is it needed for the job?');
    if (!adj) p4.push('No offer of adjustments for applying or interviewing.');
    res.push(p4.length ? ['look', p4.join(' ')] : ['ok', 'Offers adjustments, and no physical requirements found.']);

    // 5 Must-haves
    var count = -1, nice = false;
    for (var i = 0; i < lines.length; i++) {
      if (R.niceHead.test(lines[i])) nice = true;
      if (count < 0 && R.reqHead.test(lines[i]) && !R.bullet.test(lines[i])) {
        count = 0;
        for (var j = i + 1; j < lines.length; j++) {
          var l = lines[j];
          if (!l.trim()) continue;
          if (R.bullet.test(l)) { count++; continue; }
          if (/^\s+\S/.test(l)) continue; // a bullet's continuation line
          break;
        }
      }
    }
    var proxy = uniq(scan(R.proxy, 5, 'proxy'));
    var p5 = [];
    if (count > 5) p5.push(count + ' must-haves' + (nice ? '.' : ', and no “nice to have” list.') + ' Keep three to five essentials.');
    if (proxy.length) p5.push(q(proxy) + ' stands in for a skill.');
    var n5 = shortYrs.length ? 'Asks for ' + q(shortYrs) + '. That’s fine, though saying what the experience should prove is clearer.' : '';
    if (p5.length) res.push(['look', p5.join(' '), n5]);
    else if (count < 0) res.push(['read', 'Couldn’t find a requirements list. Count the must-haves yourself.', n5]);
    else res.push(['ok', count + ' must-haves. That’s a sensible number.', n5]);

    // 6 Describe the job, not the person (Kat Matfield's word lists)
    var a = hits(lines, L.agentic), c = hits(lines, L.communal);
    var aKept = a.filter(function (h) { return !h.fixed; }), cKept = c.filter(function (h) { return !h.fixed; });
    aKept.forEach(function (h) { mark(h.line, h.start, h.end, 6, 'trait'); });
    var set = uniq(a.concat(c).filter(function (h) { return h.fixed; }).map(function (h) { return h.fixed; }));
    var gend = uniq(scan(R.gendered, 6, 'gendered'));
    var p6 = [];
    if (gend.length) p6.push('Gendered wording: ' + q(gend) + '. Use “you”, “they” or the role name.');
    if (aKept.length) p6.push('Trait words: ' + q(uniq(aKept.map(function (h) { return h.word; }))) + '. Keep only the ones the job needs.');
    var wc = aKept.length + ' agentic and ' + cKept.length + ' communal trait words' + (set.length ? ', after setting aside ' + q(set.slice(0, 4)) + (set.length > 4 ? ' and others' : '') + ' as fixed terms' : '') + '.';
    res.push(p6.length ? ['look', p6.join(' '), wc] : ['ok', 'No gendered wording or agentic trait words found.', wc]);

    // 7 Show, don't claim
    var hype = uniq(scan(R.hype, 7, 'hype'));
    var claim = R.claim.test(lines.join('\n'));
    if (hype.length) res.push(['look', 'Hype or drinks culture: ' + q(hype) + '.']);
    else if (claim) res.push(['read', 'Claims values. Does it also show how people really work?']);
    else res.push(['read', 'Can’t tell from the words. Does it show what working there is like?']);

    return { results: res, marks: marks, lines: lines, words: words, empty: !text.trim() };
  };
}
if (typeof module !== 'undefined') module.exports = makeChecker;
