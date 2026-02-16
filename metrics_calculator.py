"""
Performance metrics calculation module.
Computes risk and return metrics by regime.
"""

import pandas as pd
import numpy as np
from scipy import stats


class PerformanceMetrics:
    """
    Calculate performance metrics for each regime.
    """
    
    @staticmethod
    def calculate(returns, regimes, risk_free_rate=0.0):
        """
        Calculate comprehensive performance metrics by regime.
        
        Parameters
        ----------
        returns : pd.DataFrame
            Daily log returns for multiple assets
        regimes : pd.Series
            Regime labels aligned with returns index
        risk_free_rate : float, default=0.0
            Annualized risk-free rate
            
        Returns
        -------
        pd.DataFrame
            Performance metrics for each regime and asset
        """
        results = []
        
        # Get unique regimes including full sample
        regime_labels = regimes.unique().tolist()
        regime_labels.append('Full Sample')
        
        for asset in returns.columns:
            for regime in regime_labels:
                if regime == 'Full Sample':
                    regime_returns = returns[asset]
                else:
                    regime_returns = returns.loc[regimes == regime, asset]
                
                metrics = PerformanceMetrics._calculate_single(
                    regime_returns, 
                    asset, 
                    regime,
                    risk_free_rate
                )
                results.append(metrics)
        
        return pd.DataFrame(results)
    
    @staticmethod
    def _calculate_single(returns, asset, regime, risk_free_rate):
        """
        Calculate metrics for a single regime-asset combination.
        """
        # Basic stats
        n_days = len(returns)
        total_return = np.exp(returns.sum()) - 1
        ann_return = (1 + total_return) ** (252 / n_days) - 1
        ann_vol = returns.std() * np.sqrt(252)
        
        # Risk-adjusted returns
        sharpe = (ann_return - risk_free_rate) / ann_vol if ann_vol > 0 else 0
        
        # Downside metrics
        negative_returns = returns[returns < 0]
        if len(negative_returns) > 0:
            downside_dev = negative_returns.std() * np.sqrt(252)
            sortino = (ann_return - risk_free_rate) / downside_dev
        else:
            sortino = 0
        
        # Maximum drawdown
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()
        
        # Value at Risk
        var_95 = np.percentile(returns, 5)
        cvar_95 = returns[returns <= var_95].mean()
        
        # Skewness and kurtosis
        skew = stats.skew(returns)
        kurt = stats.kurtosis(returns)
        
        return {
            'Asset': asset,
            'Regime': regime,
            'Days': n_days,
            'Total_Return': f"{total_return * 100:.2f}%",
            'Ann_Return': f"{ann_return * 100:.2f}%",
            'Ann_Vol': f"{ann_vol * 100:.2f}%",
            'Sharpe': round(sharpe, 3),
            'Sortino': round(sortino, 3),
            'Max_Drawdown': f"{max_drawdown * 100:.2f}%",
            'VaR_95': f"{var_95 * 100:.2f}%",
            'CVaR_95': f"{cvar_95 * 100:.2f}%",
            'Skewness': round(skew, 3),
            'Kurtosis': round(kurt, 3)
        }
