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

### 📝 Key Insights

