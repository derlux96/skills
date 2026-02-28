# AMIP Architecture

## System Overview

```
┌─────────────────────────────────────────────────┐
│              ADAPTIVE SCANNER                    │
│  (Volatility-based frequency control)           │
└──────────────────┬──────────────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    ▼              ▼              ▼
┌────────┐  ┌───────────┐  ┌───────────┐
│FinnHub │  │  Signal   │  │  Insider  │
│  API   │  │ Generator │  │  Tracker  │
└────────┘  └───────────┘  └───────────┘
```

## Components

### 1. AdaptiveScanner

Main orchestrator that:
- Fetches quotes from FinnHub
- Calculates volatility from candles
- Determines scan frequency
- Generates signals
- Tracks insider transactions

### 2. SignalGenerator

Generates trading signals based on:
- Price change percentage
- Configurable thresholds
- Emoji indicators

### 3. FinnHubClient

API wrapper for:
- Stock quotes
- Stock candles (OHLCV)
- Insider transactions
- Company profiles

## Data Flow

```
1. Scanner loop starts
2. For each symbol:
   a. Fetch quote (current price, change)
   b. Fetch candles (20 periods)
   c. Calculate volatility (std dev)
   d. Fetch insider transactions
   e. Generate signal
   f. Check for price alerts
3. Determine overall scan interval (max volatility)
4. Wait for next scan
5. Repeat
```

## Volatility Calculation

```python
def calculate_volatility(candles):
    """Calculate price volatility from candles"""
    closes = [c['close'] for c in candles]
    returns = [(closes[i] - closes[i-1]) / closes[i-1]
               for i in range(1, len(closes))]
    return np.std(returns) * 100  # As percentage
```

## Adaptive Frequency Algorithm

```python
def get_scan_interval(volatility):
    if volatility < 0.5:
        return 300  # 5 min - Low volatility
    elif volatility < 1.5:
        return 120  # 2 min - Medium volatility
    else:
        return 30   # 30 sec - High volatility
```

## Signal Generation

| Change % | Signal |
|----------|--------|
| > +3% | STRONG BUY 🟢 |
| +2% to +3% | BUY 🟡 |
| -2% to +2% | NEUTRAL ⚪ |
| -3% to -2% | SELL 🟠 |
| < -3% | STRONG SELL 🔴 |

## Configuration

```python
SCAN_TARGETS = ["AAPL", "TSLA", "NVDA", ...]
VOLATILITY_THRESHOLDS = {"low": 0.5, "medium": 1.5}
SCAN_INTERVALS = {"low": 300, "medium": 120, "high": 30}
SIGNAL_THRESHOLDS = {"strong_buy": 3.0, ...}
```

## Future Enhancements

1. **Multi-Source Data** - Yahoo Finance, Alpha Vantage
2. **ML-Based Signals** - XGBoost classifier
3. **Risk Management** - Kelly Criterion, position sizing
4. **Alert Channels** - Telegram, Discord
5. **Backtesting** - Historical signal validation
