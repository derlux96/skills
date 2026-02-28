"""
AMIP Scanner Configuration
"""

import os

# FinnHub API Key
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "d645mohr01ql6dj29o2gd645mohr01ql6dj29o30")

# Scan Configuration
DEFAULT_SCAN_INTERVAL = 120  # seconds (2 minutes)

# Adaptive Scan Intervals (based on volatility)
SCAN_INTERVALS = {
    "low": 300,      # 5 min for low volatility (<0.5%)
    "medium": 120,    # 2 min for medium volatility (0.5% - 1.5%)
    "high": 30       # 30 sec for high volatility (>1.5%)
}

# Volatility Thresholds
VOLATILITY_THRESHOLDS = {
    "low": 0.5,      # <0.5%
    "medium": 1.5     # <1.5%
}

# Scan Targets (Symbols to monitor)
SCAN_TARGETS = ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL", "AMZN", "META", "AMD"]

# Signal Thresholds
SIGNAL_THRESHOLDS = {
    "oversold": -2.0,     # <-2% change
    "overbought": 2.0,    # >+2% change
    "strong_buy": 3.0,     # >+3% change
    "strong_sell": -3.0     # <-3% change
}

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "scanner.log"

# Data Storage
DATA_DIR = "./data"
CACHE_DIR = "./cache"
