# 🔬 Numerical Methods Project

> **Scientific Calculator + Error Analysis + Root Finding Calculator**  
> *Submitted for: Numerical Methods — Application Software Project*  
> **Team:** Divyansh Sharma · Jiya Madan · Kabir Bajaj

---

## 📌 Overview

This project is a **full-featured Numerical Methods toolkit** split into two major components:

| Component | Description |
|---|---|
| 🖩 **Scientific Calculator + Error Analysis** | Web-based calculator with 6 error analysis modules |
| 🔍 **Root Finding Calculator** | Google Colab interactive GUI with 6 root-finding methods |

---

## 🚀 How to Run

### Web App (Scientific Calculator + Error Analysis)

Simply open `index.html` in any modern browser — no installation needed.

```bash
# If you prefer a local server:
python -m http.server 8000
# Then open http://localhost:8000
```

### Root Finding Calculator (Google Colab)

1. Open [Google Colab](https://colab.research.google.com/)
2. Create a new notebook and paste the contents of `root_finding_colab.py`
3. Run the cell — an interactive GUI will appear inline below the cell
4. Enter your equation `f(x)`, choose a method, set parameters, and click **▶ Solve**

### Python Desktop App (Tkinter)

```bash
# Install dependencies
pip install -r requirements.txt

# Run Scientific Calculator
python calculator.py

# Run standalone root-finding app
python root_app.py
```

---

## 🖥️ Features

### 🔢 Scientific Calculator (Web — `index.html` + `app.js`)

- **Full Scientific Functions:** sin, cos, tan, asin, acos, atan, log, ln, eˣ, √, ∛, xⁿ
- **Memory Operations:** MC, MR, MS, M+, M−
- **Angle Modes:** DEG / RAD / GRAD
- **Keyboard Support:** Enter (=), Backspace (⌫), Escape (AC)
- **Calculation History** with one-click recall

### 📊 Error Analysis (6 Tabs)

| Tab | Description |
|---|---|
| 📐 **Basic Errors** | Absolute, Relative, Percentage, Round-off, Truncation errors |
| 📈 **Propagation** | Quadrature (RSS) law for ±, ×, ÷ operations |
| 🔢 **Taylor Series** | Truncation error for sin(x), cos(x), eˣ — term by term |
| 📊 **Sig Figures** | Rounding analysis across decimal levels |
| 🔬 **Machine Epsilon** | IEEE 754 limits + catastrophic cancellation demo |
| 📋 **Session Report** | Auto-logged calculations, exportable as `.txt` |

### 🔍 Root Finding Calculator (`root_finding_colab.py`)

| Method | Type | Convergence |
|---|---|---|
| ✂️ **Bisection** | Bracketing | Linear (guaranteed) |
| 📐 **False Position (Regula Falsi)** | Bracketing | Superlinear |
| 🚀 **Newton–Raphson** | Open | Quadratic |
| 🔗 **Secant** | Open | Superlinear (no derivative) |
| 🔄 **Fixed-Point Iteration** | Open | Linear (depends on g(x)) |
| 🌀 **Muller's Method** | Open | Order ≈ 1.84 (complex roots) |

**Outputs for each solve:**
- ✅ Root value `x*` with 12 significant figures
- Full iteration table (step-by-step)
- Convergence plot (error vs. iteration)
- Method comparison guide

---

## 📚 Numerical Methods Concepts

### Absolute Error
```
E_abs = |True Value − Approximate Value|
```

### Relative Error
```
E_rel = |True Value − Approximate Value| / |True Value|
```

### Percentage Error
```
E_pct = E_rel × 100%
```

### Error Propagation — Quadrature (RSS) Law
For `f = a ± b`:
```
ΔF = √(Δa² + Δb²)
```
For `f = a × b` or `f = a / b`:
```
ΔF/F = √((Δa/a)² + (Δb/b)²)
```

### Taylor Series Truncation Error
Error after `n` terms of sin(x):
```
R_n(x) = |sin(x) − Σ ((-1)^k × x^(2k+1)) / (2k+1)!|
```

### Newton–Raphson Iteration
```
x_(n+1) = x_n − f(x_n) / f'(x_n)
```

### Bisection Method
```
c = (a + b) / 2
```
Update: if `f(a)·f(c) < 0` → `b = c`, else `a = c`

### Machine Epsilon (IEEE 754)
```
ε ≈ 2.22 × 10⁻¹⁶   (float64)
```

---

## 📁 File Structure

```
NM project/
│
├── index.html              ← Web app entry point (Scientific Calc + Error Analysis)
├── style.css               ← Premium dark-theme stylesheet
├── app.js                  ← Calculator logic & error analysis engine (JavaScript)
│
├── root_finding_colab.py   ← Root Finding Calculator (Google Colab GUI)
├── root_app.py             ← Standalone root-finding app (Python/Tkinter)
│
├── calculator.py           ← Scientific Calculator (Python/Tkinter desktop)
├── colab_calculator.py     ← Scientific Calculator adapted for Google Colab
│
├── requirements.txt        ← Python dependencies (numpy, scipy)
└── README.md               ← This file
```

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Web Frontend | HTML5, Vanilla CSS, JavaScript (ES6+) |
| Python Backend | Python 3.8+ |
| Desktop GUI | Tkinter (built-in) |
| Scientific Computing | NumPy, SciPy |
| Colab GUI | IPython `display` + HTML/CSS/JS inline |
| Typography | Google Fonts — Inter, JetBrains Mono |

---

## 👥 Team

| Name | Role |
|---|---|
| Divyansh Sharma | Lead Developer — Root Finding + Web UI |
| Jiya Madan | Error Analysis Module + Testing |
| Kabir Bajaj | Python Backend + Report Generation |

---

*Submitted for: Numerical Methods — Application Software Project*
