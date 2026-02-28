"""
Signal Generation for AMIP Scanner
"""

from typing import Dict, Any, Optional
from config import SIGNAL_THRESHOLDS


def generate_price_signal(quote: Dict[str, Any]) -> str:
    """Generate signal based on price change"""
    change_percent = quote.get('change_percent', 0.0)

    if change_percent >= SIGNAL_THRESHOLDS['strong_buy']:
        return "🟢 STRONG BUY"
    elif change_percent >= SIGNAL_THRESHOLDS['overbought']:
        return "🟡 BUY"
    elif change_percent <= SIGNAL_THRESHOLDS['strong_sell']:
        return "🔴 STRONG SELL"
    elif change_percent <= SIGNAL_THRESHOLDS['oversold']:
        return "🟠 SELL"
    else:
        return "⚪ NEUTRAL"


def get_volatility_level(volatility: float) -> str:
    """Get volatility level string"""
    if volatility < 0.5:
        return "LOW"
    elif volatility < 1.5:
        return "MEDIUM"
    else:
        return "HIGH"


def format_quote(quote: Dict[str, Any], volatility: float) -> str:
    """Format quote for display"""
    symbol = quote['symbol']
    current = quote['current']
    change = quote['change']
    change_pct = quote['change_percent']
    high = quote['high']
    low = quote['low']

    vol_level = get_volatility_level(volatility)
    signal = generate_price_signal(quote)

    return (
        f"\n{'='*60}\n"
        f"📊 {symbol} | Volatility: {volatility:.2f}% ({vol_level})\n"
        f"{'='*60}\n"
        f"💰 Current: ${current:.2f}\n"
        f"📈 Change: {change:+.2f} ({change_pct:+.2f}%)\n"
        f"📊 Range: ${low:.2f} - ${high:.2f}\n"
        f"🎯 Signal: {signal}\n"
        f"{'='*60}\n"
    )


def format_insider(transactions: list) -> str:
    """Format insider transactions"""
    if not transactions:
        return "📭 No recent insider transactions\n"

    output = f"📊 Insider Transactions ({len(transactions)}):\n"
    for tx in transactions[:5]:  # Show max 5
        name = tx.get('name', 'N/A')
        change = tx.get('change', 0)
        tx_date = tx.get('transactionDate', 'N/A')
        tx_code = tx.get('transactionCode', 'N/A')

        emoji = "📈" if change > 0 else "📉"
        output += f"  {emoji} {name} ({tx_code}): {change:+,} shares on {tx_date}\n"

    return output
