# 🌊 Module: Stochastic Processes

This directory contains a curated collection of laboratory works centered on the mathematical modeling of stochastic processes. The material emphasizes the progression from foundational concepts to their implementation in discrete-time frameworks.

## 🧪 Lab Index

<table>
  <thead>
    <tr>
      <th>Lab #</th>
      <th>Title</th>
      <th>Description</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>01</td>
      <td><a href="./Stochastic-Rate-Bond-Pricing/"><strong>Stochastic Rate Bond Pricing</strong></a></td>
      <td>Interactive Binomial Lattice for ZCB, Forwards, Futures, and American Options.</td>
      <td>✅ Complete</td>
    </tr>
  </tbody>
</table>

## 🏛️ Featured Project: Stochastic Rate Bond Pricing

This application is a full-stack financial pricing engine built to visualize how interest rate volatility impacts the valuation of debt instruments and derivatives.

### 🚀 How to Run

This project is "Zero-Config." The included scripts handle the creation of a Python Virtual Environment (.venv) and the installation of all necessary libraries.

**For Windows**:
1) Open the project folder.
2) Double-click run.bat.

**For Linux (Arch/Ubuntu/Debian) & macOS**:
```
chmod +x run.sh
./run.sh
```

### 📂 Directory Structure

The project follows a modular architecture that separates the mathematical engine from the web interface. This design ensures that the pricing logic remains independent and testable.

```
Stochastic-Rate-Bond-Pricing/
├── src/
│   ├── main_page.py       # Streamlit UI and state management
│   └── engine/
│       └── calculator.py  # The CalculationModel class (Core logic)
├── requirements.txt       # Project dependencies (Streamlit, NumPy)
├── run.bat                # One-click launcher for Windows
└── run.sh                 # One-click launcher for Linux and macOS
```

### 💻 Technical Implementation &amp; Stack

- **Python 3.10+**: Core logic and scripting.

- **Streamlit**: Used for the frontend UI and session state management.

- **NumPy**: Highly optimized for efficient calculations.

- **Pandas**: Utilized for real-time styling and rendering of the lattice dataframes.

### 🧠 Core Mathematical Logic

This project implements a discrete-time Short-Rate Binomial Model to analyze the valuation of Zero-Coupon Bonds (ZCB) and their derivatives. The model transitions from a stochastic interest rate lattice to the recursive pricing of fixed-income instruments, forwards, futures, and American options.

#### 1. The Short-Rate Lattice Architecture

The model assumes the short rate follows a binomial process over $n$ periods. Given a volatility $\sigma$ and time horizon $T$, the tree is governed by:

* **Up/Down Factors**:  
  $u = \exp(\sigma \sqrt{T / n})$ and $d = 1 / u$

* **State Evolution**:  
  At any node $(i, j)$, the interest rate is calculated as:
  $$r_{i,j} = r_0 \cdot u^j \cdot d^{i-j}$$

* **Risk-Neutral Probabilities**:  
  Transitions are determined by:
  $$p = \frac{\exp(r_0 T / n) - d}{u - d}$$
  and $q = 1 - p$

#### 2. Zero-Coupon Bond (ZCB) Valuation
The ZCB is priced using **Backward Induction**. Starting from maturity $T$ (where the bond equals its nominal value of 100%), the price at any preceding node is the discounted expected value of its future nodes:
$$P_{i,j} = \frac{p \cdot P_{i+1, j+1} + q \cdot P_{i, j+1}}{1 + r_{i,j}}$$

#### 3. Linear Derivative Pricing: Forwards vs. Futures
The model highlights the divergence between Forward and Futures prices under stochastic rates:

* **Forward Price ($F_t$):** Calculated as a ratio of present values, representing the price that prevents arbitrage at time $t$:
    $$F_t = \frac{ZCB_{Maturity}}{ZCB_t}$$
* **Futures Price:** Unlike forwards, futures are priced as **martingales**. The value at each node is the simple expected value of the next period's futures price, without local discounting:
    $$Futures_{i,j} = p \cdot Futures_{i+1, j+1} + q \cdot Futures_{i, j+1}$$

#### 4. Nonlinear Derivatives: American Options
The model values American Call options on ZCB futures. At every node, the engine evaluates the **Early Exercise Condition**, choosing the maximum between the intrinsic value and the continuation value:

$$V_{i,j} = \max(Spot_{i,j} - Strike, \text{Continuation Value})$$

### 📝 Key Insights

- **Forward–Futures Divergence**: The model demonstrates that stochastic interest rates can cause forward and futures prices to decouple, reflecting the impact of daily futures settlement and martingale pricing.

- **Lattice Sensitivity**: The implementation illustrates how interest-rate volatility, $\sigma$, scales the up and down factors $(u, d)$, thereby increasing the time value of options on the ZCB10.

- **Numerical Efficiency**: Using a 10-period binomial tree, the engine provides an efficient discrete approximation for pricing path-dependent derivatives.

