"""
Volatility regime detection module.
Identifies high and low volatility periods based on rolling standard deviation.
"""

import pandas as pd
import numpy as np


class VolatilityRegimeDetector:
    """
    Detect market volatility regimes based on rolling standard deviation.
    
    Parameters
    ----------
    window : int, default=30
        Rolling window size for volatility calculation
    threshold : str, default='median'
        Method for threshold determination ('median' or 'mean')
    """
    
    def __init__(self, window=30, threshold='median'):
        self.window = window
        self.threshold = threshold
        self.volatility = None
        self.threshold_value = None
        
    def fit(self, returns):
        """
        Calculate rolling volatility and threshold.
        
        Parameters
        ----------
        returns : pd.Series
            Daily log returns
            
        Returns
        -------
        self
        """
        self.volatility = returns.rolling(window=self.window).std()
        
        if self.threshold == 'median':
            self.threshold_value = self.volatility.median()
        elif self.threshold == 'mean':
            self.threshold_value = self.volatility.mean()
        else:
            raise ValueError("threshold must be 'median' or 'mean'")
            
        return self
    
    def transform(self, returns):
        """
        Generate regime labels based on volatility.
        
        Parameters
        ----------
        returns : pd.Series
            Daily log returns
            
        Returns
        -------
        pd.Series
            Regime labels ('Low-Vol' or 'High-Vol')
        """
        if self.volatility is None:
            self.fit(returns)
            
        # Align returns with volatility index
        valid_idx = self.volatility.dropna().index
        returns_aligned = returns.loc[valid_idx]
        
        # Generate labels
        labels = pd.Series(index=valid_idx, dtype=str)
        labels[self.volatility.loc[valid_idx] <= self.threshold_value] = 'Low-Vol'
        labels[self.volatility.loc[valid_idx] > self.threshold_value] = 'High-Vol'
        
        return labels
    
    def fit_transform(self, returns):
        """
        Fit detector and generate regime labels.
        
        Parameters
        ----------
        returns : pd.Series
            Daily log returns
            
        Returns
        -------
        pd.Series
            Regime labels
        """
        self.fit(returns)
        return self.transform(returns)
    
    def get_regime_numeric(self, labels):
        """
        Convert regime labels to numeric values.
        
        Parameters
        ----------
        labels : pd.Series
            Regime labels
            
        Returns
        -------
        pd.Series
            Numeric regime values (0 for Low-Vol, 1 for High-Vol)
        """
        numeric = pd.Series(index=labels.index, dtype=int)
        numeric[labels == 'Low-Vol'] = 0
        numeric[labels == 'High-Vol'] = 1
        return numeric
