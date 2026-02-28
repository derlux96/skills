# FinnHub API Endpoints Reference

## Base URL

```
https://api.finnhub.io/api/v1
```

## Authentication

Add `token=YOUR_API_KEY` as query parameter to all requests.

## Rate Limits

| Tier | Rate | Cost |
|------|------|------|
| Free | 60 calls/min | $0 |
| Starter | 300 calls/min | $29/mo |
| Pro | 600 calls/min | $79/mo |

---

## Stock Endpoints

### Quote

```
GET /quote?symbol=AAPL
```

Response:
```json
{
  "c": 178.12,      // Current price
  "d": 1.23,        // Change
  "dp": 0.69,       // Change percent
  "h": 179.50,      // High
  "l": 177.00,      // Low
  "o": 177.50,      // Open
  "pc": 176.89,     // Previous close
  "t": 1234567890   // Timestamp
}
```

### Company Profile

```
GET /stock/profile2?symbol=AAPL
```

Response:
```json
{
  "country": "US",
  "currency": "USD",
  "exchange": "NASDAQ",
  "ipo": "1980-12-12",
  "marketCapitalization": 2800000,
  "name": "Apple Inc",
  "phone": "14089961010",
  "shareOutstanding": 1553,
  "ticker": "AAPL",
  "weburl": "https://www.apple.com",
  "logo": "https://static...",
  "finnhubIndustry": "Technology"
}
```

### Stock Candles

```
GET /stock/candle?symbol=AAPL&resolution=D&count=100
```

Resolutions: `1`, `5`, `15`, `30`, `60`, `D`, `W`, `M`

### Company Peers

```
GET /stock/peers?symbol=AAPL
```

Response: `["MSFT", "GOOGL", "AMZN", "META"]`

---

## Insider Trading

### Transactions

```
GET /stock/insider-transactions?symbol=AAPL
```

Response:
```json
{
  "data": [
    {
      "name": "Cook Timothy Donald",
      "share": 0,
      "change": -200000,
      "transactionPrice": 174.99,
      "transactionCode": "S",
      "transactionDate": "2024-01-31"
    }
  ]
}
```

Transaction Codes:
- `P` = Open market purchase
- `S` = Open market sale
- `A` = Grant/award
- `M` = Option exercise

### Sentiment

```
GET /stock/insider-sentiment?symbol=AAPL
```

---

## News

### Company News

```
GET /company-news?symbol=AAPL&from=2024-01-01&to=2024-01-31
```

### Market News

```
GET /news?category=general
```

Categories: `general`, `forex`, `crypto`, `merger`

---

## Technical Indicators

```
GET /indicator?symbol=AAPL&resolution=D&indicator=rsi
```

Available Indicators:
- `sma` - Simple Moving Average
- `ema` - Exponential Moving Average
- `wma` - Weighted Moving Average
- `dema` - Double EMA
- `tema` - Triple EMA
- `rsi` - Relative Strength Index
- `macd` - Moving Average Convergence Divergence
- `bbands` - Bollinger Bands
- `stoch` - Stochastic Oscillator
- `adx` - Average Directional Index
- `williams` - Williams %R

---

## Earnings

```
GET /stock/earnings?symbol=AAPL
```

---

## Paid Tier Only (Not Available)

| Endpoint | Tier Required |
|----------|---------------|
| `/news-sentiment` | Pro |
| `/stock/recommendation` | Starter |
| `/stock/price-target` | Starter |
| `/stock/upgrades-downgrades` | Starter |
| `/scan/pattern` | Pro |
