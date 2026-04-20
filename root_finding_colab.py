"""
╔══════════════════════════════════════════════════════════════╗
║   ROOT FINDING CALCULATOR                                    ║
║   Numerical Methods Project                                  ║
║   Authors: Divyansh Sharma · Jiya Madan · Kabir Bajaj        ║
╠══════════════════════════════════════════════════════════════╣
║  METHODS IMPLEMENTED:                                        ║
║   1. Bisection Method                                        ║
║   2. False Position (Regula Falsi)                           ║
║   3. Newton–Raphson Method                                   ║
║   4. Secant Method                                           ║
║   5. Fixed-Point Iteration                                   ║
║   6. Muller's Method                                         ║
╠══════════════════════════════════════════════════════════════╣
║  HOW TO USE IN GOOGLE COLAB:                                 ║
║   1. Paste this entire script into a Colab cell              ║
║   2. Run it — the interactive GUI appears below              ║
║   3. Enter f(x), pick a method, set parameters, click Solve  ║
╚══════════════════════════════════════════════════════════════╝
"""

# ═══════════════════════════════════════════════════════════
#  PYTHON ROOT-FINDING ENGINE  (pure Python backend)
# ═══════════════════════════════════════════════════════════
import math, cmath

def _safe_eval(expr_str, x_val):
    """Safely evaluate f(x) for a given x value."""
    allowed = {
        'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
        'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
        'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
        'exp': math.exp, 'log': math.log, 'log2': math.log2,
        'log10': math.log10, 'sqrt': math.sqrt, 'abs': abs,
        'ceil': math.ceil, 'floor': math.floor,
        'pi': math.pi, 'e': math.e, 'x': x_val
    }
    return eval(expr_str, {"__builtins__": {}}, allowed)

def _numerical_deriv(f_str, x, h=1e-7):
    """Central-difference numerical derivative."""
    return (_safe_eval(f_str, x + h) - _safe_eval(f_str, x - h)) / (2 * h)

class RootSolver:
    @staticmethod
    def bisection(f_str, a, b, tol=1e-7, max_iter=100):
        rows = []
        fa = _safe_eval(f_str, a)
        fb = _safe_eval(f_str, b)
        if fa * fb > 0:
            return None, [], "f(a) and f(b) must have opposite signs."
        for i in range(1, max_iter + 1):
            c = (a + b) / 2.0
            fc = _safe_eval(f_str, c)
            ea = abs(b - a) / 2.0
            rows.append((i, a, b, c, fc, ea))
            if abs(fc) < tol or ea < tol:
                return c, rows, None
            if fa * fc < 0:
                b, fb = c, fc
            else:
                a, fa = c, fc
        return c, rows, "Max iterations reached."

    @staticmethod
    def false_position(f_str, a, b, tol=1e-7, max_iter=100):
        rows = []
        fa = _safe_eval(f_str, a)
        fb = _safe_eval(f_str, b)
        if fa * fb > 0:
            return None, [], "f(a) and f(b) must have opposite signs."
        c_old = a
        for i in range(1, max_iter + 1):
            fa = _safe_eval(f_str, a)
            fb = _safe_eval(f_str, b)
            c = b - fb * (b - a) / (fb - fa)
            fc = _safe_eval(f_str, c)
            ea = abs(c - c_old)
            rows.append((i, a, b, c, fc, ea))
            if abs(fc) < tol or (i > 1 and ea < tol):
                return c, rows, None
            if fa * fc < 0:
                b, fb = c, fc
            else:
                a, fa = c, fc
            c_old = c
        return c, rows, "Max iterations reached."

    @staticmethod
    def newton_raphson(f_str, x0, tol=1e-7, max_iter=100):
        rows = []
        x = x0
        for i in range(1, max_iter + 1):
            fx = _safe_eval(f_str, x)
            fpx = _numerical_deriv(f_str, x)
            if abs(fpx) < 1e-14:
                return None, rows, "Derivative too small — possible inflection point."
            x_new = x - fx / fpx
            ea = abs(x_new - x)
            rows.append((i, x, fx, fpx, x_new, ea))
            if ea < tol and abs(fx) < tol:
                return x_new, rows, None
            x = x_new
        return x, rows, "Max iterations reached."

    @staticmethod
    def secant(f_str, x0, x1, tol=1e-7, max_iter=100):
        rows = []
        for i in range(1, max_iter + 1):
            f0 = _safe_eval(f_str, x0)
            f1 = _safe_eval(f_str, x1)
            if abs(f1 - f0) < 1e-14:
                return None, rows, "f(x1) ≈ f(x0) — division by zero risk."
            x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
            ea = abs(x2 - x1)
            rows.append((i, x0, x1, x2, _safe_eval(f_str, x2), ea))
            if ea < tol:
                return x2, rows, None
            x0, x1 = x1, x2
        return x1, rows, "Max iterations reached."

    @staticmethod
    def fixed_point(f_str, g_str, x0, tol=1e-7, max_iter=100):
        rows = []
        x = x0
        for i in range(1, max_iter + 1):
            x_new = _safe_eval(g_str, x)
            ea = abs(x_new - x)
            fx = _safe_eval(f_str, x_new)
            rows.append((i, x, x_new, fx, ea))
            if ea < tol:
                return x_new, rows, None
            x = x_new
        return x, rows, "Max iterations reached (check g(x) convergence)."

    @staticmethod
    def muller(f_str, x0, x1, x2, tol=1e-7, max_iter=100):
        """Muller's Method — can find complex roots."""
        rows = []
        for i in range(1, max_iter + 1):
            f0 = _safe_eval(f_str, x0)
            f1 = _safe_eval(f_str, x1)
            f2 = _safe_eval(f_str, x2)
            h1 = x1 - x0
            h2 = x2 - x1
            d1 = (f1 - f0) / h1 if h1 != 0 else 0
            d2 = (f2 - f1) / h2 if h2 != 0 else 0
            a = (d2 - d1) / (h2 + h1) if (h2 + h1) != 0 else 0
            b = a * h2 + d2
            c = f2
            disc = b**2 - 4*a*c
            if disc < 0:
                sq = cmath.sqrt(disc)
                denom = (b + sq) if abs(b + sq) > abs(b - sq) else (b - sq)
                dx = -2*c / denom if denom != 0 else 0
            else:
                sq = math.sqrt(disc)
                denom = (b + sq) if abs(b + sq) > abs(b - sq) else (b - sq)
                dx = -2*c / denom if denom != 0 else 0
            x3 = x2 + dx
            ea = abs(dx)
            rows.append((i, x0, x1, x2, x3, f2, ea))
            if ea < tol:
                return x3, rows, None
            x0, x1, x2 = x1, x2, x3
        return x2, rows, "Max iterations reached."


# ═══════════════════════════════════════════════════════════
#  HTML / CSS / JS  INTERFACE
# ═══════════════════════════════════════════════════════════
ROOT_FINDER_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet"/>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#121212;--panel:#1A1A1A;--card:#242424;--card2:#2D2D2D;--border:#333;
  --accent:#FF6D00;--accent-l:#FF9E40;--accent-d:#BF5200;
  --green:#AEEA00;--pink:#FF4081;--gold:#FFD600;
  --text:#E0E0E0;--t2:#B0B0B0;--t3:#757575;--t4:#333;
  --font:'Inter',sans-serif;--mono:'JetBrains Mono',monospace;
  --glow-p:rgba(255,109,0,.35);--glow-c:rgba(174,234,0,.25);
}
body{font-family:var(--font);background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:var(--panel)}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:6px}

/* ─── Header ─── */
.hdr{
  background:linear-gradient(135deg,#1A0A00 0%,#261000 40%,#121212 100%);
  padding:14px 22px;border-bottom:1px solid var(--border);
  display:flex;align-items:center;justify-content:space-between;
  position:relative;overflow:hidden;
}
.hdr::before{
  content:'';position:absolute;inset:0;
  background:radial-gradient(ellipse 60% 100% at 50% -20%,rgba(255,109,0,.18),transparent);
}
.hdr-l{display:flex;align-items:center;gap:14px;position:relative}
.hdr-icon{font-size:28px;animation:spin-icon 8s linear infinite;display:inline-block}
@keyframes spin-icon{0%{filter:drop-shadow(0 0 6px var(--accent))}50%{filter:drop-shadow(0 0 20px var(--green))}100%{filter:drop-shadow(0 0 6px var(--accent))}}
.hdr-title{font-size:16px;font-weight:800;letter-spacing:-.3px}
.hdr-title span{background:linear-gradient(90deg,var(--accent-l),var(--gold));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hdr-sub{font-size:10px;color:var(--t3);margin-top:2px;letter-spacing:.5px;text-transform:uppercase}
.authors{font-size:10px;color:var(--t3);background:rgba(255,255,255,.04);
  border:1px solid var(--border);border-radius:20px;padding:5px 14px;position:relative}

/* ─── Layout ─── */
.layout{display:grid;grid-template-columns:340px 1fr;height:calc(100vh - 60px);overflow:hidden}
.left-col{border-right:1px solid var(--border);display:flex;flex-direction:column;overflow:hidden;background:var(--panel)}
.right-col{display:flex;flex-direction:column;overflow:hidden}
.divider-h{height:1px;background:var(--border);flex-shrink:0}

/* ─── Section Headers ─── */
.sec-hdr{
  padding:10px 16px;background:var(--card);border-bottom:1px solid var(--border);
  font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1px;
  color:var(--t2);display:flex;align-items:center;gap:8px;flex-shrink:0
}
.sec-hdr-dot{width:6px;height:6px;border-radius:50%;background:var(--accent);
  box-shadow:0 0 8px var(--accent);animation:pulse-dot 2s ease-in-out infinite}
@keyframes pulse-dot{0%,100%{opacity:1}50%{opacity:.4}}

/* ─── Input Panel ─── */
.input-scroll{flex:1;overflow-y:auto;padding:14px 14px 8px}

.field-group{margin-bottom:12px}
.fglabel{font-size:10px;font-weight:700;color:var(--t2);text-transform:uppercase;
  letter-spacing:.8px;margin-bottom:5px;display:flex;align-items:center;gap:6px}
.fglabel .badge{
  font-size:9px;background:var(--accent-d);color:var(--accent-l);
  border-radius:4px;padding:1px 6px;text-transform:none;letter-spacing:0
}

.inp{
  width:100%;background:var(--card2);border:1px solid var(--border);border-radius:8px;
  color:var(--text);font-family:var(--mono);font-size:12px;padding:9px 12px;
  outline:none;transition:border-color .2s,box-shadow .2s;
}
.inp:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--glow-p)}
.inp::placeholder{color:var(--t3)}
.inp-row{display:flex;gap:8px}
.inp-row .inp{flex:1}

/* ─── Method Selector ─── */
.method-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px}
.mcard{
  background:var(--card2);border:1.5px solid var(--border);border-radius:10px;
  padding:9px 10px;cursor:pointer;transition:all .2s;user-select:none;
  display:flex;flex-direction:column;gap:2px;
}
.mcard:hover{border-color:var(--t3);background:var(--card)}
.mcard.sel{
  border-color:var(--accent);background:rgba(255,109,0,.12);
  box-shadow:0 0 14px var(--glow-p);
}
.mcard-icon{font-size:14px}
.mcard-name{font-size:11px;font-weight:700;color:var(--text)}
.mcard.sel .mcard-name{color:var(--accent-l)}
.mcard-desc{font-size:9px;color:var(--t3);line-height:1.3}
.mcard.sel .mcard-desc{color:var(--t2)}

/* ─── Parameter Sliders/Inputs ─── */
.param-row{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:2px}
.param-box{background:var(--card2);border:1px solid var(--border);border-radius:8px;padding:8px 10px}
.param-label{font-size:9px;color:var(--t3);text-transform:uppercase;letter-spacing:.5px;margin-bottom:3px}
.param-inp{
  width:100%;background:transparent;border:none;color:var(--gold);
  font-family:var(--mono);font-size:12px;font-weight:600;outline:none;
}
.param-inp::-webkit-inner-spin-button{opacity:0}

/* ─── Solve Button ─── */
.solve-btn{
  width:100%;background:linear-gradient(135deg,var(--accent-d),var(--accent));
  border:none;border-radius:10px;color:#fff;font-family:var(--font);
  font-size:13px;font-weight:700;padding:13px;cursor:pointer;
  transition:all .25s;box-shadow:0 4px 20px var(--glow-p);
  letter-spacing:.3px;position:relative;overflow:hidden;margin-top:8px;
}
.solve-btn::after{
  content:'';position:absolute;inset:0;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.1),transparent);
  transform:translateX(-100%);transition:transform .5s;
}
.solve-btn:hover::after{transform:translateX(100%)}
.solve-btn:hover{box-shadow:0 6px 28px rgba(255,109,0,.6);transform:translateY(-1px)}
.solve-btn:active{transform:scale(.98)}

/* ─── Methods context box ─── */
.method-detail{
  margin-top:6px;background:var(--card);border:1px solid var(--border);
  border-radius:8px;padding:8px 10px;font-size:10px;color:var(--t2);line-height:1.6;
  display:none;
}
.method-detail.vis{display:block;animation:fi .2s ease}
.method-detail .formula{font-family:var(--mono);color:var(--gold);font-size:10px}

/* ─── Right: Tabs + Output ─── */
.tabs-bar{
  display:flex;gap:0;padding:8px 16px 0;background:var(--panel);
  border-bottom:1px solid var(--border);overflow-x:auto;flex-shrink:0;
}
.tabs-bar::-webkit-scrollbar{height:3px}
.tab-btn{
  background:none;border:none;border-bottom:2px solid transparent;
  color:var(--t3);font-family:var(--font);font-size:11px;font-weight:700;
  padding:7px 14px;cursor:pointer;transition:all .2s;
  border-radius:6px 6px 0 0;margin-bottom:-1px;letter-spacing:.2px;
}
.tab-btn:hover{color:var(--t2);background:rgba(255,255,255,.04)}
.tab-btn.on{color:var(--text);background:var(--card);border-bottom-color:var(--accent);
  border-left:1px solid var(--border);border-right:1px solid var(--border);border-top:1px solid var(--border)}

.tab-content{display:none;flex:1;overflow:hidden;flex-direction:column}
.tab-content.on{display:flex;animation:fi .2s ease}
@keyframes fi{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}

/* ─── Results Panel ─── */
.results-scroll{flex:1;overflow-y:auto;padding:16px}

/* Status Banner */
.status-banner{
  display:flex;align-items:center;gap:12px;
  background:var(--card);border:1px solid var(--border);border-radius:10px;
  padding:10px 16px;margin-bottom:14px;
}
.status-icon{font-size:20px}
.status-title{font-size:14px;font-weight:700}
.status-sub{font-size:11px;color:var(--t2);margin-top:1px}
.stat-success .status-title{color:var(--green)}
.stat-error .status-title{color:var(--pink)}
.stat-warn .status-title{color:var(--gold)}

/* Metric Cards */
.metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:14px}
.metric{background:var(--card2);border:1px solid var(--border);border-radius:8px;padding:10px 12px}
.metric-label{font-size:9px;color:var(--t3);text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px}
.metric-val{font-family:var(--mono);font-size:13px;font-weight:700;color:var(--gold)}
.metric-val.green{color:var(--green)}.metric-val.amber{color:var(--gold)}.metric-val.red{color:var(--pink)}

/* Iteration Table */
.tbl-wrap{background:var(--card);border:1px solid var(--border);border-radius:10px;overflow:hidden}
.tbl-hdr{
  display:flex;justify-content:space-between;align-items:center;
  padding:8px 14px;background:var(--card2);border-bottom:1px solid var(--border);
  font-size:10px;font-weight:700;color:var(--t2);text-transform:uppercase;letter-spacing:.5px;
}
.tbl-scroll{overflow-x:auto;max-height:320px;overflow-y:auto}
table{width:100%;border-collapse:collapse;font-family:var(--mono);font-size:10px}
thead th{
  position:sticky;top:0;background:var(--card2);color:var(--t2);
  font-size:9px;text-transform:uppercase;letter-spacing:.5px;font-weight:700;
  padding:6px 10px;text-align:right;border-bottom:1px solid var(--border);white-space:nowrap;
}
thead th:first-child{text-align:center}
tbody tr{border-bottom:1px solid var(--t4);transition:background .1s}
tbody tr:last-child{border-bottom:none}
tbody tr:hover{background:var(--card2)}
tbody tr.root-row{background:rgba(174,234,0,.07)}
tbody tr.root-row td{color:var(--green)}
td{padding:5px 10px;text-align:right;color:var(--t2)}
td:first-child{text-align:center;color:var(--t3)}
td.fx-col{color:var(--gold)}
td.ea-col{color:var(--accent-l)}

/* Convergence Plot SVG */
.plot-wrap{
  background:var(--card);border:1px solid var(--border);border-radius:10px;
  overflow:hidden;margin-top:12px;
}
.plot-hdr{padding:8px 14px;background:var(--card2);border-bottom:1px solid var(--border);
  font-size:10px;font-weight:700;color:var(--t2);text-transform:uppercase;letter-spacing:.5px}
#conv-plot{width:100%;height:180px;display:block}

/* Method Info Tab */
.info-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.info-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:14px}
.info-card-name{font-size:13px;font-weight:700;color:var(--accent-l);margin-bottom:6px}
.info-card-formula{
  font-family:var(--mono);font-size:11px;color:var(--gold);
  background:var(--card2);border:1px solid var(--border);border-radius:6px;
  padding:8px 10px;margin:6px 0;line-height:1.4;
}
.info-card-desc{font-size:10px;color:var(--t2);line-height:1.6}
.info-tag{display:inline-block;font-size:9px;font-weight:700;border-radius:4px;padding:2px 7px;margin-right:4px;margin-top:6px}
.tag-fast{background:rgba(174,234,0,.15);color:var(--green)}
.tag-slow{background:rgba(255,214,0,.15);color:var(--gold)}
.tag-noderiv{background:rgba(255,64,129,.15);color:var(--pink)}
.tag-complex{background:rgba(255,109,0,.15);color:var(--accent-l)}
.tag-bracket{background:rgba(255,64,129,.15);color:var(--pink)}
.tag-open{background:rgba(174,234,0,.15);color:var(--green)}

/* Empty state */
.empty-state{
  flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;
  gap:12px;color:var(--t3);padding:40px;text-align:center;
}
.empty-icon{font-size:48px;opacity:.3;animation:float 3s ease-in-out infinite}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
.empty-title{font-size:14px;font-weight:700;color:var(--t2)}
.empty-desc{font-size:11px;line-height:1.6;max-width:280px}

/* tooltip */
.tip{position:relative;cursor:help}
.tip::after{
  content:attr(data-tip);position:absolute;bottom:110%;left:50%;transform:translateX(-50%);
  background:#0A0F1E;color:var(--t2);font-size:9px;padding:4px 8px;border-radius:5px;
  white-space:nowrap;pointer-events:none;opacity:0;transition:opacity .2s;
  border:1px solid var(--border);z-index:99;
}
.tip:hover::after{opacity:1}

/* ghost btn */
.ghost{background:none;border:1px solid var(--border);border-radius:6px;color:var(--t3);
  font-size:10px;font-family:var(--font);padding:4px 10px;cursor:pointer;transition:all .15s}
.ghost:hover{border-color:var(--t2);color:var(--t2)}
.ghost.danger:hover{border-color:var(--red);color:var(--red)}

</style>
</head>
<body>

<!-- ══════ HEADER ══════ -->
<header class="hdr">
  <div class="hdr-l">
    <span class="hdr-icon">⚙️</span>
    <div>
      <div class="hdr-title">Root Finding <span>Calculator</span></div>
      <div class="hdr-sub">Numerical Methods · Nonlinear Equation Solver</div>
    </div>
  </div>
  <span class="authors">Divyansh Sharma · Jiya Madan · Kabir Bajaj</span>
</header>

<!-- ══════ MAIN LAYOUT ══════ -->
<div class="layout">

  <!-- ══ LEFT: INPUTS ══ -->
  <div class="left-col">
    <div class="sec-hdr"><span class="sec-hdr-dot"></span>Equation Setup</div>
    <div class="input-scroll">

      <!-- Function -->
      <div class="field-group">
        <div class="fglabel">f(x) — Equation <span class="badge">use x as variable</span></div>
        <input class="inp" id="fx" type="text" placeholder="e.g.  x**3 - x - 2"
               value="x**3 - x - 2" oninput="onFxChange()"/>
        <div style="font-size:10px;color:var(--t3);margin-top:5px;font-family:var(--mono)">
          Available: sin cos tan exp log sqrt pi e  |  use ** for power
        </div>
      </div>

      <!-- g(x) for Fixed-Point -->
      <div class="field-group" id="gx-group" style="display:none">
        <div class="fglabel">g(x) — Rearrangement <span class="badge">Fixed-Point only</span></div>
        <input class="inp" id="gx" type="text" placeholder="e.g.  (x + 2)**(1/3)"
               value="(x + 2)**(1/3)"/>
        <div style="font-size:10px;color:var(--t3);margin-top:5px">
          Rewrite f(x)=0 as x = g(x). Convergence requires |g'(x)| &lt; 1 near root.
        </div>
      </div>

      <!-- Method -->
      <div class="field-group">
        <div class="fglabel">Method</div>
        <div class="method-grid" id="method-grid">
          <div class="mcard sel" data-m="bisection" onclick="selMethod('bisection')">
            <span class="mcard-icon">✂️</span>
            <div class="mcard-name">Bisection</div>
            <div class="mcard-desc">Bracketing · Guaranteed</div>
          </div>
          <div class="mcard" data-m="false_position" onclick="selMethod('false_position')">
            <span class="mcard-icon">📐</span>
            <div class="mcard-name">False Position</div>
            <div class="mcard-desc">Bracketing · Faster</div>
          </div>
          <div class="mcard" data-m="newton" onclick="selMethod('newton')">
            <span class="mcard-icon">🚀</span>
            <div class="mcard-name">Newton–Raphson</div>
            <div class="mcard-desc">Open · Quadratic conv.</div>
          </div>
          <div class="mcard" data-m="secant" onclick="selMethod('secant')">
            <span class="mcard-icon">🔗</span>
            <div class="mcard-name">Secant</div>
            <div class="mcard-desc">Open · No derivative</div>
          </div>
          <div class="mcard" data-m="fixed_point" onclick="selMethod('fixed_point')">
            <span class="mcard-icon">🔄</span>
            <div class="mcard-name">Fixed-Point</div>
            <div class="mcard-desc">Iterative · x = g(x)</div>
          </div>
          <div class="mcard" data-m="muller" onclick="selMethod('muller')">
            <span class="mcard-icon">🌀</span>
            <div class="mcard-name">Muller's</div>
            <div class="mcard-desc">Open · Complex roots</div>
          </div>
        </div>
        <div class="method-detail vis" id="method-hint">
          <span class="formula">x_new = (a + b) / 2</span><br>
          Guaranteed convergence. Requires bracket [a,b] where f(a)·f(b) &lt; 0.
          Linear convergence (one bit per iteration).
        </div>
      </div>

      <!-- Parameters -->
      <div class="field-group">
        <div class="fglabel">Parameters</div>
        <div id="params-container"></div>
      </div>

      <!-- Tolerance & Max Iter -->
      <div class="field-group">
        <div class="fglabel">Solver Settings</div>
        <div class="param-row">
          <div class="param-box tip" data-tip="Convergence tolerance">
            <div class="param-label">Tolerance</div>
            <input class="param-inp" id="tol" type="number" value="1e-7" step="any"/>
          </div>
          <div class="param-box tip" data-tip="Maximum iterations">
            <div class="param-label">Max Iterations</div>
            <input class="param-inp" id="maxiter" type="number" value="100" min="1" max="1000"/>
          </div>
        </div>
      </div>

      <button class="solve-btn" id="solve-btn" onclick="solve()">▶ Solve</button>
    </div>
  </div>

  <!-- ══ RIGHT: RESULTS ══ -->
  <div class="right-col">
    <div class="tabs-bar">
      <button class="tab-btn on" id="tb-result" onclick="switchTab('result')">📊 Results</button>
      <button class="tab-btn" id="tb-table"  onclick="switchTab('table')">📋 Iteration Table</button>
      <button class="tab-btn" id="tb-plot"   onclick="switchTab('plot')">📈 Convergence</button>
      <button class="tab-btn" id="tb-info"   onclick="switchTab('info')">📚 Method Guide</button>
    </div>

    <!-- Results Tab -->
    <div class="tab-content on" id="tc-result">
      <div class="results-scroll">
        <div id="empty-state" class="empty-state">
          <div class="empty-icon">∫</div>
          <div class="empty-title">Ready to Solve</div>
          <div class="empty-desc">
            Enter your equation f(x), select a method, set the parameters,
            then click <strong style="color:var(--accent-l)">▶ Solve</strong>.
          </div>
        </div>
        <div id="results-content" style="display:none"></div>
      </div>
    </div>

    <!-- Iteration Table Tab -->
    <div class="tab-content" id="tc-table">
      <div class="results-scroll">
        <div id="iter-table-container">
          <div class="empty-state">
            <div class="empty-icon">🗂️</div>
            <div class="empty-title">No Data Yet</div>
            <div class="empty-desc">Run the solver to see the full iteration table.</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Convergence Plot Tab -->
    <div class="tab-content" id="tc-plot">
      <div class="results-scroll">
        <div id="plot-container">
          <div class="empty-state">
            <div class="empty-icon">📉</div>
            <div class="empty-title">No Plot Yet</div>
            <div class="empty-desc">Run the solver to see the convergence chart.</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Method Info Tab -->
    <div class="tab-content" id="tc-info">
      <div class="results-scroll">
        <div class="info-grid">
          <div class="info-card">
            <div class="info-card-name">✂️ Bisection</div>
            <div class="info-card-formula">x_new = (a + b) / 2<br>Update: if f(a)·f(c)&lt;0 → b=c else a=c</div>
            <div class="info-card-desc">Divides bracket in half each iteration. Guaranteed to converge. Slow but reliable.</div>
            <span class="info-tag tag-bracket">Bracketing</span>
            <span class="info-tag tag-slow">Linear Conv.</span>
          </div>
          <div class="info-card">
            <div class="info-card-name">📐 False Position (Regula Falsi)</div>
            <div class="info-card-formula">c = b - f(b)·(b-a) / (f(b)-f(a))</div>
            <div class="info-card-desc">Uses linear interpolation instead of midpoint. Usually faster than bisection but can stagnate.</div>
            <span class="info-tag tag-bracket">Bracketing</span>
            <span class="info-tag tag-slow">Superlinear</span>
          </div>
          <div class="info-card">
            <div class="info-card-name">🚀 Newton–Raphson</div>
            <div class="info-card-formula">x_new = x - f(x) / f'(x)</div>
            <div class="info-card-desc">Uses the tangent line at each point. Very fast (quadratic) near the root. Requires derivative.</div>
            <span class="info-tag tag-open">Open</span>
            <span class="info-tag tag-fast">Quadratic Conv.</span>
          </div>
          <div class="info-card">
            <div class="info-card-name">🔗 Secant</div>
            <div class="info-card-formula">x₂ = x₁ - f(x₁)·(x₁-x₀) / (f(x₁)-f(x₀))</div>
            <div class="info-card-desc">Approximates f'(x) using two prior points. No derivative needed. Superlinear convergence.</div>
            <span class="info-tag tag-open">Open</span>
            <span class="info-tag tag-noderiv">No Derivative</span>
          </div>
          <div class="info-card">
            <div class="info-card-name">🔄 Fixed-Point Iteration</div>
            <div class="info-card-formula">x_new = g(x)<br>Converges if |g'(x)| &lt; 1 near root</div>
            <div class="info-card-desc">Rearrange f(x)=0 to x=g(x). Very simple, but convergence depends heavily on the choice of g(x).</div>
            <span class="info-tag tag-open">Open</span>
            <span class="info-tag tag-slow">Linear Conv.</span>
          </div>
          <div class="info-card">
            <div class="info-card-name">🌀 Muller's Method</div>
            <div class="info-card-formula">Fits parabola through 3 points,<br>uses quadratic formula for next root</div>
            <div class="info-card-desc">Can find complex roots. Uses three starting points. Faster than secant with order ≈ 1.84.</div>
            <span class="info-tag tag-open">Open</span>
            <span class="info-tag tag-complex">Complex Roots</span>
            <span class="info-tag tag-fast">Order 1.84</span>
          </div>
        </div>
      </div>
    </div>

  </div>
</div>

<script>
'use strict';
// ─── State ───
let currentMethod = 'bisection';
let lastRows = [];
let lastEarr = [];

// ─── Method hints ───
const METHOD_HINTS = {
  bisection:     ['<span class="formula">x_new = (a + b) / 2</span><br>Guaranteed convergence. Requires bracket [a,b] where f(a)·f(b) &lt; 0. Linear convergence.',
                  [{label:'Lower Bound (a)', id:'p-a', val:1}, {label:'Upper Bound (b)', id:'p-b', val:2}]],
  false_position:['<span class="formula">c = b - f(b)·(b-a) / (f(b)-f(a))</span><br>Linear interpolation between bracket points. Usually faster than bisection.',
                  [{label:'Lower Bound (a)', id:'p-a', val:1}, {label:'Upper Bound (b)', id:'p-b', val:2}]],
  newton:        ['<span class="formula">x_new = x - f(x) / f\'(x)</span><br>Numerical derivative (central difference, h=1e-7). Quadratic convergence near root.',
                  [{label:'Initial Guess x₀', id:'p-x0', val:1.5}]],
  secant:        ['<span class="formula">x₂ = x₁ - f(x₁)·(x₁-x₀)/(f(x₁)-f(x₀))</span><br>No derivative needed. Two starting points required.',
                  [{label:'First Guess x₀', id:'p-x0', val:1}, {label:'Second Guess x₁', id:'p-x1', val:2}]],
  fixed_point:   ['<span class="formula">x_new = g(x)</span><br>Rearrange f(x)=0 as x=g(x). Convergence requires |g\'(x)| &lt; 1 near root.',
                  [{label:'Initial Guess x₀', id:'p-x0', val:1}]],
  muller:        ['<span class="formula">Fits parabola through (x₀,f₀),(x₁,f₁),(x₂,f₂)</span><br>Three starting points. Can handle complex roots. Order ≈ 1.84.',
                  [{label:'x₀', id:'p-x0', val:1},{label:'x₁', id:'p-x1', val:1.5},{label:'x₂', id:'p-x2', val:2}]],
};

function selMethod(m){
  currentMethod = m;
  document.querySelectorAll('.mcard').forEach(c => c.classList.toggle('sel', c.dataset.m === m));
  const [hint, params] = METHOD_HINTS[m];
  document.getElementById('method-hint').innerHTML = hint;
  document.getElementById('method-hint').classList.add('vis');
  buildParams(params);
  document.getElementById('gx-group').style.display = (m === 'fixed_point') ? 'block' : 'none';
}

function buildParams(params){
  const c = document.getElementById('params-container');
  c.innerHTML = '';
  const grid = document.createElement('div');
  // Use 3-column grid when there are 3 params (Muller), else 2-column
  grid.style.cssText = `display:grid;grid-template-columns:repeat(${Math.min(params.length,3)},1fr);gap:8px;margin-bottom:2px`;
  params.forEach(p => {
    const box = document.createElement('div');
    box.className = 'param-box';
    box.innerHTML = `<div class="param-label">${p.label}</div>
      <input class="param-inp" id="${p.id}" type="number" value="${p.val}" step="any"/>`;
    grid.appendChild(box);
  });
  c.appendChild(grid);
}

function onFxChange(){ /* live preview future */ }

// ─── Tab Switching ───
function switchTab(n){
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('on'));
  document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('on'));
  document.getElementById('tb-'+n).classList.add('on');
  document.getElementById('tc-'+n).classList.add('on');
}

// ─── SOLVE (calls Python via kernel bridge) ───
function solve(){
  const fx   = document.getElementById('fx').value.trim();
  const gx   = document.getElementById('gx') ? document.getElementById('gx').value.trim() : '';
  const tol  = parseFloat(document.getElementById('tol').value) || 1e-7;
  const mi   = parseInt(document.getElementById('maxiter').value) || 100;
  const m    = currentMethod;

  // Gather method-specific params
  const getVal = id => { const el = document.getElementById(id); return el ? parseFloat(el.value) : NaN; };
  let params = {};
  if (m === 'bisection' || m === 'false_position') {
    params = {a: getVal('p-a'), b: getVal('p-b')};
  } else if (m === 'newton' || m === 'fixed_point') {
    params = {x0: getVal('p-x0')};
  } else if (m === 'secant') {
    params = {x0: getVal('p-x0'), x1: getVal('p-x1')};
  } else if (m === 'muller') {
    params = {x0: getVal('p-x0'), x1: getVal('p-x1'), x2: getVal('p-x2')};
  }

  // Validate
  for (const [k,v] of Object.entries(params)) {
    if (isNaN(v)) { showError('Parameter "' + k + '" is not a valid number.'); return; }
  }
  if (!fx) { showError('Please enter f(x).'); return; }

  // Store state and run solver
  window._rootSolverState = {method:m, fx, gx, tol, maxiter:mi, params};

  // Animate button
  const btn = document.getElementById('solve-btn');
  btn.textContent = '⏳ Solving…';
  btn.disabled = true;

  // Use the pure-JS solver — works in Colab, Jupyter, and standalone
  // (The Colab kernel bridge doesn't reliably pass application/json back to JS)
  setTimeout(() => {
    try {
      const d = window.rfSolveLocal(window._rootSolverState);
      displayResults(d);
    } catch(e) {
      showError('Solver error: ' + e.message);
    }
    btn.textContent = '▶ Solve';
    btn.disabled = false;
  }, 50); // tiny delay so browser can repaint the button state
}

// ─── Display Results ───
function displayResults(d){
  document.getElementById('empty-state').style.display = 'none';
  const rc = document.getElementById('results-content');
  rc.style.display = 'block';

  const ok = d.success;
  const rootStr = d.root !== null ? (typeof d.root === 'object' ? `${d.root.r} + ${d.root.i}j` : Number(d.root).toPrecision(12)) : 'N/A';
  const fxStr   = d.fx_root !== null ? Number(d.fx_root).toExponential(6) : '—';
  const iters   = d.iterations;
  const ea_last = d.ea_last !== null ? Number(d.ea_last).toExponential(4) : '—';

  const statusClass = ok ? 'stat-success' : 'stat-error';
  const statusIcon  = ok ? '✅' : '❌';
  const warnBanner  = d.warning ? `<div class="status-banner stat-warn" style="margin-top:8px">
    <span class="status-icon">⚠️</span>
    <div><div class="status-title">Warning</div><div class="status-sub">${d.warning}</div></div></div>` : '';

  rc.innerHTML = `
    <div class="status-banner ${statusClass}">
      <span class="status-icon">${statusIcon}</span>
      <div>
        <div class="status-title">${ok ? 'Root Found!' : 'Failed / No Convergence'}</div>
        <div class="status-sub">Method: ${d.method_name} &nbsp;|&nbsp; f(x) = ${escH(d.fx_str)}</div>
      </div>
    </div>
    ${warnBanner}
    <div class="metrics" style="margin-top:12px">
      <div class="metric">
        <div class="metric-label">Root x*</div>
        <div class="metric-val ${ok?'green':'red'}">${rootStr}</div>
      </div>
      <div class="metric">
        <div class="metric-label">f(x*)</div>
        <div class="metric-val amber">${fxStr}</div>
      </div>
      <div class="metric">
        <div class="metric-label">Iterations</div>
        <div class="metric-val">${iters}</div>
      </div>
      <div class="metric">
        <div class="metric-label">Final Error (εₐ)</div>
        <div class="metric-val">${ea_last}</div>
      </div>
      <div class="metric">
        <div class="metric-label">Tolerance</div>
        <div class="metric-val">${d.tol}</div>
      </div>
      <div class="metric">
        <div class="metric-label">Converged</div>
        <div class="metric-val ${ok?'green':'red'}">${ok ? 'Yes ✓' : 'No ✗'}</div>
      </div>
    </div>`;

  // Populate iteration table
  buildIterTable(d);
  buildPlot(d);

  // Switch to results tab
  switchTab('result');
}

function escH(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

function showError(msg){
  document.getElementById('empty-state').style.display = 'none';
  const rc = document.getElementById('results-content');
  rc.style.display = 'block';
  rc.innerHTML = `<div class="status-banner stat-error">
    <span class="status-icon">❌</span>
    <div><div class="status-title">Error</div><div class="status-sub">${escH(msg)}</div></div>
  </div>`;
  switchTab('result');
}

// ─── Iteration Table ───
function buildIterTable(d){
  const rows = d.rows || [];
  const hdrs = d.col_headers || [];
  lastRows = rows;

  const wrap = document.getElementById('iter-table-container');
  if (!rows.length){ wrap.innerHTML = '<div class="empty-state"><div class="empty-icon">🗂️</div><div class="empty-title">No Rows</div></div>'; return; }

  const maxR = rows.length;
  const isRoot = (i) => i === maxR; // highlight last row

  let thead = '<thead><tr>' + hdrs.map((h,i) => `<th>${h}</th>`).join('') + '</tr></thead>';
  let tbody = '<tbody>';
  rows.forEach((row, ri) => {
    const cls = ri === rows.length-1 ? ' class="root-row"' : '';
    tbody += `<tr${cls}>`;
    row.forEach((cell, ci) => {
      const isEa = ci === row.length - 1 && ci > 0;
      const isFx = hdrs[ci] && hdrs[ci].toLowerCase().includes('f(');
      const cls2 = isEa ? ' class="ea-col"' : isFx ? ' class="fx-col"' : '';
      let v = cell;
      if (typeof v === 'number') v = Math.abs(v) < 1e-3 && v !== 0 ? v.toExponential(6) : parseFloat(v.toPrecision(9));
      tbody += `<td${cls2}>${v}</td>`;
    });
    tbody += '</tr>';
  });
  tbody += '</tbody>';

  wrap.innerHTML = `
    <div class="tbl-wrap">
      <div class="tbl-hdr">
        <span>Iteration Table — ${rows.length} rows</span>
        <button class="ghost" onclick="exportCSV()">Export CSV</button>
      </div>
      <div class="tbl-scroll"><table>${thead}${tbody}</table></div>
    </div>`;
}

// ─── Convergence Plot (pure SVG) ───
function buildPlot(d){
  const rows = d.rows || [];
  if (!rows.length){ document.getElementById('plot-container').innerHTML = '<div class="empty-state"><div class="empty-icon">📉</div></div>'; return; }

  // Extract error col (last col) — skip first row if ea=0
  const errors = rows.map(r => Math.abs(Number(r[r.length-1]))).filter(e => e > 0 && isFinite(e));
  lastEarr = errors;
  if (!errors.length){ document.getElementById('plot-container').innerHTML = '<div class="empty-state"><div class="empty-icon">📉</div><div class="empty-title">No error data.</div></div>'; return; }

  const W=600, H=160, PL=52, PR=16, PT=12, PB=32;
  const logE = errors.map(e => Math.log10(e));
  const minL = Math.min(...logE), maxL = Math.max(...logE);
  const range = maxL - minL || 1;
  const n = errors.length;

  const sx = i => PL + (i/(n-1||1))*(W-PL-PR);
  const sy = v => PT + (1 - (v-minL)/range)*(H-PT-PB);

  // Build polyline
  let pts = errors.map((e,i) => `${sx(i).toFixed(1)},${sy(Math.log10(e)).toFixed(1)}`).join(' ');
  // Grid lines
  const ticks = 4;
  let grid = '', ylabels = '';
  for(let t=0;t<=ticks;t++){
    const y = PT + t*(H-PT-PB)/ticks;
    const logVal = maxL - t*range/ticks;
    grid += `<line x1="${PL}" y1="${y.toFixed(1)}" x2="${W-PR}" y2="${y.toFixed(1)}" stroke="#1C2E4A" stroke-width="1"/>`;
    ylabels += `<text x="${PL-4}" y="${(y+3).toFixed(1)}" fill="#4A5E78" font-size="9" text-anchor="end">${logVal.toFixed(1)}</text>`;
  }

  const svg = `<svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:180px">
    <rect width="${W}" height="${H}" fill="#0E1525"/>
    ${grid}
    <text x="${PL-38}" y="${PT+H/2-PB/2}" fill="#4A5E78" font-size="9" text-anchor="middle" transform="rotate(-90,${PL-38},${PT+H/2-PB/2})">log₁₀(Error)</text>
    <text x="${PL + (W-PL-PR)/2}" y="${H-4}" fill="#4A5E78" font-size="9" text-anchor="middle">Iteration</text>
    ${ylabels}
    <defs>
      <linearGradient id="lineg" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#FF6D00" stop-opacity="0.7"/>
        <stop offset="100%" stop-color="#FF6D00" stop-opacity="0.05"/>
      </linearGradient>
    </defs>
    <polyline points="${pts}" fill="none" stroke="#FF6D00" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>
    ${errors.map((e,i)=>`<circle cx="${sx(i).toFixed(1)}" cy="${sy(Math.log10(e)).toFixed(1)}" r="3" fill="#AEEA00"/>`).join('')}
  </svg>`;

  document.getElementById('plot-container').innerHTML = `
    <div class="plot-wrap">
      <div class="plot-hdr">Convergence — log₁₀(Approx. Error) vs Iteration</div>
      ${svg}
    </div>`;
}

// ─── Export CSV ───
function exportCSV(){
  if (!lastRows.length) return;
  const csv = lastRows.map(r => r.join(',')).join('\n');
  const a = document.createElement('a');
  a.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv);
  a.download = 'root_iterations.csv';
  a.click();
}

// ════════════════════════════════════════════════
//  LOCAL / STANDALONE SOLVER (pure JS)
//  Mirrors the Python backend so the app works
//  even without a Python kernel.
// ════════════════════════════════════════════════
window.rfSolveLocal = function(state){
  const {method, fx, gx, tol, maxiter, params} = state;
  const METHOD_NAMES = {
    bisection:'Bisection', false_position:'False Position (Regula Falsi)',
    newton:'Newton–Raphson', secant:'Secant',
    fixed_point:'Fixed-Point Iteration', muller:"Muller's Method"
  };

  const safeEval = (expr, x) => {
    try {
      const fn = new Function('x','sin','cos','tan','asin','acos','atan',
        'sinh','cosh','tanh','exp','log','log2','log10','sqrt','abs','pi','e',
        '"use strict"; return (' + expr + ');');
      return fn(x, Math.sin, Math.cos, Math.tan, Math.asin, Math.acos, Math.atan,
        Math.sinh, Math.cosh, Math.tanh, Math.exp, Math.log, Math.log2, Math.log10,
        Math.sqrt, Math.abs, Math.PI, Math.E);
    } catch(e){ throw new Error('Invalid f(x): ' + e.message); }
  };
  const deriv = (expr, x) => (safeEval(expr, x+1e-7) - safeEval(expr, x-1e-7)) / 2e-7;
  const fmt = v => typeof v === 'number' ? v : v;

  let root=null, rows=[], warning=null, success=false, col_headers=[];

  try {
    if (method === 'bisection' || method === 'false_position'){
      let {a,b} = params;
      const fa0 = safeEval(fx,a), fb0 = safeEval(fx,b);
      if (fa0*fb0 > 0) return {success:false,root:null,fx_root:null,iterations:0,ea_last:null,tol,rows:[],col_headers:[],method_name:METHOD_NAMES[method],fx_str:fx,warning:'f(a) and f(b) must have opposite signs.'};
      col_headers = ['Iter','a','b','c','f(c)','|εₐ|'];
      let fa=fa0, c=a, cOld=a;
      for(let i=1;i<=maxiter;i++){
        const fb=safeEval(fx,b);
        fa=safeEval(fx,a);
        if (method==='bisection') c=(a+b)/2;
        else c = b - fb*(b-a)/(fb-fa);
        const fc=safeEval(fx,c);
        const ea=i===1?(b-a)/2:Math.abs(c-cOld);
        rows.push([i, +a.toPrecision(9), +b.toPrecision(9), +c.toPrecision(9), +fc.toPrecision(6), +ea.toExponential(6)]);
        if(Math.abs(fc)<tol || ea<tol){ success=true; break; }
        if(fa*fc<0) b=c; else a=c;
        cOld=c;
      }
      root=c;
    } else if (method === 'newton'){
      let x=params.x0;
      col_headers=['Iter','xₙ','f(xₙ)','f\'(xₙ)','xₙ₊₁','|εₐ|'];
      for(let i=1;i<=maxiter;i++){
        const fxv=safeEval(fx,x), fpx=deriv(fx,x);
        if(Math.abs(fpx)<1e-14){ warning='Derivative too small.'; break; }
        const xn=x-fxv/fpx, ea=Math.abs(xn-x);
        rows.push([i,+x.toPrecision(9),+fxv.toPrecision(6),+fpx.toPrecision(6),+xn.toPrecision(9),+ea.toExponential(6)]);
        if(ea<tol && Math.abs(fxv)<tol){ success=true; x=xn; break; }
        x=xn;
      }
      root=x;
    } else if (method === 'secant'){
      let x0=params.x0, x1=params.x1;
      col_headers=['Iter','x₀','x₁','x₂','f(x₂)','|εₐ|'];
      for(let i=1;i<=maxiter;i++){
        const f0=safeEval(fx,x0), f1=safeEval(fx,x1);
        if(Math.abs(f1-f0)<1e-14){ warning='f(x1)≈f(x0), division by zero risk.'; break; }
        const x2=x1-f1*(x1-x0)/(f1-f0), ea=Math.abs(x2-x1);
        rows.push([i,+x0.toPrecision(9),+x1.toPrecision(9),+x2.toPrecision(9),+safeEval(fx,x2).toPrecision(6),+ea.toExponential(6)]);
        if(ea<tol){ success=true; x1=x2; break; }
        x0=x1; x1=x2;
      }
      root=x1;
    } else if (method === 'fixed_point'){
      let x=params.x0;
      col_headers=['Iter','xₙ','xₙ₊₁','f(xₙ₊₁)','|εₐ|'];
      for(let i=1;i<=maxiter;i++){
        const xn=safeEval(gx||fx,x), ea=Math.abs(xn-x), fxn=safeEval(fx,xn);
        rows.push([i,+x.toPrecision(9),+xn.toPrecision(9),+fxn.toPrecision(6),+ea.toExponential(6)]);
        if(ea<tol){ success=true; x=xn; break; }
        x=xn;
      }
      root=x;
    } else if (method === 'muller'){
      let x0=params.x0, x1=params.x1, x2=params.x2;
      col_headers=['Iter','x₀','x₁','x₂','x₃','f(x₂)','|εₐ|'];
      for(let i=1;i<=maxiter;i++){
        const f0=safeEval(fx,x0), f1=safeEval(fx,x1), f2=safeEval(fx,x2);
        const h1=x1-x0, h2=x2-x1;
        const d1=h1!==0?(f1-f0)/h1:0, d2=h2!==0?(f2-f1)/h2:0;
        const a=(h2+h1)!==0?(d2-d1)/(h2+h1):0;
        const b=a*h2+d2, c=f2;
        const disc=b*b-4*a*c;
        let dx=0;
        if(disc>=0){ const sq=Math.sqrt(disc); const den=Math.abs(b+sq)>Math.abs(b-sq)?(b+sq):(b-sq); dx=den!==0?-2*c/den:0; }
        else { dx=0; warning='Complex root encountered — shown as real part only.'; }
        const x3=x2+dx, ea=Math.abs(dx);
        rows.push([i,+x0.toPrecision(9),+x1.toPrecision(9),+x2.toPrecision(9),+x3.toPrecision(9),+f2.toPrecision(6),+ea.toExponential(6)]);
        if(ea<tol){ success=true; x2=x3; break; }
        x0=x1; x1=x2; x2=x3;
      }
      root=x2;
    }
  } catch(e){
    return {success:false,root:null,fx_root:null,iterations:rows.length,ea_last:null,
      tol,rows,col_headers,method_name:METHOD_NAMES[method],fx_str:fx,warning:e.message};
  }

  const fx_root = root !== null ? (() => { try{ return safeEval(fx, root); } catch(_){ return null; } })() : null;
  if (!success && !warning) warning = 'Max iterations reached — result may not be accurate.';
  return {
    success, root, fx_root, iterations: rows.length,
    ea_last: rows.length ? rows[rows.length-1][rows[0].length-1] : null,
    tol, rows, col_headers, method_name:METHOD_NAMES[method], fx_str:fx,
    warning: warning || null
  };
};

// ─── Init ───
selMethod('bisection');
</script>
</body>
</html>
"""


# ═══════════════════════════════════════════════════════════
#  COLAB KERNEL CALLBACK  (Python backend called from JS)
# ═══════════════════════════════════════════════════════════
def _py_solve(params_json_str):
    """Kernel function called by Colab JS via invokeFunction."""
    import json
    state = json.loads(json.loads(params_json_str))
    method   = state['method']
    fx_str   = state['fx']
    gx_str   = state.get('gx', '')
    tol      = float(state.get('tol', 1e-7))
    maxiter  = int(state.get('maxiter', 100))
    params   = state.get('params', {})

    METHOD_NAMES = {
        'bisection':     'Bisection',
        'false_position':'False Position (Regula Falsi)',
        'newton':        'Newton–Raphson',
        'secant':        'Secant',
        'fixed_point':   'Fixed-Point Iteration',
        'muller':        "Muller's Method",
    }

    COL_HEADERS = {
        'bisection':     ['Iter','a','b','c','f(c)','|εₐ|'],
        'false_position':['Iter','a','b','c','f(c)','|εₐ|'],
        'newton':        ['Iter','xₙ','f(xₙ)','f\'(xₙ)','xₙ₊₁','|εₐ|'],
        'secant':        ['Iter','x₀','x₁','x₂','f(x₂)','|εₐ|'],
        'fixed_point':   ['Iter','xₙ','xₙ₊₁','f(xₙ₊₁)','|εₐ|'],
        'muller':        ['Iter','x₀','x₁','x₂','x₃','f(x₂)','|εₐ|'],
    }

    root, rows_raw, warning = None, [], None

    try:
        if method == 'bisection':
            root, rows_raw, warning = RootSolver.bisection(fx_str, params['a'], params['b'], tol, maxiter)
        elif method == 'false_position':
            root, rows_raw, warning = RootSolver.false_position(fx_str, params['a'], params['b'], tol, maxiter)
        elif method == 'newton':
            root, rows_raw, warning = RootSolver.newton_raphson(fx_str, params['x0'], tol, maxiter)
        elif method == 'secant':
            root, rows_raw, warning = RootSolver.secant(fx_str, params['x0'], params['x1'], tol, maxiter)
        elif method == 'fixed_point':
            root, rows_raw, warning = RootSolver.fixed_point(fx_str, gx_str or fx_str, params['x0'], tol, maxiter)
        elif method == 'muller':
            root, rows_raw, warning = RootSolver.muller(fx_str, params['x0'], params['x1'], params['x2'], tol, maxiter)
    except Exception as e:
        warning = str(e)

    success = root is not None and warning is None
    fx_root = None
    if root is not None:
        try:
            fx_root = _safe_eval(fx_str, root.real if isinstance(root, complex) else root)
        except Exception:
            fx_root = None

    root_out = None
    if isinstance(root, complex):
        root_out = {'r': round(root.real, 10), 'i': round(root.imag, 10)}
    elif root is not None:
        root_out = root

    rows_serialised = [list(r) for r in rows_raw]

    result = {
        'success':     success,
        'root':        root_out,
        'fx_root':     fx_root,
        'iterations':  len(rows_raw),
        'ea_last':     rows_serialised[-1][-1] if rows_serialised else None,
        'tol':         tol,
        'rows':        rows_serialised,
        'col_headers': COL_HEADERS.get(method, []),
        'method_name': METHOD_NAMES.get(method, method),
        'fx_str':      fx_str,
        'warning':     warning,
    }
    return result


# ═══════════════════════════════════════════════════════════
#  LAUNCH
# ═══════════════════════════════════════════════════════════
def launch():
    try:
        from IPython.display import display, HTML
        import google.colab.output as colab_output

        # Register Python callback for JS kernel bridge
        colab_output.register_callback('rf_solve', _py_solve)

        print("✅  Root Finding Calculator loaded! Interact below.")
        print("    • Enter f(x), select method, set parameters, click ▶ Solve")
        print("    • All 6 methods work — results appear instantly in the GUI\n")
        display(HTML(f'<div style="height:100vh;background:#070B15">{ROOT_FINDER_HTML}</div>'))

    except (ImportError, ModuleNotFoundError):
        # Not Colab — open in browser
        import os, tempfile, webbrowser
        path = os.path.join(tempfile.gettempdir(), "root_finding_calc.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(ROOT_FINDER_HTML)
        webbrowser.open("file://" + path)
        print(f"✅  Opened Root Finding Calculator in browser: {path}")


# ═══════════════════════════════════════════════════════════
#  STANDALONE PYTHON  (no GUI — direct function calls)
# ═══════════════════════════════════════════════════════════
def solve_cli(fx_str, method='bisection', a=None, b=None, x0=None, x1=None, x2=None,
              gx_str=None, tol=1e-7, max_iter=100, verbose=True):
    """
    Command-line / notebook helper to run any root-finding method and print results.

    Examples
    --------
    solve_cli('x**3 - x - 2', method='bisection', a=1, b=2)
    solve_cli('x**3 - x - 2', method='newton', x0=1.5)
    solve_cli('cos(x) - x', method='secant', x0=0.5, x1=1.0)
    solve_cli('x**3 - x - 2', method='fixed_point', x0=1.5, gx_str='(x+2)**(1/3)')
    """
    dispatch = {
        'bisection':     lambda: RootSolver.bisection(fx_str, a, b, tol, max_iter),
        'false_position':lambda: RootSolver.false_position(fx_str, a, b, tol, max_iter),
        'newton':        lambda: RootSolver.newton_raphson(fx_str, x0, tol, max_iter),
        'secant':        lambda: RootSolver.secant(fx_str, x0, x1, tol, max_iter),
        'fixed_point':   lambda: RootSolver.fixed_point(fx_str, gx_str or fx_str, x0, tol, max_iter),
        'muller':        lambda: RootSolver.muller(fx_str, x0, x1, x2, tol, max_iter),
    }
    if method not in dispatch:
        raise ValueError(f"Unknown method '{method}'. Choose from: {list(dispatch)}")

    root, rows, warning = dispatch[method]()

    if verbose:
        sep = '═' * 52
        print(sep)
        print(f"  Method        : {method.replace('_',' ').title()}")
        print(f"  f(x)          : {fx_str}")
        print(f"  Tolerance     : {tol:.2e}   Max Iter: {max_iter}")
        print('─' * 52)
        if root is not None:
            fr = _safe_eval(fx_str, root.real if isinstance(root, complex) else root)
            print(f"  Root x*       : {root}")
            print(f"  f(x*)         : {fr:.6e}")
            print(f"  Iterations    : {len(rows)}")
            ea_last = rows[-1][-1] if rows else None
            print(f"  Final |εₐ|   : {ea_last:.4e}" if ea_last else "  Final |εₐ|   : —")
        if warning:
            print(f"  ⚠ Warning     : {warning}")
        print(sep)

    return root, rows


if __name__ == "__main__":
    launch()
