# 🔬 Scientific Calculator · Error Analysis

> **Numerical Methods — Application Software Project**  
> **Author:** Divyansh Sharma

---

## 📌 Overview

A full-featured **Scientific Calculator** with a dedicated **Error Analysis** module built as a premium web application. No installation required — runs entirely in the browser.

---

## 🚀 How to Run

```bash
# Option 1 — Open directly
open index.html

# Option 2 — Local dev server
python -m http.server 8000
# then visit http://localhost:8000
```

---

## 🖥️ Features

### 🔢 Scientific Calculator (Left Panel)

- All trigonometric functions: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`
- Logarithms: `log₁₀`, `log₂`, `ln`
- Powers & roots: `x²`, `x³`, `xⁿ`, `√`, `∛`, `eˣ`
- Constants: `π`, `e`
- Special: `n!`, `1/x`, `±`, `%`
- Memory operations: `MC`, `MR`, `MS`, `M+`, `M−`
- Angle modes: **DEG / RAD / GRAD**
- Keyboard support: `Enter` (=), `Backspace` (⌫), `Escape` (AC)
- Calculation history with one-click recall

### 📊 Error Analysis (Right Panel — 6 Tabs)

| Tab | What it does |
|---|---|
| 📐 **Basic Errors** | Absolute, Relative, Percentage, Round-off, Truncation — from true & approximate values |
| 📈 **Propagation** | RSS quadrature law for `a+b`, `a−b`, `a×b`, `a÷b` with uncertainties |
| 🔢 **Taylor Series** | Truncation error for `sin(x)`, `cos(x)`, `eˣ` — term by term |
| 📊 **Sig Figures** | Rounding analysis + absolute error at each decimal level |
| 🔬 **Machine ε** | IEEE 754 float64 limits + catastrophic cancellation demo |
| 📋 **Report** | Auto-logged session history, exportable as `.txt` |

---

## 📚 Key Formulas

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

### Taylor Series Truncation Error (sin x after n terms)
```
R_n(x) = |sin(x) − Σ ((-1)^k × x^(2k+1)) / (2k+1)!|    k = 0…n-1
```

### Machine Epsilon (IEEE 754 float64)
```
ε ≈ 2.22 × 10⁻¹⁶
```

---

## 📁 File Structure

```
NM project/
├── index.html          ← App entry point
├── style.css           ← Premium dark-theme stylesheet
├── app.js              ← Calculator + error analysis logic
├── requirements.txt    ← (numpy, scipy — for reference)
└── README.md           ← This file
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Structure | HTML5 (semantic) |
| Styling | Vanilla CSS — glassmorphism, dark theme |
| Logic | JavaScript (ES6+) — zero dependencies |
| Typography | Google Fonts — Inter, JetBrains Mono |

---

## 👥 Team

| Name | Contribution |
|---|---|
| **Divyansh Sharma** | UI/UX, JavaScript engine, Error Analysis |

---

*Submitted for: Numerical Methods — Application Software Project*
