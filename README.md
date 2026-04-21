<div align="center">

# 🔬 Scientific Calculator · Error Analysis

[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![HTML5](https://img.shields.io/badge/HTML5-Semantic-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-Glassmorphism-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen?style=for-the-badge)](.)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**A full-featured Scientific Calculator with a 6-module Error Analysis suite — built as a premium, zero-dependency web app.**  
*Numerical Methods · Application Software Project · Chandigarh University*

[🚀 Live Demo](#-how-to-run) · [📊 Features](#%EF%B8%8F-features) · [📚 Formulas](#-key-formulas) · [👤 Author](#-author)

</div>

---

## 📌 Overview

This project combines a fully-featured **Scientific Calculator** with a comprehensive **Error Analysis** toolkit into a single, elegant web interface. Built with zero external dependencies, it runs directly in your browser with a glassmorphism dark-theme UI and smooth animations.

> **What makes this different?** Most calculators stop at arithmetic. This one teaches you *why* your answers can be wrong — through interactive error propagation, Taylor series truncation visualization, and IEEE 754 machine epsilon exploration.

---

## 🚀 How to Run

```bash
# Option 1 — Open directly in browser (simplest)
open index.html

# Option 2 — Local development server
python -m http.server 8000
# Then visit: http://localhost:8000
```

No npm, no Node.js, no build step — works instantly on any machine.

---

## 🖥️ Features

### 🔢 Scientific Calculator (Left Panel)

| Category | Functions |
|---|---|
| **Trigonometry** | `sin`, `cos`, `tan`, `asin`, `acos`, `atan` |
| **Logarithms** | `log₁₀`, `log₂`, `ln` |
| **Powers & Roots** | `x²`, `x³`, `xⁿ`, `√`, `∛`, `eˣ` |
| **Constants** | `π`, `e` |
| **Special** | `n!`, `1/x`, `±`, `%` |
| **Memory** | `MC`, `MR`, `MS`, `M+`, `M−` |
| **Angle Modes** | DEG / RAD / GRAD |
| **Keyboard** | `Enter` (=), `Backspace` (⌫), `Escape` (AC) |

> 💡 **History Panel**: Every calculation is logged and can be recalled with a single click.

---

### 📊 Error Analysis Module (Right Panel — 6 Tabs)

| # | Tab | What it does |
|---|---|---|
| 1 | 📐 **Basic Errors** | Absolute, Relative, Percentage, Round-off, Truncation errors from true & approximate values |
| 2 | 📈 **Propagation** | RSS quadrature law for `a+b`, `a−b`, `a×b`, `a÷b` with uncertainties |
| 3 | 🔢 **Taylor Series** | Truncation error for `sin(x)`, `cos(x)`, `eˣ` — visualized term by term |
| 4 | 📊 **Sig Figures** | Rounding analysis + absolute error at each decimal precision level |
| 5 | 🔬 **Machine ε** | IEEE 754 float64 limits + catastrophic cancellation demonstration |
| 6 | 📋 **Report** | Auto-logged session history, exportable as `.txt` |

---

## 📚 Key Formulas

### Absolute Error
$$E_{abs} = |True Value - Approximate Value|$$

### Relative Error
$$E_{rel} = \frac{|True Value - Approximate Value|}{|True Value|}$$

### Percentage Error
$$E_{pct} = E_{rel} \times 100\%$$

### Error Propagation — Quadrature (RSS) Law

For `f = a ± b`:
```
ΔF = √(Δa² + Δb²)
```
For `f = a × b` or `f = a / b`:
```
ΔF/F = √((Δa/a)² + (Δb/b)²)
```

### Taylor Series Truncation Error (sin x, after n terms)
```
R_n(x) = |sin(x) − Σₖ₌₀ⁿ⁻¹ [(-1)ᵏ × x^(2k+1)] / (2k+1)!|
```

### Machine Epsilon (IEEE 754 float64)
```
ε ≈ 2.22 × 10⁻¹⁶
```

---

## 📁 File Structure

```
Scientific-Calculator-with-Error-Analysis/
├── index.html          ← App entry point & HTML structure
├── style.css           ← Premium glassmorphism dark-theme stylesheet
├── app.js              ← Calculator engine + all 6 error analysis modules
├── requirements.txt    ← Python reference libs (numpy, scipy)
└── README.md           ← This file
```

---

## 🛠️ Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Structure | HTML5 (semantic) | Accessibility & SEO |
| Styling | Vanilla CSS — Glassmorphism, Dark theme | Zero bloat, full control |
| Logic | JavaScript ES6+ | No build tools needed |
| Typography | Google Fonts — Inter, JetBrains Mono | Clean & readable |

---

## 🎯 Learning Outcomes

By using this tool, you will understand:

- How **floating-point arithmetic** introduces errors in every computation
- How errors **propagate** through multi-step calculations
- Why **Taylor series truncation** matters in numerical approximations
- The concept of **machine epsilon** and IEEE 754 standard limitations
- The difference between **absolute**, **relative**, and **percentage** errors

---

## 👤 Author

<div align="center">

**Divyansh Sharma**  
BTech CSE · Chandigarh University

[![GitHub](https://img.shields.io/badge/GitHub-Divyansh5070-181717?style=for-the-badge&logo=github)](https://github.com/Divyansh5070)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Divyansh%20Sharma-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/divyansh-sharma-12a52028a)

</div>

---

<div align="center">

*Submitted for: Numerical Methods — Application Software Project*  
*Chandigarh University · 2026*

</div>
