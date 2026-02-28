---
name: pyonvista
description: "Search German OnVista derivatives (turbos, options, warrants) via pyonvista API. Use when: (1) finding WKNs for Trade Republic derivatives, (2) searching turbos/options for a ticker, (3) need German derivative data (OnVista), (4) user mentions 'pyonvista', 'OnVista', 'WKN search', 'Turbo Long/Short', or 'derivative finder'. WARNING: Grauzone API - rate-limited, research use only."
---

# PyOnVista - German Derivative Search

Search OnVista for derivatives (turbos, options, warrants) with WKNs for Trade Republic.

## Quick Start

```bash
# Search derivatives
python3 ~/.openclaw/skills/pyonvista/scripts/pyonvista_test.py <TICKER> [TYPE]

# Examples
python3 ~/.openclaw/skills/pyonvista/scripts/pyonvista_test.py AAPL "Turbo Long"
python3 ~/.openclaw/skills/pyonvista/scripts/pyonvista_test.py VLO Call
python3 ~/.openclaw/skills/pyonvista/scripts/pyonvista_test.py PLTR "Turbo Short"
```

## Output

Returns list with:
- Name, ISIN, WKN (for Trade Republic)
- Type (DERIVATIVE)
- Price (if available)

## Derivative Types

| Type | Description |
|------|-------------|
| `Turbo Long` | Bullish turbo |
| `Turbo Short` | Bearish turbo |
| `Call` | Call optionsschein |
| `Put` | Put optionsschein |
| `Faktor` | Factor certificate |

## Rate Limiting

- **6 seconds** between requests
- **Max 10 requests/minute**
- Script has built-in rate-limiting
- **403 Error**: IP blocked, wait 24h

## Legal Warning

- **Grauzone**: Non-public API
- **Research/Testing only**
- Could violate OnVista ToS
- Use at own risk

## Alternatives

| Method | Legal | Speed | Derivatives |
|--------|-------|-------|-------------|
| pyonvista | Grauzone | Fast | Direct |
| Web Search | OK | Fast | Manual |
| Browser | OK | Slow | Direct |

## Integration Workflow

```bash
# 1. Get stock data
python3 tools/yahoo_finance.py AAPL

# 2. Search derivatives
python3 ~/.openclaw/skills/pyonvista/scripts/pyonvista_test.py AAPL "Turbo Long"

# 3. Copy WKNs to Trade Republic
# 4. Execute trade
```

## Troubleshooting

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError` | `pip install pyonvista --break-system-packages` |
| `403 Forbidden` | Rate-limited, wait 24h or use VPN |
| `No instruments found` | Check ticker or try different type |

## Files

- `scripts/pyonvista_test.py` - Main search script
- `references/security-audit.md` - Security analysis
