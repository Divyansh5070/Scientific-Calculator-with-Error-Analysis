"""
Root Finding Calculator — Flask Web App
Authors: Divyansh Sharma · Jiya Madan · Kabir Bajaj

Run:  python root_app.py
Open: http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, jsonify
import math, cmath, os

app = Flask(__name__, template_folder="templates")

# ─────────────────────────────────────────────────
#  SAFE EXPRESSION EVALUATOR
# ─────────────────────────────────────────────────
MATH_ENV = {
    'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
    'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
    'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
    'exp': math.exp, 'log': math.log, 'log2': math.log2,
    'log10': math.log10, 'sqrt': math.sqrt, 'abs': abs,
    'ceil': math.ceil, 'floor': math.floor,
    'pi': math.pi, 'e': math.e,
}

def f(expr, x):
    env = dict(MATH_ENV); env['x'] = x
    return eval(expr, {"__builtins__": {}}, env)

def deriv(expr, x, h=1e-7):
    return (f(expr, x + h) - f(expr, x - h)) / (2 * h)

# ─────────────────────────────────────────────────
#  ROOT-FINDING METHODS
# ─────────────────────────────────────────────────

def bisection(expr, a, b, tol, max_iter):
    fa, fb = f(expr, a), f(expr, b)
    if fa * fb > 0:
        raise ValueError("f(a) and f(b) must have opposite signs.")
    rows, headers = [], ["Iter", "a", "b", "c", "f(c)", "|εa|"]
    c = a
    for i in range(1, max_iter + 1):
        fa = f(expr, a)
        c = (a + b) / 2.0
        fc = f(expr, c)
        ea = abs(b - a) / 2.0
        rows.append([i, round(a, 10), round(b, 10), round(c, 10), round(fc, 10), ea])
        if abs(fc) < tol or ea < tol:
            return c, rows, headers, None
        if fa * fc < 0:
            b = c
        else:
            a = c
    return c, rows, headers, "Max iterations reached."


def false_position(expr, a, b, tol, max_iter):
    fa, fb = f(expr, a), f(expr, b)
    if fa * fb > 0:
        raise ValueError("f(a) and f(b) must have opposite signs.")
    rows, headers = [], ["Iter", "a", "b", "c", "f(c)", "|εa|"]
    c_old = a
    for i in range(1, max_iter + 1):
        fa, fb = f(expr, a), f(expr, b)
        if abs(fb - fa) < 1e-15:
            break
        c = b - fb * (b - a) / (fb - fa)
        fc = f(expr, c)
        ea = abs(c - c_old)
        rows.append([i, round(a, 10), round(b, 10), round(c, 10), round(fc, 10), ea])
        if abs(fc) < tol or (i > 1 and ea < tol):
            return c, rows, headers, None
        if fa * fc < 0:
            b = c
        else:
            a = c
        c_old = c
    return c, rows, headers, "Max iterations reached."


def newton_raphson(expr, x0, tol, max_iter):
    rows, headers = [], ["Iter", "xn", "f(xn)", "f'(xn)", "xn+1", "|εa|"]
    x = x0
    for i in range(1, max_iter + 1):
        fx = f(expr, x)
        fpx = deriv(expr, x)
        if abs(fpx) < 1e-14:
            raise ValueError("Derivative too small — possible inflection point.")
        x_new = x - fx / fpx
        ea = abs(x_new - x)
        rows.append([i, round(x, 10), round(fx, 10), round(fpx, 10), round(x_new, 10), ea])
        if ea < tol and abs(fx) < tol:
            return x_new, rows, headers, None
        x = x_new
    return x, rows, headers, "Max iterations reached."


def secant(expr, x0, x1, tol, max_iter):
    rows, headers = [], ["Iter", "x0", "x1", "x2", "f(x2)", "|εa|"]
    for i in range(1, max_iter + 1):
        f0, f1 = f(expr, x0), f(expr, x1)
        if abs(f1 - f0) < 1e-14:
            raise ValueError("f(x1) ≈ f(x0) — near-zero denominator.")
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        ea = abs(x2 - x1)
        rows.append([i, round(x0, 10), round(x1, 10), round(x2, 10), round(f(expr, x2), 10), ea])
        if ea < tol:
            return x2, rows, headers, None
        x0, x1 = x1, x2
    return x1, rows, headers, "Max iterations reached."


def fixed_point(expr, g_expr, x0, tol, max_iter):
    rows, headers = [], ["Iter", "xn", "xn+1", "f(xn+1)", "|εa|"]
    x = x0
    for i in range(1, max_iter + 1):
        x_new = f(g_expr, x)
        ea = abs(x_new - x)
        fx_new = f(expr, x_new)
        rows.append([i, round(x, 10), round(x_new, 10), round(fx_new, 10), ea])
        if ea < tol:
            return x_new, rows, headers, None
        x = x_new
    return x, rows, headers, "Max iterations reached (check |g'(x)| < 1)."


def muller(expr, x0, x1, x2, tol, max_iter):
    rows, headers = [], ["Iter", "x0", "x1", "x2", "x3", "f(x2)", "|εa|"]
    for i in range(1, max_iter + 1):
        f0, f1, f2 = f(expr, x0), f(expr, x1), f(expr, x2)
        h1, h2 = x1 - x0, x2 - x1
        d1 = (f1 - f0) / h1 if h1 != 0 else 0
        d2 = (f2 - f1) / h2 if h2 != 0 else 0
        a = (d2 - d1) / (h2 + h1) if (h2 + h1) != 0 else 0
        b = a * h2 + d2
        c = f2
        disc = b**2 - 4 * a * c
        if disc < 0:
            sq = cmath.sqrt(complex(disc))
        else:
            sq = math.sqrt(disc)
        denom = (b + sq) if abs(b + sq) > abs(b - sq) else (b - sq)
        dx = -2 * c / denom if denom != 0 else 0
        x3 = x2 + dx
        ea = abs(dx)
        try:
            rows.append([i, round(x0, 8), round(x1, 8), round(x2, 8),
                         round(x3.real if isinstance(x3, complex) else x3, 8),
                         round(f2, 8), ea])
        except Exception:
            rows.append([i, x0, x1, x2, x3, f2, ea])
        if ea < tol:
            root = x3.real if isinstance(x3, complex) else x3
            return root, rows, headers, None
        x0, x1, x2 = x1, x2, (x3.real if isinstance(x3, complex) else x3)
    return x2, rows, headers, "Max iterations reached."


# ─────────────────────────────────────────────────
#  FLASK ROUTES
# ─────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/solve", methods=["POST"])
def solve():
    data = request.get_json()
    method  = data.get("method", "bisection")
    expr    = data.get("fx", "").strip()
    g_expr  = data.get("gx", "").strip()
    tol     = float(data.get("tol", 1e-7))
    max_it  = int(data.get("maxiter", 100))
    params  = data.get("params", {})

    if not expr:
        return jsonify({"error": "Please enter f(x)."}), 400

    # Sanitize expression — reject dangerous tokens
    banned = ["import", "open", "exec", "eval", "__", "os", "sys"]
    for b in banned:
        if b in expr or b in g_expr:
            return jsonify({"error": f"Disallowed token: '{b}'"}), 400

    try:
        if method == "bisection":
            root, rows, hdrs, warn = bisection(expr, float(params["a"]), float(params["b"]), tol, max_it)
        elif method == "false_position":
            root, rows, hdrs, warn = false_position(expr, float(params["a"]), float(params["b"]), tol, max_it)
        elif method == "newton":
            root, rows, hdrs, warn = newton_raphson(expr, float(params["x0"]), tol, max_it)
        elif method == "secant":
            root, rows, hdrs, warn = secant(expr, float(params["x0"]), float(params["x1"]), tol, max_it)
        elif method == "fixed_point":
            if not g_expr:
                return jsonify({"error": "Please enter g(x) for Fixed-Point method."}), 400
            root, rows, hdrs, warn = fixed_point(expr, g_expr, float(params["x0"]), tol, max_it)
        elif method == "muller":
            root, rows, hdrs, warn = muller(expr, float(params["x0"]), float(params["x1"]), float(params["x2"]), tol, max_it)
        else:
            return jsonify({"error": f"Unknown method: {method}"}), 400

        fx_root = None
        try:
            fx_root = f(expr, float(root))
        except Exception:
            fx_root = None

        ea_last = rows[-1][-1] if rows else None

        return jsonify({
            "success": warn is None,
            "root": float(root),
            "fx_root": fx_root,
            "iterations": len(rows),
            "ea_last": float(ea_last) if ea_last is not None else None,
            "warning": warn,
            "rows": rows,
            "headers": hdrs,
            "method": method,
        })

    except Exception as ex:
        return jsonify({"error": str(ex)}), 400


if __name__ == "__main__":
    print("=" * 55)
    print("  Root Finding Calculator — Flask Server")
    print("  Open http://127.0.0.1:5000 in your browser")
    print("=" * 55)
    app.run(debug=True, port=5000)
