"""
Beta stability analysis module.
Calculates CAPM beta coefficients across different regimes.
"""

import pandas as pd
import numpy as np
from scipy import stats


class BetaAnalyzer:
    """
    Analyze beta stability across market regimes.
    """
    
    @staticmethod
    def calculate(returns, market_col='SPY', regimes=None):
        """
        Calculate beta coefficients for all assets.
        
        Parameters
        ----------
        returns : pd.DataFrame
            Daily log returns
        market_col : str, default='SPY'
            Column name for market returns
        regimes : pd.Series, optional
            Regime labels
            
        Returns
        -------
        pd.DataFrame
            Beta coefficients by regime
        """
        results = []
        
        assets = [col for col in returns.columns if col != market_col]
        regime_labels = ['Full Sample']
        
        if regimes is not None:
            regime_labels.extend(regimes.unique().tolist())
        
        for asset in assets:
            for regime in regime_labels:
                if regime == 'Full Sample':
                    x = returns[market_col]
                    y = returns[asset]
                else:
                    mask = regimes == regime
                    x = returns.loc[mask, market_col]
                    y = returns.loc[mask, asset]
                
                # Remove any NaN values
                mask = ~(x.isna() | y.isna())
                x_clean = x[mask]
                y_clean = y[mask]
                
                if len(x_clean) < 2:
                    continue
                
                # Linear regression
                slope, intercept, r_value, p_value, std_err = stats.linregress(
                    x_clean, y_clean
                )
                
                results.append({
                    'Asset': asset,
                    'Regime': regime,
                    'Beta': round(slope, 3),
                    'Alpha_bps': round(intercept * 252 * 10000, 2),  # Basis points annualized
                    'R_squared': round(r_value ** 2, 3),
                    'P_Value': f"{p_value:.2e}",
                    'Std_Error': round(std_err, 3),
                    'Observations': len(x_clean)
                })
        
        return pd.DataFrame(results)
    
    @staticmethod
    def get_beta_changes(beta_df):
        """
        Calculate beta changes between regimes.
        
        Parameters
        ----------
        beta_df : pd.DataFrame
            Beta coefficients by regime
            
        Returns
        -------
        pd.DataFrame
            Beta changes
        """
        changes = []
        
        for asset in beta_df['Asset'].unique():
            asset_data = beta_df[beta_df['Asset'] == asset]
            
            try:
                low_vol_beta = asset_data[asset_data['Regime'] == 'Low-Vol']['Beta'].values[0]
                high_vol_beta = asset_data[asset_data['Regime'] == 'High-Vol']['Beta'].values[0]
                
                change = high_vol_beta - low_vol_beta
                change_pct = (change / low_vol_beta) * 100
                
                changes.append({
                    'Asset': asset,
                    'Low_Vol_Beta': low_vol_beta,
                    'High_Vol_Beta': high_vol_beta,
                    'Beta_Change': round(change, 3),
                    'Beta_Change_pct': round(change_pct, 1)
                })
            except IndexError:
                continue
        
        return pd.DataFrame(changes)
