# Monte Carlo Simulation for Option Pricing Playground

## 1. What Is This?

This interactive application demonstrates how Monte Carlo simulation can be used to price European options. It uses random sampling and geometric Brownian motion to generate possible future stock price paths and estimates the option price by averaging the discounted payoffs.

**Key Concepts:**

- **Monte Carlo Simulation:**  
  Uses random sampling to simulate many potential future outcomes for the underlying asset. In this playground, the asset’s terminal price \(S_T\) is modeled as:
  
  $$
  S_T = S \cdot \exp\Bigl(\Bigl(r - \tfrac{1}{2}\sigma^2\Bigr)T + \sigma\sqrt{T}\,Z\Bigr), \quad Z \sim \mathcal{N}(0,1).
  $$

- **Option Pricing:**  
  The estimated option price is computed by discounting the average payoff:
  
  $$
  \text{Option Price} = e^{-rT}\;\mathbb{E}\Bigl[\max\bigl(S_T - K,\, 0\bigr)\Bigr],
  $$
  
  where the payoff is \(\max(S_T-K,\,0)\) for a call and \(\max(K-S_T,\,0)\) for a put.

Use the interactive controls to adjust parameters such as stock price, strike price, time to maturity, risk-free rate, volatility, and the number of simulation paths. Visual outputs include a histogram of terminal stock prices and sample full-path simulations.

## 2. Setting Up a Local Development Environment

### 2.1 Prerequisites

1. **A computer** (Windows, macOS, or Linux).
2. **Python 3.9 or higher** (Python 3.12 preferred, but anything 3.9+ works).  
   - If you don’t have Python, download it from [python.org/downloads](https://www.python.org/downloads/).
3. **Visual Studio Code (VS Code)**
   - Download from [code.visualstudio.com](https://code.visualstudio.com/)
4. **Git** (optional, but recommended for cloning the repository).  
   - Install from [git-scm.com/downloads](https://git-scm.com/downloads)

### 2.2 Downloading the Project

#### Option 1: Cloning via Git (Recommended)

1. Open **Terminal** (macOS/Linux) or **Command Prompt/PowerShell** (Windows).
2. Navigate to the folder where you want to download the project:
   ```bash
   cd Documents
