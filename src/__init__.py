"""
中国A股指数投资组合回测系统

Portfolio Backtesting System for Chinese A-share Market Indices
"""

__version__ = "0.1.0"
__author__ = "Portfolio Backtest System"

from .data_collector import DataCollector
from .data_loader import DataLoader
from .portfolio_config import PortfolioConfig

__all__ = [
    'DataCollector',
    'DataLoader',
    'PortfolioConfig',
]