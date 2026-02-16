# regime-aware-quant-analysis
Regime-aware risk &amp; performance analysis: showing why average metrics fail in crashes — with GARCH forecasting, beta instability, and stress testing (NVDA/JPM/PG/SPY).

# Regime-Aware Quantitative Analysis

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📊 Overview

This project demonstrates advanced quantitative finance techniques by analyzing how stock performance and risk characteristics change across different market volatility regimes. Using SPY as a market proxy, we identify high and low volatility periods and analyze how individual stocks (NVDA, JPM, PG) behave differently under these conditions.

### Key Questions Addressed:
- How do Sharpe ratios change during high volatility periods?
- Is beta stable across different market regimes?
- Are traditional risk metrics (VaR, CVaR) underestimating risk during stress periods?
- Do defensive stocks (PG) maintain lower betas during market turbulence?

## 🎯 Key Findings

| Metric | Low-Vol Regime | High-Vol Regime | Insight |
|--------|----------------|-----------------|---------|
| **NVDA Sharpe** | 2.48 | 0.73 | 71% Sharpe reduction in stress |
| **JPM Sharpe** | 1.34 | 0.09 | Near-zero risk-adjusted returns in stress |
| **PG Beta Change** | 0.43 → 0.61 | +41% | Defensive stocks still increase correlation |
| **SPY VaR (95%)** | -1.23% | -2.71% | 2.2x tail risk in high volatility |

**Critical Insight**: Average metrics mask severe performance deterioration during stress periods - exactly when risk management matters most.

## 🛠️ Features

- **Volatility Regime Detection**: Identifies low/high volatility periods using rolling standard deviation
- **Comprehensive Performance Metrics**: Sharpe, Sortino, VaR, CVaR, Max Drawdown by regime
- **Beta Stability Analysis**: Tests CAPM assumption of stable beta across regimes
- **Interactive Visualizations**: Clear plots showing regime effects on returns and risk

## 📈 Sample Visualizations

![Regime Analysis](outputs/figures/regime_plot.png)
*Market regimes based on 30-day rolling volatility of SPY*

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/regime-aware-quant-analysis.git
cd regime-aware-quant-analysis

# Install required packages
pip install -r requirements.txt

# Run the Jupyter notebook
jupyter notebook notebooks/regime_dependent_risk_&_performance_attribution.ipynb
