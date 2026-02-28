---
name: finnhub
description: "FinnHub API client for real-time stock quotes, insider trading data, company news, and technical indicators. Use when: (1) fetching stock prices/quotes, (2) checking insider transactions, (3) getting company profiles/financials, (4) technical analysis (RSI, MACD, SMA), (5) market news, (6) user mentions 'finnhub', 'stock api', 'insider trading data', or 'real-time quotes'. Free tier: 60 calls/minute."
---

# FinnHub - Free Market Data API

Real-time stock quotes, insider trading, news, and technical indicators.

## Quick Start

```bash
# Test API
python3 ~/.openclaw/skills/finnhub/scripts/finnhub_client.py

# Import in Python
from pathlib import sys; sys.path.append("~/.openclaw/skills/finnhub/scripts")
from finnhub_client import FinnhubClient

client = FinnhubClient()
quote = client.get_stock_quote("AAPL")
```

## API Key

**Free Tier Key:** `d645mohr01ql6dj29o2gd645mohr01ql6dj29o30`
**Rate Limit:** 60 calls/minute
**Docs:** https://finnhub.io/docs/api

## Available Endpoints

### Stock Data

| Method | Description | Example |
|--------|-------------|---------|
| `get_stock_quote(symbol)` | Real-time price | `client.get_stock_quote("AAPL")` |
| `get_company_profile(symbol)` | Company info | `client.get_company_profile("TSLA")` |
| `get_stock_candles(symbol, res)` | OHLCV data | `client.get_stock_candles("AAPL", "D")` |
| `get_company_peers(symbol)` | Competitors | `client.get_company_peers("NVDA")` |
| `get_company_basic_financials(symbol)` | Financials | `client.get_company_basic_financials("AAPL")` |

### Insider Trading

| Method | Description | Example |
|--------|-------------|---------|
| `get_insider_transactions(symbol)` | Insider buys/sells | `client.get_insider_transactions("AAPL")` |
| `get_insider_sentiment(symbol)` | Insider sentiment | `client.get_insider_sentiment("AAPL")` |

### News

| Method | Description | Example |
|--------|-------------|---------|
| `get_company_news(symbol)` | Company news | `client.get_company_news("AAPL")` |
| `get_market_news(category)` | Market news | `client.get_market_news("general")` |

### Technical Indicators

| Method | Description | Example |
|--------|-------------|---------|
| `get_technical_indicators(symbol, res, indicator)` | RSI, MACD, SMA | `client.get_technical_indicators("AAPL", "D", "rsi")` |

**Available indicators:** `sma`, `ema`, `wma`, `dema`, `tema`, `williams`, `rsi`, `macd`, `rsi`, `bbands`, `stoch`, `adx`

### Earnings

| Method | Description | Example |
|--------|-------------|---------|
| `get_earnings_surprises(symbol)` | Earnings data | `client.get_earnings_surprises("AAPL")` |

## Usage Examples

### Get Stock Quote

```python
client = FinnhubClient()
quote = client.get_stock_quote("AAPL")

# Response:
# {
#   "c": 178.12,      # Current price
#   "d": 1.23,        # Change
#   "dp": 0.69,       # Change percent
#   "h": 179.50,      # High
#   "l": 177.00,      # Low
#   "o": 177.50,      # Open
#   "pc": 176.89,     # Previous close
#   "t": 1234567890   # Timestamp
# }

print(f"AAPL: ${quote['c']} ({quote['dp']}%)")
```

### Check Insider Trading

```python
transactions = client.get_insider_transactions("AAPL")

for tx in transactions[:5]:
    if tx['change'] > 0:
        print(f"🟢 BUY: {tx['name']} +{tx['change']} shares @ ${tx['transactionPrice']}")
    else:
        print(f"🔴 SELL: {tx['name']} {tx['change']} shares")
```

### Technical Analysis (RSI)

```python
indicators = client.get_technical_indicators("AAPL", "D", "rsi")
rsi = indicators['technicalAnalysis']['rsi']

if rsi < 30:
    print("🟢 OVERSOLD - Buy signal")
elif rsi > 70:
    print("🔴 OVERBOUGHT - Sell signal")
else:
    print(f"📊 RSI: {rsi} - Neutral")
```

### Market News

```python
# General market news
news = client.get_market_news("general")
for article in news[:3]:
    print(f"📰 {article['headline']}")

# Company-specific news
aapl_news = client.get_company_news("AAPL")
```

## Rate Limiting

- **60 calls/minute** (Free tier)
- Built-in session reuse
- No auth required for basic endpoints

## Not Available (Paid Tier)

- News sentiment
- Pattern recognition
- Social sentiment
- Recommendation trends

## Integration Examples

### With TradePeter

```python
# Morning scan
for symbol in ["AAPL", "TSLA", "NVDA"]:
    quote = client.get_stock_quote(symbol)
    insider = client.get_insider_transactions(symbol)
    print(f"{symbol}: ${quote['c']} | Insider txns: {len(insider)}")
```

### With Gordon

```python
# Technical scan
symbols = ["EURUSD", "GBPUSD", "USDJPY"]
for symbol in symbols:
    rsi = client.get_technical_indicators(symbol, "60", "rsi")
    print(f"{symbol} RSI: {rsi['technicalAnalysis']['rsi']}")
```

## Files

- `scripts/finnhub_client.py` - Main API client
- `references/endpoints.md` - Full endpoint reference
