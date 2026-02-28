---
name: amip-scanner
description: "Adaptive Market Intelligence Platform scanner with volatility-based scan frequency. Use when: (1) monitoring multiple stocks adaptively, (2) need volatility-based scanning, (3) price alerts and signals, (4) insider transaction tracking, (5) user mentions 'adaptive scanning', 'volatility scanner', 'market scanner', or 'AMIP'. Adjusts scan rate based on market volatility (5min/2min/30sec)."
---

# AMIP Scanner - Adaptive Market Scanner

Volatility-based adaptive scanner that adjusts scan frequency based on market conditions.

## Quick Start

```bash
# Run scanner
cd ~/.openclaw/skills/amip-scanner/scripts
python3 scanner.py

# Or import module
from scanner import AdaptiveScanner
scanner = AdaptiveScanner()
results = scanner.scan_all()
```

## Adaptive Scanning

Scanner adjusts frequency based on volatility:

| Volatility | Scan Rate | Trigger |
|------------|-----------|---------|
| **LOW** | 5 min | < 0.5% |
| **MEDIUM** | 2 min | 0.5% - 1.5% |
| **HIGH** | 30 sec | > 1.5% |

## Features

- **Adaptive Frequency** - Faster scanning when volatility is high
- **Price Alerts** - Notifies when price changes >1% since last scan
- **Signal Generation** - BUY/SELL/NEUTRAL based on price change
- **Insider Tracking** - Monitors insider transactions
- **Multi-Symbol** - Scans multiple targets simultaneously

## Configuration

Edit `config.py`:

```python
# Scan targets
SCAN_TARGETS = ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL"]

# Volatility thresholds
VOLATILITY_THRESHOLDS = {
    "low": 0.5,      # <0.5% = 5min scan
    "medium": 1.5    # <1.5% = 2min scan
}

# Signal thresholds
SIGNAL_THRESHOLDS = {
    "strong_buy": 3.0,    # >+3%
    "buy": 2.0,           # >+2%
    "strong_sell": -3.0,  # <-3%
    "sell": -2.0          # <-2%
}
```

## Output Example

```
============================================================
📊 AAPL | Volatility: 0.82% (MEDIUM)
============================================================
💰 Current: $178.12
📈 Change: +1.23 (+0.69%)
📊 Range: $177.00 - $179.50
🎯 Signal: 🟡 BUY
============================================================

🚨 PRICE ALERT: +1.05% since last scan!

📊 Insider Transactions (3):
  📉 Cook Timothy (S): -200,000 shares on 2024-01-31
  📈 Williams Jeff (P): +50,000 shares on 2024-01-29
```

## Signal Generation

| Signal | Condition | Emoji |
|--------|-----------|-------|
| STRONG BUY | > +3% | 🟢 |
| BUY | +2% to +3% | 🟡 |
| NEUTRAL | -2% to +2% | ⚪ |
| SELL | -3% to -2% | 🟠 |
| STRONG SELL | < -3% | 🔴 |

## Usage Examples

### Single Scan

```python
from scanner import AdaptiveScanner

scanner = AdaptiveScanner()
result = scanner.scan_symbol("AAPL")

print(f"Price: ${result['quote']['current']}")
print(f"Signal: {result['signal']}")
print(f"Volatility: {result['volatility']}%")
```

### Continuous Scanning

```python
scanner = AdaptiveScanner()
scanner.run()  # Runs until Ctrl+C
```

### Custom Targets

```python
from config import SCAN_TARGETS

# Modify targets
SCAN_TARGETS = ["TSLA", "NVDA", "AMD", "PLTR"]

# Run
scanner = AdaptiveScanner()
scanner.run()
```

## Integration with TradePeter/Gordon

```python
# In tradepeter AGENTS.md or TOOLS.md
from amip_scanner import AdaptiveScanner

# Morning routine
scanner = AdaptiveScanner()
results = scanner.scan_all()

for result in results:
    if "STRONG" in result['signal']:
        send_telegram(f"🚨 {result['symbol']}: {result['signal']}")
```

## Files

- `scripts/scanner.py` - Main scanner engine
- `scripts/config.py` - Configuration
- `scripts/signals.py` - Signal generation
- `scripts/finnhub_client.py` - API client (local)
- `references/architecture.md` - System design

## Requirements

```
requests>=2.28.0
```

## Notes

- Uses FinnHub API (60 calls/min free tier)
- Logs to `scanner.log`
- Stores scan data in `./data/`
- Cache in `./cache/`
