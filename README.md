A Python library for pricing vanilla financial products, built from scratch as a learning project in quantitative finance.

## What this project does

This library provides tools to price the most common financial instruments used in derivatives markets and fixed income:

- **Vanilla options** using the Black-Scholes model
- **Option sensitivities** (the Greeks: Delta, Gamma, Vega, Theta, Rho)
- **European and American options** using the binomial tree model (Cox-Ross-Rubinstein)
- **Zero-coupon bonds** and **coupon-bearing bonds** with yield and duration calculations

Each product is implemented as a Python class with clearly documented methods. Jupyter notebooks demonstrate the models with visualizations and numerical examples.

-----

## Project structure

```
pyfinance-pricer/
│
├── pyfinance/                  ← main package
│   ├── options/
│   │   ├── black_scholes.py    ← Black-Scholes model for European options
│   │   ├── binomial.py         ← CRR binomial tree (European & American)
│   │   └── greeks.py           ← Delta, Gamma, Vega, Theta, Rho
│   ├── bonds/
│   │   ├── zero_coupon.py      ← Zero-coupon bond pricing
│   │   └── coupon_bond.py      ← Coupon bond: price, YTM, duration, convexity
│   └── utils/
│       └── stats.py            ← Shared statistical helpers
│
├── notebooks/
│   ├── 01_black_scholes.ipynb  ← Black-Scholes demo and visualizations
│   ├── 02_greeks.ipynb         ← Greeks profiles across spot prices
│   └── 03_bonds.ipynb          ← Bond pricing and yield curves
│
├── tests/
│   └── test_black_scholes.py   ← Unit tests with pytest
│
├── requirements.txt
└── README.md
```

-----

## Installation

**Clone the repository:**

```bash
git clone https://github.com/YOURUSERNAME/pyfinance-pricer.git
cd pyfinance-pricer
```

**Install dependencies:**

```bash
pip install -r requirements.txt
```

Dependencies used: `numpy`, `pandas`, `scipy`, `matplotlib`

-----

## Quick start

```python
from pyfinance.options.black_scholes import BlackScholesModel

# Define an option
option = BlackScholesModel(S=100, K=105, T=1, r=0.05, sigma=0.2)

# Price the option
print(option.price_call())   # European call price
print(option.price_put())    # European put price
```

```python
from pyfinance.bonds.coupon_bond import CouponBond

# Define a bond
bond = CouponBond(face=1000, coupon_rate=0.05, maturity=5, r=0.04)

print(bond.price())             # Fair value
print(bond.yield_to_maturity()) # YTM
print(bond.duration())          # Macaulay duration
```

-----

## Models implemented

### Black-Scholes (1973)

The Black-Scholes model gives a closed-form formula for pricing European calls and puts. It assumes the underlying asset follows a geometric Brownian motion with constant volatility.

**Inputs:** spot price S, strike K, time to maturity T (in years), risk-free rate r, volatility σ

**Outputs:** call price, put price, and verification via put-call parity

### Greeks

Sensitivities of the option price to changes in market parameters:

|Greek|Measures sensitivity to   |
|-----|--------------------------|
|Delta|Change in underlying price|
|Gamma|Change in Delta           |
|Vega |Change in volatility      |
|Theta|Passage of time           |
|Rho  |Change in risk-free rate  |

### Binomial Tree (Cox-Ross-Rubinstein, 1979)

The CRR model builds a discrete price tree over N time steps. Unlike Black-Scholes, it can handle **American options** (early exercise). As N increases, the binomial price converges to the Black-Scholes price.

### Bond pricing

Zero-coupon bonds and coupon bonds are priced using discounted cash flow analysis. The yield to maturity is solved numerically using `scipy.optimize`. Duration and convexity are computed analytically.

-----

## Notebooks

The `notebooks/` folder contains interactive demonstrations:

- **01_black_scholes.ipynb** — plots option price as a function of spot, strike, and volatility
- **02_greeks.ipynb** — visualizes Greek profiles across different market conditions
- **03_bonds.ipynb** — shows yield curves, duration sensitivity, and price/yield relationship

-----

## Running the tests

```bash
pytest tests/
```

Tests verify that model outputs match known reference values (cross-checked against external pricing tools).

-----

## Roadmap

-  Black-Scholes model
-  Greeks (analytical)
-  Binomial tree (European + American)
-  Zero-coupon bond
-  Coupon bond with YTM
-  Monte Carlo simulation for path-dependent options
-  Implied volatility solver
-  Yield curve bootstrapping

-----

## About

This project was built as a self-study exercise in quantitative finance and Python software design. The goal was to go beyond using existing libraries and actually implement the mathematical models from scratch, with clean object-oriented code and documented notebooks.

**Skills demonstrated:** object-oriented Python, numerical methods (scipy), financial mathematics, data visualization, unit testing, project structuring.

-----

## References

- Black, F. & Scholes, M. (1973). *The Pricing of Options and Corporate Liabilities*. Journal of Political Economy.
- Cox, J., Ross, S. & Rubinstein, M. (1979). *Option Pricing: A Simplified Approach*. Journal of Financial Economics.
- Hull, J. (2018). *Options, Futures, and Other Derivatives*. Pearson. (reference textbook)
