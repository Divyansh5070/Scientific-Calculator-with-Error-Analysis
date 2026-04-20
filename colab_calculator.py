"""
╔══════════════════════════════════════════════════════════╗
║   Scientific Calculator with Error Analysis              ║
║   Numerical Methods Project                              ║
║   Authors: Divyansh Sharma · Jiya Madan · Kabir Bajaj   ║
╚══════════════════════════════════════════════════════════╝

HOW TO USE IN GOOGLE COLAB:
  1. Upload this file to Colab  (or paste its contents into a cell)
  2. Run the cell — the full calculator appears in the output
  3. Use all tabs: Basic Errors, Propagation, Taylor, Sig Figs, Machine ε
"""

import math

# ═══════════════════════════════════════════════════════════
#  PYTHON ERROR ENGINE  (core logic — pure Python)
# ═══════════════════════════════════════════════════════════
class Calc:
    @staticmethod
    def absolute(t, a):   return abs(t - a)
    @staticmethod
    def relative(t, a):   return float('inf') if t == 0 else abs((t - a) / t)
    @staticmethod
    def percent(t, a):    return Calc.relative(t, a) * 100
    @staticmethod
    def roundoff(v, dp):  return abs(v - round(v, dp))
    @staticmethod
    def trunc(v, dp):
        f = 10**dp; return abs(v - math.trunc(v * f) / f)
    @staticmethod
    def meps():
        e = 1.0
        while (1.0 + e / 2) != 1.0: e /= 2
        return e
    @staticmethod
    def prop_add(da, db):        return math.sqrt(da**2 + db**2)
    @staticmethod
    def prop_mul(a, b, da, db):  return 0 if a==0 or b==0 else abs(a*b)*math.sqrt((da/a)**2+(db/b)**2)
    @staticmethod
    def prop_div(a, b, da, db):
        if b == 0: return float('inf')
        return 0 if a == 0 else abs(a/b)*math.sqrt((da/a)**2+(db/b)**2)
    @staticmethod
    def taylor(fn, x, n):
        if fn == "sin":
            ex = math.sin(x);  ap = sum((-1)**k*x**(2*k+1)/math.factorial(2*k+1) for k in range(n))
        elif fn == "cos":
            ex = math.cos(x);  ap = sum((-1)**k*x**(2*k)/math.factorial(2*k) for k in range(n))
        else:
            ex = math.exp(x);  ap = sum(x**k/math.factorial(k) for k in range(n))
        return ex, ap, abs(ex - ap)
    @staticmethod
    def sigfig(v, n):
        if v == 0: return 0
        d = math.ceil(math.log10(abs(v)))
        return round(v * 10**(n-d)) / 10**(n-d)


# ═══════════════════════════════════════════════════════════
#  HTML / CSS / JS  INTERFACE
# ═══════════════════════════════════════════════════════════
CALCULATOR_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"/>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#080C18;--card:#111827;--card2:#16202E;--border:#1E2D4A;
  --purple:#7C3AED;--purple-l:#9D5FF5;--purple-d:#5B21B6;
  --cyan:#22D3EE;--green:#34D399;--amber:#FBBF24;
  --text:#F1F5F9;--t2:#94A3B8;--t3:#475569;--t4:#1E2D4A;
  --num:#131E30;--num-h:#1E2E48;--op:#160E3B;--op-h:#231562;
  --fn:#071B28;--fn-h:#0D2D40;--clr:#3B0F0F;--clr-h:#7F1D1D;
  --font:'Inter',sans-serif;--mono:'JetBrains Mono',monospace;
}
body{font-family:var(--font);background:var(--bg);color:var(--text);min-height:100vh}
::-webkit-scrollbar{width:4px}::-webkit-scrollbar-thumb{background:var(--border);border-radius:4px}

/* ── Header ── */
.hdr{background:linear-gradient(90deg,#0B0525,#12063A,#0D1220);padding:12px 20px;
     border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between}
.hdr-l{display:flex;align-items:center;gap:12px}
.hdr-icon{font-size:24px;filter:drop-shadow(0 0 8px var(--purple));
          animation:glow 3s ease-in-out infinite}
@keyframes glow{0%,100%{filter:drop-shadow(0 0 6px #7C3AED)}50%{filter:drop-shadow(0 0 18px #9D5FF5)}}
.hdr-title{font-size:15px;font-weight:700}.hdr-title span{color:var(--purple-l)}
.hdr-sub{font-size:10px;color:var(--t3);margin-top:1px}
.author{font-size:10px;color:var(--t3);background:var(--card);border:1px solid var(--border);
        border-radius:20px;padding:4px 12px}

/* ── Layout ── */
.body{display:flex;height:680px;overflow:hidden}
.divider{width:1px;background:var(--border);flex-shrink:0}

/* ── Calculator Panel ── */
.calc-panel{width:400px;min-width:340px;flex-shrink:0;padding:12px;
            display:flex;flex-direction:column;gap:8px;overflow-y:auto;background:#0D1220}

/* ── Display ── */
.display{background:var(--card);border:1px solid var(--border);border-radius:12px;overflow:hidden}
.angle-row{display:flex;align-items:center;justify-content:space-between;
           padding:7px 10px;background:var(--card2);border-bottom:1px solid var(--border)}
.angle-grp{display:flex;gap:3px}
.ang{font-size:10px;font-weight:700;color:var(--t3);padding:3px 9px;border-radius:5px;
     cursor:pointer;border:1px solid transparent;transition:all .2s;user-select:none}
.ang.on{background:var(--purple);color:var(--text);border-color:var(--purple-l);
         box-shadow:0 0 8px rgba(124,58,237,.5)}
.ang:not(.on):hover{color:var(--t2);border-color:var(--border)}
.mem-d{font-size:10px;color:var(--t3);font-family:var(--mono)}
.expr-line{font-family:var(--mono);font-size:12px;color:var(--t2);
           text-align:right;padding:5px 14px 0;min-height:20px;word-break:break-all}
.result-line{font-family:var(--mono);font-size:38px;font-weight:700;color:var(--text);
             text-align:right;padding:2px 14px 12px;word-break:break-all;line-height:1.1;
             text-shadow:0 0 30px rgba(124,58,237,.3);transition:all .15s}
.disp-accent{height:2px;background:linear-gradient(90deg,transparent,var(--purple),var(--cyan),transparent);
             animation:glow2 3s ease-in-out infinite}
@keyframes glow2{0%,100%{opacity:.5}50%{opacity:1}}

/* ── Buttons ── */
.grid{display:grid;grid-template-columns:repeat(6,1fr);gap:4px}
.wide2{grid-column:span 2}
.btn{height:48px;border:none;border-radius:8px;font-family:var(--font);font-size:13px;
     font-weight:600;color:var(--text);cursor:pointer;transition:all .1s;outline:none}
.btn:active{transform:scale(.95)}
.btn.num{background:var(--num)}.btn.num:hover{background:var(--num-h)}
.btn.op{background:var(--op);color:#C4B5FD}.btn.op:hover{background:var(--op-h)}
.btn.fn{background:var(--fn);font-size:11px;color:var(--cyan)}.btn.fn:hover{background:var(--fn-h)}
.btn.eq{background:linear-gradient(135deg,#5B21B6,#7C3AED);font-size:18px;
         box-shadow:0 4px 18px rgba(124,58,237,.4)}
.btn.eq:hover{background:linear-gradient(135deg,#7C3AED,#9D5FF5);transform:translateY(-1px)}
.btn.clr{background:var(--clr);color:#F87171}.btn.clr:hover{background:var(--clr-h)}
.btn.sm{font-size:10px;color:var(--t2)}

/* ── History ── */
.hist-pane{background:var(--card);border:1px solid var(--border);border-radius:8px;overflow:hidden;flex-shrink:0}
.hist-hdr{display:flex;justify-content:space-between;align-items:center;
          padding:6px 10px;background:var(--card2);border-bottom:1px solid var(--border);
          font-size:10px;font-weight:700;color:var(--t2);text-transform:uppercase;letter-spacing:.5px}
.hist-list{list-style:none;max-height:100px;overflow-y:auto}
.hist-list li{padding:5px 10px;font-family:var(--mono);font-size:10px;color:var(--t2);
              border-bottom:1px solid var(--border);cursor:pointer;transition:all .15s;
              white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.hist-list li:hover{background:var(--card2);color:var(--text)}
.ghost{background:none;border:1px solid var(--border);border-radius:5px;color:var(--t3);
       font-size:10px;font-family:var(--font);padding:3px 8px;cursor:pointer;transition:all .15s}
.ghost:hover{border-color:var(--border);color:var(--t2);background:var(--card2)}
.ghost.d:hover{border-color:#EF4444;color:#EF4444}

/* ── Error Panel ── */
.err-panel{flex:1;display:flex;flex-direction:column;overflow:hidden}
.tabs-bar{display:flex;gap:2px;padding:8px 14px 0;background:#0D1220;
          border-bottom:1px solid var(--border);overflow-x:auto}
.tabs-bar::-webkit-scrollbar{height:3px}
.tab-btn{background:none;border:none;border-bottom:3px solid transparent;color:var(--t3);
         font-family:var(--font);font-size:11px;font-weight:700;padding:7px 12px;
         cursor:pointer;white-space:nowrap;transition:all .2s;border-radius:5px 5px 0 0;margin-bottom:-1px}
.tab-btn:hover{color:var(--t2);background:var(--card)}
.tab-btn.on{color:var(--text);background:var(--card);border-bottom-color:var(--purple);
            border-left:1px solid var(--border);border-right:1px solid var(--border);border-top:1px solid var(--border)}
.tab-content{display:none;padding:16px;overflow-y:auto;flex:1;flex-direction:column;gap:10px}
.tab-content.on{display:flex;animation:fi .2s ease}
@keyframes fi{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}
.tab-title{font-size:15px;font-weight:700;margin-bottom:2px}
.fields{display:flex;flex-direction:column;gap:7px}
.frow{display:flex;align-items:center;gap:10px}
.flbl{font-size:11px;font-weight:600;color:var(--t2);min-width:150px;flex-shrink:0}
.finp{flex:1;background:var(--card2);border:1px solid var(--border);border-radius:7px;
      color:var(--text);font-family:var(--mono);font-size:12px;padding:8px 10px;
      outline:none;transition:border-color .2s,box-shadow .2s;max-width:200px}
.finp:focus{border-color:var(--purple);box-shadow:0 0 0 3px rgba(124,58,237,.18)}
.finp::-webkit-inner-spin-button{opacity:0}
.radio-row{display:flex;gap:6px;flex-wrap:wrap;background:var(--card2);
           border:1px solid var(--border);border-radius:8px;padding:6px 10px}
.rchip{display:flex;align-items:center;gap:5px;font-size:11px;font-weight:600;
       color:var(--t2);cursor:pointer;padding:4px 9px;border-radius:5px;transition:all .15s}
.rchip input{display:none}
.rchip.sel{background:var(--purple);color:var(--text);box-shadow:0 0 10px rgba(124,58,237,.35)}
.rchip:not(.sel):hover{background:var(--card2);color:var(--text)}
.act-btn{align-self:flex-start;background:linear-gradient(135deg,var(--purple-d),var(--purple));
         border:none;border-radius:8px;color:var(--text);font-family:var(--font);
         font-size:12px;font-weight:700;padding:10px 24px;cursor:pointer;
         transition:all .2s;box-shadow:0 4px 14px rgba(124,58,237,.35)}
.act-btn:hover{background:linear-gradient(135deg,var(--purple),var(--purple-l));
               box-shadow:0 4px 22px rgba(124,58,237,.55);transform:translateY(-1px)}
.act-btn:active{transform:scale(.97)}
.outbox{background:var(--card);border:1px solid var(--border);border-radius:8px;
        padding:12px 14px;font-family:var(--mono);font-size:11px;line-height:1.9;
        overflow-y:auto;flex:1;min-height:120px;white-space:pre-wrap;word-break:break-all}
.outbox:empty::before{content:'Results will appear here…';color:var(--t4);font-style:italic}
.lk{color:var(--cyan)}.ls{color:var(--t4)}.lv{color:var(--green)}
.tiles{display:grid;grid-template-columns:1fr 1fr;gap:7px}
.tile{background:var(--card2);border:1px solid var(--border);border-radius:8px;padding:9px 12px}
.t-lbl{font-size:10px;color:var(--t2)}.t-val{font-family:var(--mono);font-size:12px;color:var(--cyan);font-weight:700}
.sub-h{font-size:12px;font-weight:700;color:var(--t2);padding-top:4px;border-top:1px solid var(--border)}
.hint{font-size:11px;color:var(--t3);margin-top:-4px}
.rep-acts{display:flex;gap:7px}
.rep-box .lv{color:var(--t2)}
</style>
</head>
<body>
<header class="hdr">
  <div class="hdr-l">
    <span class="hdr-icon">⚛</span>
    <div>
      <div class="hdr-title">Scientific Calculator <span>·</span> Error Analysis</div>
      <div class="hdr-sub">Numerical Methods Project</div>
    </div>
  </div>
  <span class="author">Divyansh Sharma · Jiya Madan · Kabir Bajaj</span>
</header>

<div class="body">
  <!-- ══ LEFT: CALCULATOR ══ -->
  <div class="calc-panel">
    <!-- display -->
    <div class="display">
      <div class="angle-row">
        <div class="angle-grp">
          <span class="ang on" id="ang-DEG"  onclick="setAngle('DEG')">DEG</span>
          <span class="ang"    id="ang-RAD"  onclick="setAngle('RAD')">RAD</span>
          <span class="ang"    id="ang-GRAD" onclick="setAngle('GRAD')">GRAD</span>
        </div>
        <span class="mem-d" id="mem-d">M</span>
      </div>
      <div class="expr-line"   id="expr-line">&nbsp;</div>
      <div class="result-line" id="res-line">0</div>
      <div class="disp-accent"></div>
    </div>
    <!-- buttons -->
    <div class="grid">
      <button class="btn fn sm" onclick="mClear()">MC</button>
      <button class="btn fn sm" onclick="mRecall()">MR</button>
      <button class="btn fn sm" onclick="mAdd()">M+</button>
      <button class="btn fn sm" onclick="mSub()">M−</button>
      <button class="btn fn sm" onclick="mStore()">MS</button>
      <button class="btn clr"   onclick="back()">⌫</button>

      <button class="btn fn" onclick="iF('sin')">sin</button>
      <button class="btn fn" onclick="iF('cos')">cos</button>
      <button class="btn fn" onclick="iF('tan')">tan</button>
      <button class="btn fn" onclick="iF('sqrt')">√x</button>
      <button class="btn fn" onclick="ip('**2')">x²</button>
      <button class="btn op" onclick="ip('**')">xⁿ</button>

      <button class="btn fn" onclick="iF('asin')">asin</button>
      <button class="btn fn" onclick="iF('acos')">acos</button>
      <button class="btn fn" onclick="iF('atan')">atan</button>
      <button class="btn fn" onclick="iF('log10')">log</button>
      <button class="btn fn" onclick="iF('ln')">ln</button>
      <button class="btn fn" onclick="iF('exp')">eˣ</button>

      <button class="btn fn" onclick="ip('3.14159265359')">π</button>
      <button class="btn fn" onclick="ip('2.71828182846')">e</button>
      <button class="btn op" onclick="ip('(')">(</button>
      <button class="btn op" onclick="ip(')')">)</button>
      <button class="btn fn" onclick="iF('fact')">n!</button>
      <button class="btn fn" onclick="iF('inv')">1/x</button>

      <button class="btn num" onclick="ip('7')">7</button>
      <button class="btn num" onclick="ip('8')">8</button>
      <button class="btn num" onclick="ip('9')">9</button>
      <button class="btn op"  onclick="ip('/')">÷</button>
      <button class="btn fn"  onclick="ip('**3')">x³</button>
      <button class="btn clr" onclick="ac()">AC</button>

      <button class="btn num" onclick="ip('4')">4</button>
      <button class="btn num" onclick="ip('5')">5</button>
      <button class="btn num" onclick="ip('6')">6</button>
      <button class="btn op"  onclick="ip('*')">×</button>
      <button class="btn fn"  onclick="iF('log2')">log₂</button>
      <button class="btn fn"  onclick="iF('cbrt')">∛</button>

      <button class="btn num" onclick="ip('1')">1</button>
      <button class="btn num" onclick="ip('2')">2</button>
      <button class="btn num" onclick="ip('3')">3</button>
      <button class="btn op"  onclick="ip('-')">−</button>
      <button class="btn op"  onclick="neg()">±</button>
      <button class="btn op"  onclick="ip('%')">%</button>

      <button class="btn num wide2" onclick="ip('0')">0</button>
      <button class="btn num"       onclick="ip('.')">.</button>
      <button class="btn op"        onclick="ip('+')">+</button>
      <button class="btn eq  wide2" onclick="calc()">=</button>
    </div>
    <!-- history -->
    <div class="hist-pane">
      <div class="hist-hdr">
        <span>History</span>
        <button class="ghost d" onclick="clearHist()">Clear</button>
      </div>
      <ul class="hist-list" id="hist-list"></ul>
    </div>
  </div>

  <div class="divider"></div>

  <!-- ══ RIGHT: ERROR ANALYSIS ══ -->
  <div class="err-panel">
    <div class="tabs-bar">
      <button class="tab-btn on" id="tb-basic"   onclick="tab('basic')">📐 Basic</button>
      <button class="tab-btn"    id="tb-prop"     onclick="tab('prop')">📈 Propagation</button>
      <button class="tab-btn"    id="tb-taylor"   onclick="tab('taylor')">🔢 Taylor</button>
      <button class="tab-btn"    id="tb-sigfig"   onclick="tab('sigfig')">📊 Sig Figs</button>
      <button class="tab-btn"    id="tb-machine"  onclick="tab('machine')">🔬 Machine ε</button>
      <button class="tab-btn"    id="tb-report"   onclick="tab('report')">📋 Report</button>
    </div>

    <!-- Basic -->
    <div class="tab-content on" id="tc-basic">
      <div class="tab-title">Basic Error Calculations</div>
      <div class="fields">
        <div class="frow"><label class="flbl">True Value</label><input class="finp" id="b-tv" type="number" placeholder="e.g. 3.14159"/></div>
        <div class="frow"><label class="flbl">Approx Value</label><input class="finp" id="b-av" type="number" placeholder="e.g. 3.14"/></div>
        <div class="frow"><label class="flbl">Decimal Places</label><input class="finp" id="b-dp" type="number" value="5" min="0" max="15"/></div>
      </div>
      <button class="act-btn" onclick="runBasic()">Calculate Errors</button>
      <div class="outbox" id="out-basic"></div>
    </div>

    <!-- Propagation -->
    <div class="tab-content" id="tc-prop">
      <div class="tab-title">Error Propagation</div>
      <div class="radio-row" id="pr-row">
        <label class="rchip sel" id="pr-add"><input type="radio" name="pr" value="add" checked/> Addition</label>
        <label class="rchip"     id="pr-sub"><input type="radio" name="pr" value="sub"/> Subtraction</label>
        <label class="rchip"     id="pr-mul"><input type="radio" name="pr" value="mul"/> Multiply</label>
        <label class="rchip"     id="pr-div"><input type="radio" name="pr" value="div"/> Divide</label>
      </div>
      <div class="fields">
        <div class="frow"><label class="flbl">Value a</label><input class="finp" id="p-a"  type="number" placeholder="5.0"/></div>
        <div class="frow"><label class="flbl">Abs Error Δa</label><input class="finp" id="p-da" type="number" placeholder="0.1"/></div>
        <div class="frow"><label class="flbl">Value b</label><input class="finp" id="p-b"  type="number" placeholder="3.0"/></div>
        <div class="frow"><label class="flbl">Abs Error Δb</label><input class="finp" id="p-db" type="number" placeholder="0.05"/></div>
      </div>
      <button class="act-btn" onclick="runProp()">Propagate Error</button>
      <div class="outbox" id="out-prop"></div>
    </div>

    <!-- Taylor -->
    <div class="tab-content" id="tc-taylor">
      <div class="tab-title">Taylor Series Truncation Error</div>
      <div class="radio-row" id="tf-row">
        <label class="rchip sel" id="tf-sin"><input type="radio" name="tf" value="sin" checked/> sin(x)</label>
        <label class="rchip"     id="tf-cos"><input type="radio" name="tf" value="cos"/> cos(x)</label>
        <label class="rchip"     id="tf-exp"><input type="radio" name="tf" value="exp"/> exp(x)</label>
      </div>
      <div class="fields">
        <div class="frow"><label class="flbl">x (radians)</label><input class="finp" id="t-x" type="number" placeholder="1.0"/></div>
        <div class="frow"><label class="flbl">Max Terms (1–20)</label><input class="finp" id="t-n" type="number" value="8" min="1" max="20"/></div>
      </div>
      <button class="act-btn" onclick="runTaylor()">Compute Error</button>
      <div class="outbox" id="out-taylor" style="font-size:10px"></div>
    </div>

    <!-- Sig Figs -->
    <div class="tab-content" id="tc-sigfig">
      <div class="tab-title">Significant Figures &amp; Rounding</div>
      <div class="fields">
        <div class="frow"><label class="flbl">Value</label><input class="finp" id="sf-v" type="number" placeholder="3.14159265"/></div>
        <div class="frow"><label class="flbl">Significant Figures</label><input class="finp" id="sf-n" type="number" value="4" min="1"/></div>
      </div>
      <button class="act-btn" onclick="runSigfig()">Analyse</button>
      <div class="outbox" id="out-sigfig"></div>
    </div>

    <!-- Machine -->
    <div class="tab-content" id="tc-machine">
      <div class="tab-title">Machine Epsilon &amp; Floating Point</div>
      <div class="tiles" id="mach-tiles"></div>
      <div class="sub-h">Catastrophic Cancellation Demo</div>
      <div class="fields">
        <div class="frow"><label class="flbl">a</label><input class="finp" id="m-a" type="number" value="1.0"/></div>
        <div class="frow"><label class="flbl">b (tiny)</label><input class="finp" id="m-b" type="number" value="1e-16"/></div>
      </div>
      <button class="act-btn" onclick="runMachine()">Analyse Cancellation</button>
      <div class="outbox" id="out-machine"></div>
    </div>

    <!-- Report -->
    <div class="tab-content" id="tc-report">
      <div class="tab-title">Session Report</div>
      <div class="hint">All computations are auto-logged here.</div>
      <div class="rep-acts">
        <button class="ghost d" onclick="clearRep()">Clear</button>
        <button class="ghost"   onclick="exportRep()">Export .txt</button>
      </div>
      <div class="outbox rep-box" id="out-report"></div>
    </div>
  </div>
</div>

<script>
'use strict';
let expr='', memory=0, history=[], repLines=[], angleMode='DEG';

// ── display helpers ──────────────────────────────────
const EL=id=>document.getElementById(id);
function setExpr(t){EL('expr-line').textContent=t||'\\u00A0'}
function setRes(t){EL('res-line').textContent=t}
function getRes(){return EL('res-line').textContent}

// ── math engine ─────────────────────────────────────
const factorial=n=>{let r=1;for(let i=2;i<=n;i++)r*=i;return r};
function evaluate(e){
  const toR=x=>angleMode==='DEG'?x*Math.PI/180:angleMode==='GRAD'?x*Math.PI/200:x;
  const frR=r=>angleMode==='DEG'?r*180/Math.PI:angleMode==='GRAD'?r*200/Math.PI:r;
  let s=e.replace(/\\^/g,'**')
   .replace(/\\bsin\\(/g,'_sin(').replace(/\\bcos\\(/g,'_cos(').replace(/\\btan\\(/g,'_tan(')
   .replace(/\\basin\\(/g,'_asin(').replace(/\\bacos\\(/g,'_acos(').replace(/\\batan\\(/g,'_atan(')
   .replace(/\\bsqrt\\(/g,'_sqrt(').replace(/\\bcbrt\\(/g,'_cbrt(')
   .replace(/\\blog10\\(/g,'_log10(').replace(/\\blog2\\(/g,'_log2(')
   .replace(/\\bln\\(/g,'_ln(').replace(/\\bexp\\(/g,'_exp(')
   .replace(/\\binv\\(/g,'_inv(').replace(/\\bfact\\(/g,'_fact(')
   .replace(/\\bpi\\b/g,String(Math.PI)).replace(/\\be\\b/g,String(Math.E));
  return Function(
   '_sin','_cos','_tan','_asin','_acos','_atan','_sqrt','_cbrt',
   '_log10','_log2','_ln','_exp','_inv','_fact',
   '"use strict";return('+s+');'
  )(x=>Math.sin(toR(x)),x=>Math.cos(toR(x)),x=>Math.tan(toR(x)),
    x=>frR(Math.asin(x)),x=>frR(Math.acos(x)),x=>frR(Math.atan(x)),
    Math.sqrt,Math.cbrt,Math.log10,Math.log2,Math.log,Math.exp,
    x=>1/x,x=>factorial(Math.round(x)));
}
function fmtN(n){if(!isFinite(n))return String(n);if(Number.isInteger(n)&&Math.abs(n)<1e15)return String(n);return parseFloat(n.toPrecision(10)).toString()}

// ── calculator ──────────────────────────────────────
function ip(c){expr+=c;setExpr(expr);live()}
function iF(n){expr+=n+'(';setExpr(expr)}
function ac(){expr='';setExpr('');setRes('0')}
function back(){expr=expr.slice(0,-1);setExpr(expr);live()}
function neg(){if(expr){expr='-('+expr+')';setExpr(expr);live()}}
function live(){try{const r=evaluate(expr);setRes(fmtN(r))}catch(_){}}
function calc(){
  if(!expr)return;
  try{
    const r=evaluate(expr),d=fmtN(r),entry=expr+'  =  '+d;
    history.unshift(entry);if(history.length>30)history.pop();
    renderHist();setRes(d);setExpr(expr+' =');expr=d;
    EL('res-line').style.textShadow='0 0 40px rgba(124,58,237,.9)';
    setTimeout(()=>EL('res-line').style.textShadow='',250);
    logRep('= '+d);
  }catch(ex){setRes('Error');setExpr(String(ex).slice(0,55))}
}
function setAngle(m){
  angleMode=m;
  ['DEG','RAD','GRAD'].forEach(x=>EL('ang-'+x).classList.toggle('on',x===m));
  live();
}
function mStore(){try{memory=parseFloat(getRes());updM()}catch(_){}}
function mRecall(){ip(String(memory))}
function mClear(){memory=0;updM()}
function mAdd(){try{memory+=parseFloat(getRes());updM()}catch(_){}}
function mSub(){try{memory-=parseFloat(getRes());updM()}catch(_){}}
function updM(){const e=EL('mem-d');if(memory!==0){e.textContent='M: '+parseFloat(memory.toPrecision(6));e.style.color='#22D3EE'}else{e.textContent='M';e.style.color=''}}
function renderHist(){const ul=EL('hist-list');ul.innerHTML='';history.forEach(it=>{const li=document.createElement('li');li.textContent=it;li.onclick=()=>{expr=it.split('  =  ')[0].trim();setExpr(expr);live()};ul.appendChild(li)})}
function clearHist(){history=[];renderHist()}

// ── tabs ────────────────────────────────────────────
function tab(n){
  document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('on'));
  document.querySelectorAll('.tab-content').forEach(c=>c.classList.remove('on'));
  EL('tb-'+n).classList.add('on');EL('tc-'+n).classList.add('on');
}
// radio chip highlight
function setupRadio(name,rowId){
  document.querySelectorAll('input[name="'+name+'"]').forEach(r=>{
    r.addEventListener('change',()=>{
      document.querySelectorAll('#'+rowId+' .rchip').forEach(c=>c.classList.remove('sel'));
      r.closest('.rchip').classList.add('sel');
    });
  });
}
setupRadio('pr','pr-row');setupRadio('tf','tf-row');

// ── output renderer ─────────────────────────────────
function renderOut(id,lines){
  const box=EL(id);box.innerHTML='';
  lines.forEach(l=>{
    const d=document.createElement('div');
    if(l.startsWith('═')||l.startsWith('─')){d.className='ls';d.textContent=l}
    else if(l.includes(':')){
      const i=l.indexOf(':');
      const ks=document.createElement('span');ks.className='lk';ks.textContent=l.slice(0,i+1);
      const vs=document.createElement('span');vs.className='lv';vs.textContent=l.slice(i+1);
      d.appendChild(ks);d.appendChild(vs);
    }else{d.textContent=l}
    box.appendChild(d);
  });
}

// ── report ──────────────────────────────────────────
function logRep(l){
  repLines.push(l);const box=EL('out-report');
  const d=document.createElement('div');d.style.color='#34D399';
  d.textContent='  •  ['+new Date().toLocaleTimeString()+']  '+l;
  box.appendChild(d);box.scrollTop=box.scrollHeight;
}
function clearRep(){repLines=[];EL('out-report').innerHTML=''}
function exportRep(){
  const b=new Blob([['Scientific Calculator — Error Analysis Report',
    'Authors: Divyansh Sharma · Jiya Madan · Kabir Bajaj',
    'Exported: '+new Date().toLocaleString(),'',
    ...repLines.map(l=>'• '+l)].join('\\n')],{type:'text/plain'});
  const a=document.createElement('a');a.href=URL.createObjectURL(b);
  a.download='error-report.txt';a.click();
}

// ── error tabs ──────────────────────────────────────
function runBasic(){
  const tv=parseFloat(EL('b-tv').value),av=parseFloat(EL('b-av').value),dp=parseInt(EL('b-dp').value)||5;
  if(isNaN(tv)||isNaN(av)){alert('Enter valid True and Approx values');return}
  const ae=Math.abs(tv-av),re=tv===0?Infinity:Math.abs((tv-av)/tv),pe=re*100;
  const f=10**dp,ro=Math.abs(av-Math.round(av*f)/f),te=Math.abs(av-Math.trunc(av*f)/f);
  const acc=re>0?Math.floor(-Math.log10(re)):'∞';
  renderOut('out-basic',[
    '═══════════════════════════════════════',
    '  True Value       :  '+tv,
    '  Approx Value     :  '+av,
    '  Decimal Places   :  '+dp,
    '───────────────────────────────────────',
    '  Absolute Error   :  '+ae.toExponential(8),
    '  Relative Error   :  '+re.toExponential(8),
    '  Percentage Error :  '+pe.toFixed(6)+' %',
    '  Round-off Error  :  '+ro.toExponential(8),
    '  Truncation Error :  '+te.toExponential(8),
    '───────────────────────────────────────',
    '  Accurate Digits  :  '+acc,
    '═══════════════════════════════════════',
  ]);
  logRep('Basic — AE='+ae.toExponential(4)+' RE='+re.toExponential(4)+' PE='+pe.toFixed(4)+'%');
}

function runProp(){
  const a=parseFloat(EL('p-a').value),da=parseFloat(EL('p-da').value);
  const b=parseFloat(EL('p-b').value),db=parseFloat(EL('p-db').value);
  const op=document.querySelector('input[name="pr"]:checked').value;
  if([a,da,b,db].some(isNaN)){alert('Fill in all four fields');return}
  let res,df,sym;
  if(op==='add'){res=a+b;df=Math.sqrt(da**2+db**2);sym='+'}
  else if(op==='sub'){res=a-b;df=Math.sqrt(da**2+db**2);sym='−'}
  else if(op==='mul'){res=a*b;df=(a===0||b===0)?0:Math.abs(a*b)*Math.sqrt((da/a)**2+(db/b)**2);sym='×'}
  else{res=b?a/b:Infinity;df=b===0?Infinity:(a===0?0:Math.abs(a/b)*Math.sqrt((da/a)**2+(db/b)**2));sym='÷'}
  const rel=res?df/Math.abs(res):Infinity;
  renderOut('out-prop',[
    '═══════════════════════════════════════',
    '  Operation    :  '+a+'  '+sym+'  '+b,
    '  Result       :  '+parseFloat(res.toPrecision(8)),
    '───────────────────────────────────────',
    '  Delta a      :  ±'+da,'  Delta b      :  ±'+db,
    '  Prop Error   :  ±'+df.toExponential(6),
    '  Range        :  ['+(res-df).toPrecision(6)+' , '+(res+df).toPrecision(6)+']',
    '  Relative Err :  '+rel.toExponential(4),
    '───────────────────────────────────────',
    '  Method       :  Quadrature (RSS) Law',
    '═══════════════════════════════════════',
  ]);
}

function runTaylor(){
  const x=parseFloat(EL('t-x').value),n=parseInt(EL('t-n').value);
  const fn=document.querySelector('input[name="tf"]:checked').value;
  if(isNaN(x)){alert('Enter a number for x');return}
  if(n<1||n>20||isNaN(n)){alert('Terms must be 1–20');return}
  let exact;
  if(fn==='sin')exact=Math.sin(x);else if(fn==='cos')exact=Math.cos(x);else exact=Math.exp(x);
  const fac=k=>{let r=1;for(let i=2;i<=k;i++)r*=i;return r};
  const lines=['══════════════════════════════════════════════════════',
    '  Function : '+fn+'(x)    x = '+x,'  Exact    : '+exact.toFixed(12),
    '──────────────────────────────────────────────────────',
    '  Terms       Approximate              Error',
    '──────────────────────────────────────────────────────'];
  for(let t=1;t<=n;t++){
    let ap=0;
    if(fn==='sin')for(let k=0;k<t;k++)ap+=((-1)**k)*(x**(2*k+1))/fac(2*k+1);
    else if(fn==='cos')for(let k=0;k<t;k++)ap+=((-1)**k)*(x**(2*k))/fac(2*k);
    else for(let k=0;k<t;k++)ap+=(x**k)/fac(k);
    const e=Math.abs(exact-ap);
    lines.push('  '+String(t).padStart(4)+'    '+ap.toFixed(8).padStart(18)+'    '+e.toExponential(6).padStart(14));
  }
  lines.push('══════════════════════════════════════════════════════');
  renderOut('out-taylor',lines);
  logRep('Taylor '+fn+'('+x+') with '+n+' terms');
}

function runSigfig(){
  const v=parseFloat(EL('sf-v').value),n=parseInt(EL('sf-n').value);
  if(isNaN(v)){alert('Enter a valid number');return}
  if(n<1||isNaN(n)){alert('Sig figs must be ≥ 1');return}
  const d=Math.ceil(Math.log10(Math.abs(v)||1));
  const rv=Math.round(v*10**(n-d))/10**(n-d);
  const ae=Math.abs(v-rv),re=v?ae/Math.abs(v):0;
  const lines=['═══════════════════════════════════════',
    '  Original Value :  '+v,'  Sig Figures    :  '+n,
    '───────────────────────────────────────',
    '  Rounded Value  :  '+rv,'  Absolute Error :  '+ae.toExponential(6),
    '  Relative Error :  '+re.toExponential(6),'  Percentage Err :  '+(re*100).toFixed(4)+' %',
    '───────────────────────────────────────','  Rounding Table:',
    '───────────────────────────────────────'];
  for(let dp=1;dp<=8;dp++){
    const rv2=parseFloat(v.toFixed(dp)),e=Math.abs(v-rv2);
    lines.push('  dp='+dp+'  →  '+String(rv2).padEnd(20)+'  err='+e.toExponential(2));
  }
  lines.push('═══════════════════════════════════════');
  renderOut('out-sigfig',lines);
  logRep('SigFigs('+v+', '+n+') → '+rv);
}

// machine epsilon init
(function(){
  let eps=1;while((1+eps/2)!==1)eps/=2;
  const rows=[
    ['Computed ε (float64)',eps.toExponential(4)],
    ['IEEE 754 ε (float64)','2.2204e-16'],
    ['IEEE 754 ε (float32)','1.1921e-07'],
    ['IEEE 754 ε (float16)','9.7656e-04'],
    ['Max float64','1.7977e+308'],
    ['Min positive float64','5.0000e-324'],
  ];
  const c=EL('mach-tiles');
  rows.forEach(([l,v])=>{c.innerHTML+='<div class="tile"><div class="t-lbl">'+l+'</div><div class="t-val">'+v+'</div></div>'});
})();

function runMachine(){
  const a=parseFloat(EL('m-a').value),b=parseFloat(EL('m-b').value);
  if(isNaN(a)||isNaN(b)){alert('Enter valid floats');return}
  let eps=1;while((1+eps/2)!==1)eps/=2;
  const res=a+b,act=res-a,loss=Math.abs(act-b);
  renderOut('out-machine',[
    '═══════════════════════════════════════',
    '  a                :  '+a,'  b                :  '+b,
    '  a + b            :  '+res,'  (a+b) − a        :  '+act,
    '  Expected b       :  '+b,'  Information lost :  '+loss.toExponential(4),
    '  Loss / epsilon   :  '+(eps>0?loss/eps:0).toFixed(2)+' × ε',
    '═══════════════════════════════════════',
  ]);
  logRep('Machine ε: a='+a+', b='+b+', loss='+loss.toExponential(4));
}

// keyboard
document.addEventListener('keydown',e=>{
  if(e.target.tagName==='INPUT')return;
  if(e.key==='Enter'){e.preventDefault();calc()}
  else if(e.key==='Backspace'){e.preventDefault();back()}
  else if(e.key==='Escape'){e.preventDefault();ac()}
  else if('0123456789.+-*/()%'.includes(e.key)){e.preventDefault();ip(e.key)}
});

logRep('Session started — compute errors using the tabs above.');
</script>
</body>
</html>
"""

# ═══════════════════════════════════════════════════════════
#  LAUNCH  — works in Google Colab, Jupyter, and browser
# ═══════════════════════════════════════════════════════════
def launch():
    try:
        # ── Google Colab / Jupyter: inject HTML directly ──
        from IPython.display import display, HTML
        print("✅  Calculator loaded! Scroll down to interact.")
        display(HTML(CALCULATOR_HTML))
    except ImportError:
        # ── Plain Python: save & open in browser ──────────
        import os, tempfile, webbrowser
        path = os.path.join(tempfile.gettempdir(), "nm_calculator.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(CALCULATOR_HTML)
        webbrowser.open("file://" + path)
        print(f"Opened calculator in browser: {path}")


# ── Also expose Python Calc functions for notebook use ──────
def basic_errors(true_val, approx_val, decimal_places=5):
    """Print all basic error metrics — call this directly in a Colab cell."""
    ae = Calc.absolute(true_val, approx_val)
    re = Calc.relative(true_val, approx_val)
    pe = Calc.percent(true_val, approx_val)
    ro = Calc.roundoff(approx_val, decimal_places)
    te = Calc.trunc(approx_val, decimal_places)
    print(f"""
  True Value        : {true_val}
  Approx Value      : {approx_val}
  ─────────────────────────────────────
  Absolute Error    : {ae:.8e}
  Relative Error    : {re:.8e}
  Percentage Error  : {pe:.6f} %
  Round-off Error   : {ro:.8e}
  Truncation Error  : {te:.8e}
""")


if __name__ == "__main__":
    launch()
