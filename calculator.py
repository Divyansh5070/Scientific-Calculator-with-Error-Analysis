"""
Scientific Calculator with Error Analysis
Numerical Methods Project
Authors: Divyansh Sharma · Jiya Madan · Kabir Bajaj
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math, os

os.environ["TK_SILENCE_DEPRECATION"] = "1"

# ── Colours ──────────────────────────────────────────
BG     = "#0B0F1A"
CARD   = "#131929"
CARD2  = "#1A2235"
BORDER = "#263350"
PURPLE = "#7C3AED"
PL     = "#9D5FF5"
CYAN   = "#22D3EE"
GREEN  = "#34D399"
TEXT   = "#F1F5F9"
T2     = "#94A3B8"
T3     = "#475569"
NUM    = "#1C2A42"; NUH = "#2A3F60"
OP     = "#1F1050"; OPH = "#342085"
FN     = "#0A2336"; FNH = "#10385A"
EQ     = "#5B21B6"; EQH = "#7C3AED"
CLR    = "#7F1D1D"; CLH = "#DC2626"


# ── Utility Button ────────────────────────────────────
def Btn(parent, label, bg, hover, cmd,
        fg=TEXT, font=("Arial", 11, "bold"), cw=7, rh=2):
    b = tk.Button(parent, text=label, bg=bg, fg=fg,
                  activebackground=hover, activeforeground=fg,
                  font=font, relief="flat", bd=0,
                  highlightthickness=0, cursor="hand2",
                  width=cw, height=rh, command=cmd)
    b.bind("<Enter>", lambda e: b.config(bg=hover))
    b.bind("<Leave>", lambda e: b.config(bg=bg))
    return b


# ── Error Engine ──────────────────────────────────────
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
        f = 10 ** dp; return abs(v - math.trunc(v * f) / f)
    @staticmethod
    def meps():
        e = 1.0
        while (1.0 + e / 2) != 1.0: e /= 2
        return e
    @staticmethod
    def prop_add(da, db):       return math.sqrt(da**2 + db**2)
    @staticmethod
    def prop_mul(a, b, da, db):
        return 0 if a == 0 or b == 0 else abs(a*b)*math.sqrt((da/a)**2 + (db/b)**2)
    @staticmethod
    def prop_div(a, b, da, db):
        if b == 0: return float('inf')
        return 0 if a == 0 else abs(a/b)*math.sqrt((da/a)**2 + (db/b)**2)
    @staticmethod
    def taylor(fn, x, n):
        if fn == "sin":
            ex = math.sin(x)
            ap = sum((-1)**k * x**(2*k+1) / math.factorial(2*k+1) for k in range(n))
        elif fn == "cos":
            ex = math.cos(x)
            ap = sum((-1)**k * x**(2*k) / math.factorial(2*k) for k in range(n))
        else:
            ex = math.exp(x)
            ap = sum(x**k / math.factorial(k) for k in range(n))
        return ex, ap, abs(ex - ap)
    @staticmethod
    def sigfig(v, n):
        if v == 0: return 0
        d = math.ceil(math.log10(abs(v)))
        return round(v * 10**(n-d)) / 10**(n-d)
    @staticmethod
    def evaluate(expr, angle_mode):
        def to_r(x):
            if angle_mode == "DEG":  return math.radians(x)
            if angle_mode == "GRAD": return x * math.pi / 200
            return x
        def fr_r(r):
            if angle_mode == "DEG":  return math.degrees(r)
            if angle_mode == "GRAD": return r * 200 / math.pi
            return r
        ns = {
            "sin":  lambda x: math.sin(to_r(x)),
            "cos":  lambda x: math.cos(to_r(x)),
            "tan":  lambda x: math.tan(to_r(x)),
            "asin": lambda x: fr_r(math.asin(x)),
            "acos": lambda x: fr_r(math.acos(x)),
            "atan": lambda x: fr_r(math.atan(x)),
            "sqrt": math.sqrt,
            "cbrt": lambda x: math.copysign(abs(x)**(1/3), x),
            "log10": math.log10, "log2": math.log2,
            "ln": math.log, "exp": math.exp,
            "inv": lambda x: 1/x,
            "fact": math.factorial,
            "abs": abs, "pi": math.pi, "e": math.e,
        }
        return eval(expr.replace("^", "**"), {"__builtins__": {}}, ns)


# ═══════════════════════════════════════════════════
#  DISPLAY HELPER  — uses Entry widget (macOS-safe)
# ═══════════════════════════════════════════════════
class Display:
    """Two-line calculator display using Entry widgets.
    Entry reliably repaints on macOS; Label+StringVar does not."""

    def __init__(self, parent):
        wrap = tk.Frame(parent, bg=CARD,
                        highlightbackground=BORDER, highlightthickness=1)
        wrap.pack(fill="x", pady=(0, 8))

        # ── expr line (small, top) ──
        self._expr = tk.Entry(wrap, bg=CARD, fg=T3,
                              font=("Arial", 12),
                              relief="flat", bd=0,
                              highlightthickness=0,
                              insertwidth=0,
                              justify="right",
                              readonlybackground=CARD,
                              state="readonly")
        self._expr.pack(fill="x", padx=12, pady=(6, 0))

        # ── result line (large, bottom) ──
        self._res = tk.Entry(wrap, bg=CARD, fg=TEXT,
                             font=("Arial", 36, "bold"),
                             relief="flat", bd=0,
                             highlightthickness=0,
                             insertwidth=0,
                             justify="right",
                             readonlybackground=CARD,
                             state="readonly")
        self._res.pack(fill="x", padx=12, pady=(2, 10))
        self._set(self._res, "0")

        tk.Frame(wrap, bg=PURPLE, height=2).pack(fill="x")

    # ── internal write helper ──
    def _set(self, widget, text):
        widget.config(state="normal")
        widget.delete(0, "end")
        widget.insert(0, text)
        widget.config(state="readonly")
        widget.xview_moveto(1)        # scroll to right end

    def set_expr(self, text):   self._set(self._expr, text)
    def set_result(self, text): self._set(self._res,  text)
    def get_result(self):       return self._res.get()


# ═══════════════════════════════════════════════════
#  MAIN APP
# ═══════════════════════════════════════════════════
class App:
    def __init__(self, root):
        self.root   = root
        self.expr   = ""
        self.hist   = []
        self.mem    = 0.0
        self.angle  = tk.StringVar(value="DEG")
        self._input_entries = set()

        root.title("Scientific Calculator  ·  Error Analysis")
        root.configure(bg=BG)
        root.geometry("1200x860")
        root.minsize(1000, 700)

        self._ui()
        self._keys()
        root.lift()
        root.attributes("-topmost", True)
        root.after(300, lambda: root.attributes("-topmost", False))

    # ── layout ──────────────────────────────────────
    def _ui(self):
        self._header()
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=12, pady=(6, 12))
        left = tk.Frame(body, bg=BG); left.pack(side="left", fill="y")
        tk.Frame(body, bg=BORDER, width=1).pack(side="left", fill="y", padx=10)
        right = tk.Frame(body, bg=BG); right.pack(side="left", fill="both", expand=True)
        self._left(left)
        self._right(right)

    # ── header ──────────────────────────────────────
    def _header(self):
        bar = tk.Frame(self.root, bg="#130840", height=50)
        bar.pack(fill="x"); bar.pack_propagate(False)
        tk.Label(bar, text="⚛  Scientific Calculator with Error Analysis",
                 bg="#130840", fg=TEXT,
                 font=("Arial", 13, "bold")).pack(side="left", padx=16, pady=12)
        tk.Label(bar,
                 text="Divyansh Sharma  ·  Jiya Madan  ·  Kabir Bajaj   |   Numerical Methods",
                 bg="#130840", fg=T3,
                 font=("Arial", 9)).pack(side="right", padx=16)
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x")

    # ═══════════════════════════════════════════════
    #  LEFT : CALCULATOR
    # ═══════════════════════════════════════════════
    def _left(self, parent):
        # angle-mode bar
        top = tk.Frame(parent, bg=CARD2, padx=6, pady=5)
        top.pack(fill="x", pady=(0, 6))
        for m in ("DEG", "RAD", "GRAD"):
            tk.Radiobutton(top, text=m, variable=self.angle, value=m,
                           bg=CARD2, fg=T2, selectcolor=PURPLE,
                           activebackground=CARD2, activeforeground=TEXT,
                           font=("Arial", 9, "bold"), indicatoron=False,
                           relief="flat", padx=10, pady=4,
                           cursor="hand2").pack(side="left", padx=2)
        self.mem_lbl = tk.Label(top, text="M", bg=CARD2, fg=T3, font=("Arial", 9))
        self.mem_lbl.pack(side="right", padx=8)

        # display (Entry-based — always repaints on macOS)
        self.disp = Display(parent)

        # button grid
        self._grid(parent)

        # history
        self._hist_ui(parent)

    # ── button grid ──────────────────────────────────
    def _grid(self, parent):
        g = tk.Frame(parent, bg=BG, padx=2, pady=2)
        g.pack()
        P = 3
        sm = ("Arial", 9,  "bold")
        fn = ("Arial", 10, "bold")

        def b(txt, bg, hover, cmd, fg=TEXT, font=("Arial", 11, "bold"), cw=7, rh=2):
            return Btn(g, txt, bg, hover, cmd, fg=fg, font=font, cw=cw, rh=rh)

        def gd(w, r, c, cs=1):
            w.grid(row=r, column=c, columnspan=cs, padx=P, pady=P, sticky="nsew")

        # Row 0 – memory
        gd(b("MC",  FN, CLH, self._mc,   font=sm, cw=5), 0, 0)
        gd(b("MR",  FN, FNH, self._mr,   font=sm, cw=5), 0, 1)
        gd(b("M+",  FN, FNH, self._mp,   font=sm, cw=5), 0, 2)
        gd(b("M−",  FN, FNH, self._mm,   font=sm, cw=5), 0, 3)
        gd(b("MS",  FN, FNH, self._ms,   font=sm, cw=5), 0, 4)
        gd(b("⌫",  CLR, CLH, self._back, font=("Arial", 14, "bold"), cw=5), 0, 5)

        # Row 1 – trig
        gd(b("sin", FN, FNH, lambda: self._fn("sin"),  font=fn, cw=5), 1, 0)
        gd(b("cos", FN, FNH, lambda: self._fn("cos"),  font=fn, cw=5), 1, 1)
        gd(b("tan", FN, FNH, lambda: self._fn("tan"),  font=fn, cw=5), 1, 2)
        gd(b("√x",  FN, FNH, lambda: self._fn("sqrt"), font=fn, cw=5), 1, 3)
        gd(b("x²",  FN, FNH, lambda: self._put("**2"), font=fn, cw=5), 1, 4)
        gd(b("xⁿ",  OP, OPH, lambda: self._put("**"),  font=fn, cw=5), 1, 5)

        # Row 2 – inv trig + log
        gd(b("asin", FN, FNH, lambda: self._fn("asin"),  font=fn, cw=5), 2, 0)
        gd(b("acos", FN, FNH, lambda: self._fn("acos"),  font=fn, cw=5), 2, 1)
        gd(b("atan", FN, FNH, lambda: self._fn("atan"),  font=fn, cw=5), 2, 2)
        gd(b("log",  FN, FNH, lambda: self._fn("log10"), font=fn, cw=5), 2, 3)
        gd(b("ln",   FN, FNH, lambda: self._fn("ln"),    font=fn, cw=5), 2, 4)
        gd(b("eˣ",   FN, FNH, lambda: self._fn("exp"),   font=fn, cw=5), 2, 5)

        # Row 3 – constants + brackets
        gd(b("π",   FN, FNH, lambda: self._put(str(round(math.pi, 10))), font=fn, cw=5), 3, 0)
        gd(b("e",   FN, FNH, lambda: self._put(str(round(math.e,  10))), font=fn, cw=5), 3, 1)
        gd(b("(",   OP, OPH, lambda: self._put("("),   font=fn, cw=5), 3, 2)
        gd(b(")",   OP, OPH, lambda: self._put(")"),   font=fn, cw=5), 3, 3)
        gd(b("n!",  FN, FNH, lambda: self._fn("fact"), font=fn, cw=5), 3, 4)
        gd(b("1/x", FN, FNH, lambda: self._fn("inv"),  font=fn, cw=5), 3, 5)

        # Row 4 – 7 8 9
        gd(b("7",  NUM, NUH, lambda: self._put("7")),  4, 0)
        gd(b("8",  NUM, NUH, lambda: self._put("8")),  4, 1)
        gd(b("9",  NUM, NUH, lambda: self._put("9")),  4, 2)
        gd(b("÷",  OP,  OPH, lambda: self._put("/"), font=("Arial", 13, "bold"), cw=7), 4, 3)
        gd(b("x³", FN,  FNH, lambda: self._put("**3"), font=fn, cw=5), 4, 4)
        gd(b("AC", CLR, CLH, self._clear, cw=5), 4, 5)

        # Row 5 – 4 5 6
        gd(b("4",    NUM, NUH, lambda: self._put("4")),  5, 0)
        gd(b("5",    NUM, NUH, lambda: self._put("5")),  5, 1)
        gd(b("6",    NUM, NUH, lambda: self._put("6")),  5, 2)
        gd(b("×",    OP,  OPH, lambda: self._put("*"), font=("Arial", 13, "bold"), cw=7), 5, 3)
        gd(b("log₂", FN,  FNH, lambda: self._fn("log2"), font=fn, cw=5), 5, 4)
        gd(b("∛",    FN,  FNH, lambda: self._fn("cbrt"), font=fn, cw=5), 5, 5)

        # Row 6 – 1 2 3
        gd(b("1", NUM, NUH, lambda: self._put("1")), 6, 0)
        gd(b("2", NUM, NUH, lambda: self._put("2")), 6, 1)
        gd(b("3", NUM, NUH, lambda: self._put("3")), 6, 2)
        gd(b("−", OP,  OPH, lambda: self._put("-"), font=("Arial", 13, "bold"), cw=7), 6, 3)
        gd(b("±", OP,  OPH, self._neg, cw=5),  6, 4)
        gd(b("%", OP,  OPH, lambda: self._put("%"), cw=5), 6, 5)

        # Row 7 – 0 . + =
        gd(b("0", NUM, NUH, lambda: self._put("0"), cw=15, rh=2), 7, 0, cs=2)
        gd(b(".", NUM, NUH, lambda: self._put(".")), 7, 2)
        gd(b("+", OP,  OPH, lambda: self._put("+"), font=("Arial", 13, "bold"), cw=7), 7, 3)
        gd(b("=", EQ,  EQH, self._calc, font=("Arial", 13, "bold"), cw=15, rh=2), 7, 4, cs=2)

        for c in range(6): g.columnconfigure(c, weight=1)
        for r in range(8): g.rowconfigure(r, weight=1)

    # ── history ──────────────────────────────────────
    def _hist_ui(self, parent):
        hdr = tk.Frame(parent, bg=BG); hdr.pack(fill="x", pady=(8, 2))
        tk.Label(hdr, text="History", bg=BG, fg=T2,
                 font=("Arial", 10, "bold")).pack(side="left")
        tk.Button(hdr, text="Clear", bg=BG, fg=T3,
                  font=("Arial", 9), relief="flat", bd=0, cursor="hand2",
                  command=lambda: (self.hist.clear(),
                                   self.hist_lb.delete(0, "end"))).pack(side="right")
        frm = tk.Frame(parent, bg=CARD,
                       highlightbackground=BORDER, highlightthickness=1)
        frm.pack(fill="x")
        self.hist_lb = tk.Listbox(frm, bg=CARD, fg=T2,
                                  font=("Courier", 9),
                                  selectbackground=PURPLE, selectforeground=TEXT,
                                  relief="flat", bd=0, highlightthickness=0, height=4)
        self.hist_lb.pack(fill="x", padx=4, pady=4)
        self.hist_lb.bind("<<ListboxSelect>>", self._recall)

    def _recall(self, _=None):
        s = self.hist_lb.curselection()
        if not s: return
        self.expr = self.hist_lb.get(s[0]).split(" =")[0].strip()
        self.disp.set_expr(self.expr)
        self._live()

    # ═══════════════════════════════════════════════
    #  RIGHT : ERROR ANALYSIS
    # ═══════════════════════════════════════════════
    def _right(self, parent):
        nb = ttk.Notebook(parent); nb.pack(fill="both", expand=True)
        s  = ttk.Style(); s.theme_use("clam")
        s.configure("TNotebook", background=BG, borderwidth=0)
        s.configure("TNotebook.Tab", background=CARD, foreground=T3,
                    padding=[14, 7], font=("Arial", 10, "bold"), borderwidth=0)
        s.map("TNotebook.Tab",
              background=[("selected", PURPLE)], foreground=[("selected", TEXT)])
        for title, fn in [
            ("  📐 Basic Errors",  self._t_basic),
            ("  📈 Propagation",   self._t_prop),
            ("  🔢 Taylor",        self._t_taylor),
            ("  📊 Sig Figs",      self._t_sigfig),
            ("  🔬 Machine ε",     self._t_machine),
            ("  📋 Report",        self._t_report),
        ]:
            f = tk.Frame(nb, bg=BG, padx=16, pady=12)
            nb.add(f, text=title); fn(f)

    # ── shared helpers ───────────────────────────────
    def _sec(self, p, t):
        tk.Label(p, text=t, bg=BG, fg=TEXT,
                 font=("Arial", 13, "bold")).pack(anchor="w", pady=(0, 10))

    def _fld(self, p, lbl, key, store, def_=""):
        r = tk.Frame(p, bg=BG); r.pack(fill="x", pady=3)
        tk.Label(r, text=lbl, bg=BG, fg=T2, font=("Arial", 10),
                 width=22, anchor="w").pack(side="left")
        e = tk.Entry(r, bg=CARD2, fg=TEXT, font=("Courier", 11),
                     insertbackground=TEXT, relief="flat", bd=0,
                     highlightthickness=1, highlightcolor=PURPLE,
                     highlightbackground=BORDER, width=20)
        e.pack(side="left", ipady=5, padx=(4, 0))
        if def_: e.insert(0, def_)
        self._input_entries.add(e)
        store[key] = e; return e

    def _rrow(self, p, var, opts):
        r = tk.Frame(p, bg=CARD2, padx=6, pady=6); r.pack(fill="x", pady=(0, 8))
        for t, v in opts:
            tk.Radiobutton(r, text=t, variable=var, value=v,
                           bg=CARD2, fg=T2, selectcolor=PURPLE,
                           activebackground=CARD2, activeforeground=TEXT,
                           font=("Arial", 9), cursor="hand2").pack(side="left", padx=6)

    def _abtn(self, p, t, cmd):
        Btn(p, t, PURPLE, PL, cmd, fg=TEXT,
            font=("Arial", 10, "bold"), cw=22, rh=2).pack(pady=(10, 4), anchor="w")

    def _box(self, p, h=10):
        f = tk.Frame(p, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        f.pack(fill="both", expand=True, pady=(6, 0))
        t = tk.Text(f, bg=CARD, fg=GREEN, font=("Courier", 10),
                    relief="flat", height=h, state="disabled",
                    wrap="word", bd=0, highlightthickness=0,
                    padx=10, pady=8, selectbackground=PURPLE)
        t.tag_configure("k", foreground=CYAN)
        t.tag_configure("v", foreground=GREEN)
        t.tag_configure("d", foreground=T3)
        t.pack(side="left", fill="both", expand=True)
        sb = tk.Scrollbar(f, command=t.yview, bg=CARD,
                          troughcolor=CARD, relief="flat", width=8)
        sb.pack(side="right", fill="y"); t.configure(yscrollcommand=sb.set)
        return t

    def _wr(self, w, text):
        w.config(state="normal"); w.delete("1.0", "end")
        for line in text.split("\n"):
            s = line.strip()
            if s.startswith(("═", "─")): w.insert("end", line + "\n", "d")
            elif ":" in line:
                k, _, v = line.partition(":")
                w.insert("end", k + ":", "k"); w.insert("end", v + "\n", "v")
            else: w.insert("end", line + "\n")
        w.config(state="disabled")

    # ── Tab 1: Basic ─────────────────────────────────
    def _t_basic(self, p):
        self._sec(p, "Basic Error Calculations"); self._e1 = {}
        self._fld(p, "True Value",     "tv", self._e1)
        self._fld(p, "Approx Value",   "av", self._e1)
        self._fld(p, "Decimal Places", "dp", self._e1, "5")
        self._abtn(p, "   Calculate Errors   ", self._run_basic)
        self._b_out = self._box(p, 11)

    def _run_basic(self):
        try:
            tv = float(self._e1["tv"].get()); av = float(self._e1["av"].get())
            dp = int(self._e1["dp"].get() or "5")
        except ValueError: messagebox.showerror("Input", "Enter valid numbers."); return
        ae  = Calc.absolute(tv, av)
        re  = Calc.relative(tv, av)
        pe  = Calc.percent(tv, av)
        ro  = Calc.roundoff(av, dp)
        te  = Calc.trunc(av, dp)
        acc = int(-math.log10(re)) if re > 0 else "∞"
        self._wr(self._b_out, "\n".join([
            "═══════════════════════════════════",
            f"  True Value        : {tv}",
            f"  Approx Value      : {av}",
            f"  Decimal Places    : {dp}",
            "───────────────────────────────────",
            f"  Absolute Error    : {ae:.8e}",
            f"  Relative Error    : {re:.8e}",
            f"  Percentage Error  : {pe:.6f} %",
            f"  Round-off Error   : {ro:.8e}",
            f"  Truncation Error  : {te:.8e}",
            "───────────────────────────────────",
            f"  Accurate Digits   : {acc}",
            "═══════════════════════════════════",
        ])); self._log(f"Basic AE={ae:.4e} RE={re:.4e} PE={pe:.4f}%")

    # ── Tab 2: Propagation ────────────────────────────
    def _t_prop(self, p):
        self._sec(p, "Error Propagation"); self._pop = tk.StringVar(value="add")
        self._rrow(p, self._pop, [("Addition", "add"), ("Subtraction", "sub"),
                                   ("Multiply", "mul"), ("Divide", "div")])
        self._ep = {}
        self._fld(p, "Value a",           "a",  self._ep)
        self._fld(p, "Absolute Error Δa", "da", self._ep)
        self._fld(p, "Value b",           "b",  self._ep)
        self._fld(p, "Absolute Error Δb", "db", self._ep)
        self._abtn(p, "   Propagate Error   ", self._run_prop)
        self._p_out = self._box(p, 11)

    def _run_prop(self):
        try:
            a  = float(self._ep["a"].get());  da = float(self._ep["da"].get())
            b  = float(self._ep["b"].get());  db = float(self._ep["db"].get())
        except ValueError: messagebox.showerror("Input", "Enter valid numbers."); return
        op = self._pop.get()
        if   op == "add": res = a+b; df = Calc.prop_add(da, db);      sym = "+"
        elif op == "sub": res = a-b; df = Calc.prop_add(da, db);      sym = "−"
        elif op == "mul": res = a*b; df = Calc.prop_mul(a, b, da, db); sym = "×"
        else: res = a/b if b else float('inf'); df = Calc.prop_div(a, b, da, db); sym = "÷"
        rel = df / abs(res) if res else float('inf')
        self._wr(self._p_out, "\n".join([
            "═══════════════════════════════════",
            f"  Operation    : {a}  {sym}  {b}",
            f"  Result       : {res:.8g}",
            "───────────────────────────────────",
            f"  Delta a      : +/-{da}",
            f"  Delta b      : +/-{db}",
            f"  Prop Error   : +/-{df:.6e}",
            f"  Range        : [{res-df:.6g} , {res+df:.6g}]",
            f"  Relative Err : {rel:.4e}",
            "───────────────────────────────────",
            "  Method       : Quadrature (RSS) Law",
            "═══════════════════════════════════",
        ]))

    # ── Tab 3: Taylor ─────────────────────────────────
    def _t_taylor(self, p):
        self._sec(p, "Taylor Series Truncation Error"); self._tfn = tk.StringVar(value="sin")
        self._rrow(p, self._tfn, [("sin(x)", "sin"), ("cos(x)", "cos"), ("exp(x)", "exp")])
        self._et = {}
        self._fld(p, "x (radians)",      "x",     self._et)
        self._fld(p, "Max terms (1-20)", "terms", self._et, "8")
        self._abtn(p, "   Compute Error   ", self._run_taylor)
        self._ta_out = self._box(p, 14)

    def _run_taylor(self):
        try:
            x = float(self._et["x"].get()); n = int(self._et["terms"].get())
            if n < 1 or n > 20: raise ValueError
        except ValueError: messagebox.showerror("Input", "x=float; terms=1-20."); return
        fn = self._tfn.get(); exact, _, _ = Calc.taylor(fn, x, n)
        lines = ["════════════════════════════════════════",
                 f"  Function : {fn}(x)    x = {x}",
                 f"  Exact    : {exact:.12f}",
                 "────────────────────────────────────────",
                 f"  {'Terms':>5}   {'Approximate':>18}   {'Error':>14}",
                 "────────────────────────────────────────"]
        for t in range(1, n+1):
            _, ap, err = Calc.taylor(fn, x, t)
            lines.append(f"  {t:>5}   {ap:>18.8f}   {err:>14.6e}")
        lines.append("════════════════════════════════════════")
        self._wr(self._ta_out, "\n".join(lines))

    # ── Tab 4: Sig Figs ───────────────────────────────
    def _t_sigfig(self, p):
        self._sec(p, "Significant Figures & Rounding"); self._esf = {}
        self._fld(p, "Value",               "v", self._esf)
        self._fld(p, "Significant Figures", "n", self._esf, "4")
        self._abtn(p, "   Analyse   ", self._run_sigfig)
        self._sf_out = self._box(p, 13)

    def _run_sigfig(self):
        try:
            v = float(self._esf["v"].get()); n = int(self._esf["n"].get())
            if n < 1: raise ValueError
        except ValueError: messagebox.showerror("Input", "float + sig figs≥1."); return
        rv = Calc.sigfig(v, n); ae = abs(v - rv); re = ae/abs(v) if v else 0
        lines = ["═══════════════════════════════════",
                 f"  Original Value : {v}", f"  Sig Figures    : {n}",
                 "───────────────────────────────────",
                 f"  Rounded Value  : {rv}", f"  Absolute Error : {ae:.6e}",
                 f"  Relative Error : {re:.6e}", f"  Percentage Err : {re*100:.4f} %",
                 "───────────────────────────────────", "  Rounding Table:",
                 "───────────────────────────────────"]
        for dp in range(1, 8):
            rv2 = round(v, dp); e = abs(v - rv2)
            lines.append(f"  dp={dp}  ->  {rv2:<18} err={e:.2e}")
        lines.append("═══════════════════════════════════")
        self._wr(self._sf_out, "\n".join(lines))

    # ── Tab 5: Machine ε ──────────────────────────────
    def _t_machine(self, p):
        self._sec(p, "Machine Epsilon & Floating Point")
        eps = Calc.meps()
        rows = [("Computed epsilon (float64)", f"{eps:.4e}"),
                ("IEEE 754 eps (float64)",     f"{2.220446049250313e-16:.4e}"),
                ("IEEE 754 eps (float32)",     f"{1.1920929e-07:.4e}"),
                ("IEEE 754 eps (float16)",     f"{9.765625e-04:.4e}"),
                ("Max float64",                f"{1.7976931348623157e+308:.4e}"),
                ("Min positive float64",       f"{5e-324:.4e}")]
        info = tk.Frame(p, bg=CARD2, highlightbackground=BORDER, highlightthickness=1)
        info.pack(fill="x", pady=(0, 10))
        for k, v in rows:
            r = tk.Frame(info, bg=CARD2); r.pack(fill="x", padx=10, pady=2)
            tk.Label(r, text=k, bg=CARD2, fg=T2, font=("Arial", 9),
                     width=28, anchor="w").pack(side="left")
            tk.Label(r, text=v, bg=CARD2, fg=CYAN, font=("Courier", 9)).pack(side="left")
        tk.Label(p, text="Catastrophic Cancellation Demo",
                 bg=BG, fg=T2, font=("Arial", 10, "bold")).pack(anchor="w", pady=(6, 4))
        self._em = {}
        self._fld(p, "a",        "a", self._em, "1.0")
        self._fld(p, "b (tiny)", "b", self._em, "1e-16")
        self._abtn(p, "   Analyse Cancellation   ", self._run_machine)
        self._m_out = self._box(p, 8)

    def _run_machine(self):
        try: a = float(self._em["a"].get()); b = float(self._em["b"].get())
        except ValueError: messagebox.showerror("Input", "Enter valid floats."); return
        eps = Calc.meps(); result = a+b; actual = result-a; loss = abs(actual-b)
        self._wr(self._m_out, "\n".join([
            "═══════════════════════════════════",
            f"  a                : {a}", f"  b                : {b}",
            f"  a + b            : {result}", f"  (a+b) - a        : {actual}",
            f"  Expected b       : {b}", f"  Information lost : {loss:.4e}",
            f"  Loss / epsilon   : {loss/eps if eps else 0:.2f} x eps",
            "═══════════════════════════════════"]))

    # ── Tab 6: Report ─────────────────────────────────
    def _t_report(self, p):
        self._rlines = []
        self._sec(p, "Session Report")
        tk.Label(p, text="All computations are auto-logged here.",
                 bg=BG, fg=T3, font=("Arial", 9)).pack(anchor="w", pady=(0, 8))
        row = tk.Frame(p, bg=BG); row.pack(fill="x", pady=(0, 6))
        Btn(row, "  Clear  ",      CLR, CLH, self._clear_report,
            font=("Arial", 9, "bold"), cw=10, rh=1).pack(side="left", padx=(0, 6))
        Btn(row, "  Export .txt  ", FN,  FNH, self._export,
            fg=CYAN, font=("Arial", 9, "bold"), cw=14, rh=1).pack(side="left")
        self._rep = self._box(p, 20)
        self._log("Session started — compute errors using the tabs.")

    def _log(self, line):
        if not hasattr(self, "_rep"): return
        if not hasattr(self, "_rlines"): self._rlines = []
        self._rlines.append(line)
        self._rep.config(state="normal")
        self._rep.insert("end", f"  •  {line}\n", "v")
        self._rep.see("end"); self._rep.config(state="disabled")

    def _clear_report(self):
        self._rep.config(state="normal"); self._rep.delete("1.0", "end")
        self._rep.config(state="disabled"); self._rlines.clear()

    def _export(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt",
               filetypes=[("Text", "*.txt"), ("All", "*.*")])
        if not path: return
        with open(path, "w") as f:
            f.write("Scientific Calculator — Error Analysis Report\n")
            f.write("Authors: Divyansh Sharma · Jiya Madan · Kabir Bajaj\n\n")
            for ln in self._rlines: f.write(f"• {ln}\n")
        messagebox.showinfo("Exported", f"Saved:\n{path}")

    # ═══════════════════════════════════════════════
    #  CALCULATOR LOGIC
    # ═══════════════════════════════════════════════
    def _put(self, ch):
        self.expr += ch
        self.disp.set_expr(self.expr)
        self._live()

    def _fn(self, name):
        self.expr += name + "("
        self.disp.set_expr(self.expr)

    def _clear(self):
        self.expr = ""
        self.disp.set_expr("")
        self.disp.set_result("0")

    def _back(self):
        self.expr = self.expr[:-1]
        self.disp.set_expr(self.expr)
        self._live()

    def _neg(self):
        if self.expr:
            self.expr = f"-({self.expr})"
            self.disp.set_expr(self.expr)

    # memory
    def _ms(self):
        try:
            self.mem = float(self.disp.get_result())
            self.mem_lbl.config(text=f"M:{self.mem:.4g}", fg=CYAN)
        except: pass

    def _mr(self): self._put(str(self.mem))
    def _mc(self): self.mem = 0.0; self.mem_lbl.config(text="M", fg=T3)

    def _mp(self):
        try:
            self.mem += float(self.disp.get_result())
            self.mem_lbl.config(text=f"M:{self.mem:.4g}", fg=CYAN)
        except: pass

    def _mm(self):
        try:
            self.mem -= float(self.disp.get_result())
            self.mem_lbl.config(text=f"M:{self.mem:.4g}", fg=CYAN)
        except: pass

    def _live(self):
        """Live-evaluate and update result display."""
        try:
            r = Calc.evaluate(self.expr, self.angle.get())
            self.disp.set_result(f"{r:.6g}" if isinstance(r, float) else str(r))
        except:
            pass

    def _calc(self):
        if not self.expr: return
        try:
            result = Calc.evaluate(self.expr, self.angle.get())
            disp   = f"{result:.10g}" if isinstance(result, float) else str(result)
            entry  = f"{self.expr}  =  {disp}"
            self.hist.insert(0, entry)
            if len(self.hist) > 30: self.hist.pop()
            self.hist_lb.delete(0, "end")
            for it in self.hist: self.hist_lb.insert("end", it)
            self.disp.set_result(disp)
            self.disp.set_expr(self.expr + " =")
            self.expr = disp
            self._log(f"= {disp}   [{self.expr}]")
        except Exception as ex:
            self.disp.set_result("Error")
            self.disp.set_expr(str(ex)[:50])

    def _focus_in_entry(self):
        return self.root.focus_get() in self._input_entries

    def _keys(self):
        def on_key(e):
            if self._focus_in_entry(): return
            ks = e.keysym
            if ks in ("Return", "KP_Enter"): self._calc(); return "break"
            if ks == "BackSpace":            self._back(); return "break"
            if ks == "Escape":               self._clear(); return "break"
            c = e.char
            if c and c in "0123456789.+-*/()%":
                self._put(c); return "break"
        self.root.bind_all("<KeyPress>", on_key)


# ═══════════════════════════════════════════════════
def main():
    root = tk.Tk()
    root.resizable(True, True)
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
