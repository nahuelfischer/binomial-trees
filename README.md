# Binomial Tree Option Pricing (Streamlit)

This repository contains a Streamlit app that prices options using a Cox-Ross-Rubinstein binomial tree model. It includes interactive parameter inputs and plots of the stock tree and option value tree.

## 🚀 What’s included

- `binomial_trees.py`: Streamlit app for pricing call/put options under European and American styles.

## 🔍 Quantitative Finance Theory

### Binomial Tree Model (CRR)
- The model splits time to maturity into `N` steps with up and down moves.
- Up factor: `u = exp(sigma * sqrt(dt))`
- Down factor: `d = 1 / u`
- Risk-neutral probability: `q = (exp(r * dt) - d) / (u - d)`.
- Option price is computed by backward induction from terminal payoffs:
  - European: `V = exp(-r dt) * (q V_up + (1 - q) V_down)`.
  - American: `V = max(intrinsic, discounted continuation)` at each node.

### Why it works
- In a no-arbitrage market, the discounted expected payoff under the risk-neutral measure equals fair option price.
- As `N` grows, European binomial prices converge to Black-Scholes values.
- American option pricing works naturally through early-exercise decisions at each node.

## ▶️ Run the app (GitHub-friendly)

1. Create and activate a Python environment (recommended):
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Run Streamlit:
   ```bash
   streamlit run binomial_trees.py
   ```

3. Open the URL printed by Streamlit (typically `http://localhost:8501`).

## 🧪 Example usage

In the sidebar, choose:
- Option Type: `call` or `put`
- Option Style: `european` or `american`
- Stock Price `S0`, Strike `K`, Time `T`, Rate `r`, Volatility `sigma`, Steps `N`

Then click **Calculate Option Price**.

## ✅ Interpreting outputs

- `Option Price` displayed in the dashboard is the present value at the root node.
- The left plot shows the underlying stock-lattice.
- The right plot shows option values at each node.
- For American options, early-exercise is embedded by comparing intrinsic vs continuation values.

## 📚 Notes

- The model uses continuous compounding for discounting.
- For valid no-arbitrage inputs, ensure `d < exp(r dt) < u` (holds automatically with CRR and positive volatility).
- Use higher `N` for better accuracy, but note runtime and plot density increase.

---
