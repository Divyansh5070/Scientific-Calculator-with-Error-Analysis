/**
 * Scientific Calculator with Error Analysis — Web Edition
 * Authors: Divyansh Sharma · Jiya Madan · Kabir Bajaj
 * Numerical Methods Project
 */

'use strict';

/* ═══════════════════════════════════════════════
   STATE
   ═══════════════════════════════════════════════ */
let expr    = '';
let memory  = 0;
let history = [];
let reportLines = [];

/* ═══════════════════════════════════════════════
   MATH ENGINE  (mirrors Python Calc class)
   ═══════════════════════════════════════════════ */
const Calc = {
  /* Basic errors */
  absolute : (t, a)      => Math.abs(t - a),
  relative : (t, a)      => t === 0 ? Infinity : Math.abs((t - a) / t),
  percent  : (t, a)      => Calc.relative(t, a) * 100,
  roundoff : (v, dp)     => { const f = Math.pow(10, dp); return Math.abs(v - Math.round(v * f) / f); },
  trunc    : (v, dp)     => { const f = Math.pow(10, dp); return Math.abs(v - Math.trunc(v * f) / f); },

  /* Machine epsilon */
  meps: () => {
    let e = 1.0;
    while ((1.0 + e / 2) !== 1.0) e /= 2;
    return e;
  },

  /* Propagation */
  propAdd : (da, db)           => Math.sqrt(da * da + db * db),
  propMul : (a, b, da, db)     => (a === 0 || b === 0) ? 0 : Math.abs(a * b) * Math.sqrt((da/a)**2 + (db/b)**2),
  propDiv : (a, b, da, db)     => { if (b === 0) return Infinity; return a === 0 ? 0 : Math.abs(a / b) * Math.sqrt((da/a)**2 + (db/b)**2); },

  /* Taylor */
  factorial: (n) => { let r = 1; for (let i = 2; i <= n; i++) r *= i; return r; },
  taylor: (fn, x, n) => {
    let exact, approx = 0;
    if (fn === 'sin') {
      exact = Math.sin(x);
      for (let k = 0; k < n; k++) approx += ((-1) ** k) * (x ** (2*k+1)) / Calc.factorial(2*k+1);
    } else if (fn === 'cos') {
      exact = Math.cos(x);
      for (let k = 0; k < n; k++) approx += ((-1) ** k) * (x ** (2*k)) / Calc.factorial(2*k);
    } else {
      exact = Math.exp(x);
      for (let k = 0; k < n; k++) approx += (x ** k) / Calc.factorial(k);
    }
    return { exact, approx, error: Math.abs(exact - approx) };
  },

  /* Significant figures */
  sigfig: (v, n) => {
    if (v === 0) return 0;
    const d = Math.ceil(Math.log10(Math.abs(v)));
    const factor = Math.pow(10, n - d);
    return Math.round(v * factor) / factor;
  },

  /* Expression evaluator */
  evaluate: (exprStr, angleMode) => {
    const toRad = x => angleMode === 'DEG' ? x * Math.PI / 180 : angleMode === 'GRAD' ? x * Math.PI / 200 : x;
    const frRad = r => angleMode === 'DEG' ? r * 180 / Math.PI : angleMode === 'GRAD' ? r * 200 / Math.PI : r;

    // Replace tokens for JS eval
    let e = exprStr
      .replace(/\^/g, '**')
      .replace(/\bsin\(/g,  '_sin(')
      .replace(/\bcos\(/g,  '_cos(')
      .replace(/\btan\(/g,  '_tan(')
      .replace(/\basin\(/g, '_asin(')
      .replace(/\bacos\(/g, '_acos(')
      .replace(/\batan\(/g, '_atan(')
      .replace(/\bsqrt\(/g, '_sqrt(')
      .replace(/\bcbrt\(/g, '_cbrt(')
      .replace(/\blog10\(/g,'_log10(')
      .replace(/\blog2\(/g, '_log2(')
      .replace(/\bln\(/g,   '_ln(')
      .replace(/\bexp\(/g,  '_exp(')
      .replace(/\binv\(/g,  '_inv(')
      .replace(/\bfact\(/g, '_fact(')
      .replace(/\bpi\b/g,   String(Math.PI))
      .replace(/\be\b/g,    String(Math.E));

    const _sin  = x => Math.sin(toRad(x));
    const _cos  = x => Math.cos(toRad(x));
    const _tan  = x => Math.tan(toRad(x));
    const _asin = x => frRad(Math.asin(x));
    const _acos = x => frRad(Math.acos(x));
    const _atan = x => frRad(Math.atan(x));
    const _sqrt = x => Math.sqrt(x);
    const _cbrt = x => Math.cbrt(x);
    const _log10= x => Math.log10(x);
    const _log2 = x => Math.log2(x);
    const _ln   = x => Math.log(x);
    const _exp  = x => Math.exp(x);
    const _inv  = x => 1 / x;
    const _fact = x => Calc.factorial(Math.round(x));

    // eslint-disable-next-line no-new-func
    return Function(
      '_sin','_cos','_tan','_asin','_acos','_atan',
      '_sqrt','_cbrt','_log10','_log2','_ln','_exp','_inv','_fact',
      `"use strict"; return (${e});`
    )(_sin,_cos,_tan,_asin,_acos,_atan,_sqrt,_cbrt,_log10,_log2,_ln,_exp,_inv,_fact);
  }
};

/* ═══════════════════════════════════════════════
   DOM HELPERS
   ═══════════════════════════════════════════════ */
const $ = id => document.getElementById(id);

function getAngle() {
  return document.querySelector('input[name="angle"]:checked').value;
}

function setResult(val) {
  $('result-line').textContent = val;
}

function setExpr(val) {
  $('expr-line').textContent = val || '\u00A0';
}

function formatNum(n) {
  if (!isFinite(n)) return String(n);
  if (Number.isInteger(n) && Math.abs(n) < 1e15) return String(n);
  return parseFloat(n.toPrecision(10)).toString();
}

function formatSci(n, digits = 6) {
  return n.toExponential(digits);
}

function fmtFixed(n, d = 8) {
  return n.toFixed(d);
}

function pad(str, len) {
  return String(str).padStart(len);
}

function rpad(str, len) {
  return String(str).padEnd(len);
}

/* ═══════════════════════════════════════════════
   RENDER OUTPUT BOX (styled lines)
   ═══════════════════════════════════════════════ */
function renderOutput(boxId, lines) {
  const box = $(boxId);
  box.innerHTML = '';
  lines.forEach(line => {
    const el = document.createElement('div');
    if (line.startsWith('═') || line.startsWith('─')) {
      el.className = 'line-sep';
      el.textContent = line;
    } else if (line.includes('  :  ') || line.match(/^  \w.*:\s/)) {
      // Split on first colon
      const idx = line.indexOf(':');
      const k = line.slice(0, idx + 1);
      const v = line.slice(idx + 1);
      const kSpan = document.createElement('span');
      kSpan.className = 'line-key';
      kSpan.textContent = k;
      const vSpan = document.createElement('span');
      vSpan.className = 'line-val';
      vSpan.textContent = v;
      el.appendChild(kSpan);
      el.appendChild(vSpan);
    } else if (line.startsWith('##') || line.startsWith('  Function') || line.startsWith('  Terms')) {
      el.className = 'line-head';
      el.textContent = line;
    } else {
      el.textContent = line;
    }
    box.appendChild(el);
  });
}

/* ═══════════════════════════════════════════════
   CALCULATOR LOGIC
   ═══════════════════════════════════════════════ */
function input(ch) {
  expr += ch;
  setExpr(expr);
  liveEval();
}

function inputFn(name) {
  expr += name + '(';
  setExpr(expr);
}

function clearAll() {
  expr = '';
  setExpr('');
  setResult('0');
}

function backspace() {
  expr = expr.slice(0, -1);
  setExpr(expr);
  liveEval();
}

function negate() {
  if (!expr) return;
  expr = `-(${expr})`;
  setExpr(expr);
  liveEval();
}

function liveEval() {
  try {
    const r = Calc.evaluate(expr, getAngle());
    if (typeof r === 'number') {
      setResult(formatNum(r));
    }
  } catch (_) { /* silently ignore incomplete expressions */ }
}

function calculate() {
  if (!expr) return;
  try {
    const result = Calc.evaluate(expr, getAngle());
    const disp   = typeof result === 'number' ? formatNum(result) : String(result);
    const entry  = `${expr}  =  ${disp}`;
    history.unshift(entry);
    if (history.length > 30) history.pop();
    renderHistory();
    setResult(disp);
    setExpr(expr + ' =');
    expr = disp;
    animateResult();
  } catch (ex) {
    setResult('Error');
    setExpr(String(ex).slice(0, 60));
    logReport(`Error: ${ex}`);
  }
}

function animateResult() {
  const el = $('result-line');
  el.style.transform = 'scale(1.04)';
  el.style.textShadow = '0 0 40px rgba(124,58,237,0.7)';
  setTimeout(() => {
    el.style.transform = '';
    el.style.textShadow = '';
  }, 200);
}

/* ── History ────────────────────────────────── */
function renderHistory() {
  const ul = $('history-list');
  ul.innerHTML = '';
  history.forEach(item => {
    const li = document.createElement('li');
    li.textContent = item;
    li.onclick = () => {
      expr = item.split('  =  ')[0].trim();
      setExpr(expr);
      liveEval();
    };
    ul.appendChild(li);
  });
}

function clearHistory() {
  history = [];
  renderHistory();
}

/* ── Memory ─────────────────────────────────── */
function memStore() {
  try { memory = parseFloat($('result-line').textContent); updateMemDisplay(); } catch (_) {}
}
function memRecall()  { input(String(memory)); }
function memClear()   { memory = 0; updateMemDisplay(); }
function memAdd()     { try { memory += parseFloat($('result-line').textContent); updateMemDisplay(); } catch (_) {} }
function memSub()     { try { memory -= parseFloat($('result-line').textContent); updateMemDisplay(); } catch (_) {} }

function updateMemDisplay() {
  const el = $('mem-display');
  if (memory !== 0) {
    el.textContent = `M: ${parseFloat(memory.toPrecision(6))}`;
    el.style.color = '#22D3EE';
  } else {
    el.textContent = 'M';
    el.style.color = '';
  }
}

/* ── Angle mode radio ───────────────────────── */
document.querySelectorAll('input[name="angle"]').forEach(radio => {
  radio.addEventListener('change', () => {
    document.querySelectorAll('.angle-btn').forEach(l => l.classList.remove('active'));
    radio.closest('.angle-btn').classList.add('active');
    liveEval();
  });
});

/* ── Keyboard support ───────────────────────── */
document.addEventListener('keydown', e => {
  // Allow normal typing in <input> fields
  if (e.target.tagName === 'INPUT') return;

  if (e.key === 'Enter')     { e.preventDefault(); calculate(); return; }
  if (e.key === 'Escape')    { e.preventDefault(); clearAll();  return; }
  if (e.key === 'Backspace') { e.preventDefault(); backspace(); return; }

  if ('0123456789.+-*/%()'.includes(e.key)) {
    e.preventDefault(); input(e.key);
  }
});

/* ═══════════════════════════════════════════════
   TAB SWITCHING
   ═══════════════════════════════════════════════ */
function switchTab(name) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
  $(`tab-${name}`).classList.add('active');
  $(`tab-content-${name}`).classList.add('active');
}

/* ═══════════════════════════════════════════════
   ERROR ANALYSIS TABS
   ═══════════════════════════════════════════════ */

/* ── Tab 1: Basic ─────────────────────────── */
function runBasic() {
  const tv = parseFloat($('basic-tv').value);
  const av = parseFloat($('basic-av').value);
  const dp = parseInt($('basic-dp').value) || 5;

  if (isNaN(tv) || isNaN(av)) { alert('Please enter valid numbers for True and Approx values.'); return; }

  const ae  = Calc.absolute(tv, av);
  const re  = Calc.relative(tv, av);
  const pe  = Calc.percent(tv, av);
  const ro  = Calc.roundoff(av, dp);
  const te  = Calc.trunc(av, dp);
  const acc = re > 0 ? Math.floor(-Math.log10(re)) : '∞';

  const lines = [
    '═══════════════════════════════════════',
    `  True Value       :  ${tv}`,
    `  Approx Value     :  ${av}`,
    `  Decimal Places   :  ${dp}`,
    '───────────────────────────────────────',
    `  Absolute Error   :  ${ae.toExponential(8)}`,
    `  Relative Error   :  ${re.toExponential(8)}`,
    `  Percentage Error :  ${pe.toFixed(6)} %`,
    `  Round-off Error  :  ${ro.toExponential(8)}`,
    `  Truncation Error :  ${te.toExponential(8)}`,
    '───────────────────────────────────────',
    `  Accurate Digits  :  ${acc}`,
    '═══════════════════════════════════════',
  ];
  renderOutput('out-basic', lines);
  logReport(`Basic Errors — AE=${ae.toExponential(4)}  RE=${re.toExponential(4)}  PE=${pe.toFixed(4)}%`);
}

/* ── Tab 2: Propagation ───────────────────── */
function runProp() {
  const a  = parseFloat($('prop-a').value);
  const da = parseFloat($('prop-da').value);
  const b  = parseFloat($('prop-b').value);
  const db = parseFloat($('prop-db').value);
  const op = document.querySelector('input[name="prop-op"]:checked').value;

  if ([a, da, b, db].some(isNaN)) { alert('Please fill in all four fields.'); return; }

  let res, df, sym;
  if      (op === 'add') { res = a + b; df = Calc.propAdd(da, db); sym = '+'; }
  else if (op === 'sub') { res = a - b; df = Calc.propAdd(da, db); sym = '−'; }
  else if (op === 'mul') { res = a * b; df = Calc.propMul(a, b, da, db); sym = '×'; }
  else                   { res = b !== 0 ? a / b : Infinity; df = Calc.propDiv(a, b, da, db); sym = '÷'; }

  const rel = res !== 0 ? df / Math.abs(res) : Infinity;

  const lines = [
    '═══════════════════════════════════════',
    `  Operation    :  ${a}  ${sym}  ${b}`,
    `  Result       :  ${parseFloat(res.toPrecision(8))}`,
    '───────────────────────────────────────',
    `  Delta a      :  ±${da}`,
    `  Delta b      :  ±${db}`,
    `  Prop Error   :  ±${df.toExponential(6)}`,
    `  Range        :  [${(res - df).toPrecision(6)} , ${(res + df).toPrecision(6)}]`,
    `  Relative Err :  ${rel.toExponential(4)}`,
    '───────────────────────────────────────',
    '  Method       :  Quadrature (RSS) Law',
    '═══════════════════════════════════════',
  ];
  renderOutput('out-prop', lines);
  logReport(`Propagation (${sym}): result=${res.toPrecision(6)} ±${df.toExponential(4)}`);
}

/* ── Tab 3: Taylor ────────────────────────── */
function runTaylor() {
  const x  = parseFloat($('taylor-x').value);
  const n  = parseInt($('taylor-n').value);
  const fn = document.querySelector('input[name="taylor-fn"]:checked').value;

  if (isNaN(x)) { alert('x must be a number.'); return; }
  if (n < 1 || n > 20 || isNaN(n)) { alert('Terms must be between 1 and 20.'); return; }

  const { exact } = Calc.taylor(fn, x, n);
  const lines = [
    '══════════════════════════════════════════════════════════',
    `  Function : ${fn}(x)    x = ${x}`,
    `  Exact    : ${exact.toFixed(12)}`,
    '──────────────────────────────────────────────────────────',
    `  ${'Terms'.padStart(5)}   ${'Approximate'.padStart(18)}   ${'Error'.padStart(14)}`,
    '──────────────────────────────────────────────────────────',
  ];
  for (let t = 1; t <= n; t++) {
    const { approx, error } = Calc.taylor(fn, x, t);
    lines.push(`  ${String(t).padStart(5)}   ${approx.toFixed(8).padStart(18)}   ${error.toExponential(6).padStart(14)}`);
  }
  lines.push('══════════════════════════════════════════════════════════');
  renderOutput('out-taylor', lines);
  logReport(`Taylor ${fn}(${x}) — ${n} terms, final error=${Calc.taylor(fn,x,n).error.toExponential(4)}`);
}

/* ── Tab 4: Sig Figs ──────────────────────── */
function runSigfig() {
  const v = parseFloat($('sf-v').value);
  const n = parseInt($('sf-n').value);

  if (isNaN(v)) { alert('Enter a valid number.'); return; }
  if (n < 1 || isNaN(n)) { alert('Significant figures must be ≥ 1.'); return; }

  const rv = Calc.sigfig(v, n);
  const ae = Math.abs(v - rv);
  const re = v !== 0 ? ae / Math.abs(v) : 0;

  const lines = [
    '═══════════════════════════════════════',
    `  Original Value :  ${v}`,
    `  Sig Figures    :  ${n}`,
    '───────────────────────────────────────',
    `  Rounded Value  :  ${rv}`,
    `  Absolute Error :  ${ae.toExponential(6)}`,
    `  Relative Error :  ${re.toExponential(6)}`,
    `  Percentage Err :  ${(re * 100).toFixed(4)} %`,
    '───────────────────────────────────────',
    '  Rounding Table:',
    '───────────────────────────────────────',
  ];
  for (let dp = 1; dp <= 8; dp++) {
    const rv2 = parseFloat(v.toFixed(dp));
    const err = Math.abs(v - rv2);
    lines.push(`  dp=${dp}  →  ${rpad(rv2, 20)}  err=${err.toExponential(2)}`);
  }
  lines.push('═══════════════════════════════════════');
  renderOutput('out-sigfig', lines);
  logReport(`SigFigs(${v}, ${n}) → ${rv}, AE=${ae.toExponential(4)}`);
}

/* ── Tab 5: Machine ε ─────────────────────── */
function initMachine() {
  const eps = Calc.meps();
  const tiles = [
    ['Computed ε (float64)',        eps.toExponential(4)],
    ['IEEE 754 ε (float64)',        '2.2204e-16'],
    ['IEEE 754 ε (float32)',        '1.1921e-07'],
    ['IEEE 754 ε (float16)',        '9.7656e-04'],
    ['Max float64',                 '1.7977e+308'],
    ['Min positive float64',        '5.0000e-324'],
  ];
  const container = $('machine-tiles');
  container.innerHTML = '';
  tiles.forEach(([label, value]) => {
    container.innerHTML += `
      <div class="info-tile">
        <span class="tile-label">${label}</span>
        <span class="tile-value">${value}</span>
      </div>`;
  });
}

function runMachine() {
  const a = parseFloat($('mach-a').value);
  const b = parseFloat($('mach-b').value);
  if (isNaN(a) || isNaN(b)) { alert('Enter valid floats.'); return; }

  const eps    = Calc.meps();
  const result = a + b;
  const actual = result - a;
  const loss   = Math.abs(actual - b);

  const lines = [
    '═══════════════════════════════════════',
    `  a                :  ${a}`,
    `  b                :  ${b}`,
    `  a + b            :  ${result}`,
    `  (a+b) - a        :  ${actual}`,
    `  Expected b       :  ${b}`,
    `  Information lost :  ${loss.toExponential(4)}`,
    `  Loss / epsilon   :  ${(eps > 0 ? loss / eps : 0).toFixed(2)} × ε`,
    '═══════════════════════════════════════',
  ];
  renderOutput('out-machine', lines);
  logReport(`Machine ε demo: a=${a}, b=${b}, loss=${loss.toExponential(4)}`);
}

/* ── Tab 6: Report ────────────────────────── */
function logReport(line) {
  reportLines.push(line);
  const box = $('out-report');
  const div = document.createElement('div');
  div.className = 'report-entry';
  const ts = new Date().toLocaleTimeString();
  div.textContent = `  •  [${ts}]  ${line}`;
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}

function clearReport() {
  reportLines = [];
  $('out-report').innerHTML = '';
}

function exportReport() {
  const lines = [
    'Scientific Calculator — Error Analysis Report',
    'Authors: Divyansh Sharma · Jiya Madan · Kabir Bajaj',
    `Exported: ${new Date().toLocaleString()}`,
    '',
    ...reportLines.map(l => `• ${l}`),
  ];
  const blob = new Blob([lines.join('\n')], { type: 'text/plain' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `error-analysis-report-${Date.now()}.txt`;
  a.click();
}

/* ═══════════════════════════════════════════════
   INIT
   ═══════════════════════════════════════════════ */
initMachine();
logReport('Session started — compute errors using the tabs above.');
