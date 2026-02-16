# Methodology Documentation

## 1. Data Collection

We analyze daily adjusted close prices for four tickers:
- **NVDA**: NVIDIA Corporation (Technology/Growth)
- **JPM**: JPMorgan Chase & Co. (Financial)
- **PG**: Procter & Gamble Co. (Consumer Staples/Defensive)
- **SPY**: SPDR S&P 500 ETF (Market proxy)

**Period**: January 2019 - December 2023 (5 years)

## 2. Return Calculation

Daily log returns are calculated as:

Log returns are preferred for their statistical properties (time-additivity, approximate normality).

## 3. Regime Detection

### Methodology
- Calculate 30-day rolling standard deviation of SPY returns
- Classify days with volatility above/below median as High/Low volatility regimes
- 30-day window balances responsiveness with stability

### Rationale
SPY is used as market proxy because:
- Broad market exposure
- High liquidity
- Standard benchmark in CAPM

## 4. Performance Metrics

### Risk-Adjusted Returns
- **Sharpe Ratio**: (R_p - R_f) / σ_p
- **Sortino Ratio**: (R_p - R_f) / σ_d (downside deviation only)

### Tail Risk Metrics
- **VaR (95%)**: 5th percentile of returns (historical method)
- **CVaR (95%)**: Average of returns below VaR

### Drawdown Analysis
- Maximum drawdown calculated as peak-to-trough decline

## 5. Beta Stability Analysis

### CAPM Framework

### Analysis
- Beta calculated separately for each regime
- Statistical significance tested via t-statistics
- R² measures how well market explains asset returns

### Interpretation
- **Beta increase in High-Vol** → Correlation convergence (reduced diversification)
- **Beta decrease in High-Vol** → Flight to quality/hedging behavior

## 6. Statistical Testing

- **Kurtosis**: Measures tail fatness (normal distribution = 3)
- **Jarque-Bera test**: Tests normality of returns
- **t-tests**: Compare metrics across regimes

## 7. Limitations

1. **Single volatility threshold**: Using median splits data arbitrarily
2. **Look-ahead bias**: Rolling calculations use future data
3. **Regime persistence**: Quick regime changes may not be captured
4. **Market proxy**: SPY may not represent true market portfolio

## 8. Future Enhancements

- Multiple volatility thresholds (low/medium/high)
- Markov-switching models for regime detection
- Out-of-sample backtesting
- Machine learning for regime prediction
- Transaction cost analysis for regime-switching strategies

