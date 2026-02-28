#!/usr/bin/env python3
"""
FinnHub API Client
Free API for realtime stock, forex, crypto data
Docs: https://finnhub.io/docs/api
"""

import os
import sys
import json
import requests
from datetime import datetime
from typing import Optional, List, Dict, Any

# API Key - Free tier
FINNHUB_API_KEY = "d645mohr01ql6dj29o2gd645mohr01ql6dj29o30"
BASE_URL = "https://finnhub.io/api/v1"


class FinnhubClient:
    """FinnHub API Client"""

    def __init__(self, api_key: str = FINNHUB_API_KEY):
        self.api_key = api_key
        self.base_url = BASE_URL
        self.session = requests.Session()

    def _request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Internal request method"""
        params['token'] = self.api_key
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    # ============== STOCK DATA ==============

    def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        """Get company profile, metrics, and financials"""
        return self._request("/stock/profile2", {"symbol": symbol})

    def get_stock_quote(self, symbol: str) -> Dict[str, Any]:
        """Get real-time quote for stock"""
        return self._request("/quote", {"symbol": symbol})

    def get_stock_candles(self, symbol: str, resolution: str = "D",
                        count: int = 100) -> Dict[str, Any]:
        """Get stock candles (OHLCV)"""
        params = {
            "symbol": symbol,
            "resolution": resolution,  # 1, 5, 15, 30, 60, D, W, M
            "count": count
        }
        return self._request("/stock/candle", params)

    def get_company_peers(self, symbol: str) -> List[str]:
        """Get company peers"""
        return self._request("/stock/peers", {"symbol": symbol})

    def get_company_basic_financials(self, symbol: str) -> Dict[str, Any]:
        """Get company basic financials"""
        return self._request("/stock/metric", {"symbol": symbol, "metric": "all"})

    # ============== INSIDER TRADING ==============

    def get_insider_transactions(self, symbol: str, from_date: str = None,
                             to_date: str = None) -> List[Dict[str, Any]]:
        """Get insider transactions"""
        params = {"symbol": symbol}
        if from_date:
            params['from'] = from_date
        if to_date:
            params['to'] = to_date
        return self._request("/stock/insider-transactions", params).get('data', [])

    def get_insider_sentiment(self, symbol: str, from_date: str = None,
                            to_date: str = None) -> Dict[str, Any]:
        """Get insider sentiment"""
        params = {"symbol": symbol}
        if from_date:
            params['from'] = from_date
        if to_date:
            params['to'] = to_date
        return self._request("/stock/insider-sentiment", params)

    # ============== NEWS & ANALYSIS ==============

    def get_company_news(self, symbol: str, from_date: str = None,
                      to_date: str = None) -> List[Dict[str, Any]]:
        """Get company news"""
        if not from_date:
            from_date = (datetime.now().replace(day=1)).strftime("%Y-%m-%d")
        if not to_date:
            to_date = datetime.now().strftime("%Y-%m-%d")
        return self._request("/company-news", {
            "symbol": symbol,
            "from": from_date,
            "to": to_date
        })

    def get_market_news(self, category: str = "general", min_id: int = 0) -> List[Dict[str, Any]]:
        """Get market news by category (general, forex, crypto, merger)"""
        return self._request("/news", {
            "category": category,
            "minId": min_id
        })

    def get_news_sentiment(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get news sentiment for a company (FREE TIER: Not available)"""
        # Note: This endpoint requires paid subscription
        # Returns None instead of raising error
        return None

    # ============== TECHNICAL INDICATORS ==============

    def get_technical_indicators(self, symbol: str, resolution: str = "D",
                               indicator: str = "sma") -> Dict[str, Any]:
        """Get technical indicators (sma, ema, rsi, macd, etc.)"""
        return self._request("/indicator", {
            "symbol": symbol,
            "resolution": resolution,
            "indicator": indicator
        })

    # ============== EARNINGS ==============

    def get_earnings_surprises(self, symbol: str) -> List[Dict[str, Any]]:
        """Get earnings surprises"""
        return self._request("/stock/earnings", {"symbol": symbol}).get('data', [])


def format_insider_transaction(tx: Dict[str, Any]) -> str:
    """Format insider transaction for display"""
    return (
        f"📅 {tx.get('transactionDate', 'N/A')} | "
        f"👤 {tx.get('name', 'N/A')} | "
        f"🔄 {tx.get('transactionCode', 'N/A')} | "
        f"📊 Change: {tx.get('change', 0)} shares | "
        f"💰 Price: ${tx.get('transactionPrice', 0)}"
    )


def main():
    """Test function"""
    client = FinnhubClient()

    print("=" * 60)
    print("📊 FINNHUB API TEST")
    print("=" * 60)

    # Test 1: Company Profile
    print("\n1️⃣ Company Profile (AAPL):")
    profile = client.get_company_profile("AAPL")
    print(json.dumps(profile, indent=2))

    # Test 2: Stock Quote
    print("\n2️⃣ Stock Quote (AAPL):")
    quote = client.get_stock_quote("AAPL")
    print(json.dumps(quote, indent=2))

    # Test 3: Insider Transactions
    print("\n3️⃣ Insider Transactions (AAPL):")
    transactions = client.get_insider_transactions("AAPL")
    for tx in transactions[:3]:
        print(format_insider_transaction(tx))

    # Test 4: Company News
    print("\n4️⃣ Company News (AAPL):")
    news = client.get_company_news("AAPL")
    for article in news[:3]:
        print(f"📰 {article.get('headline', 'N/A')} | "
              f"📅 {article.get('datetime', 'N/A')} | "
              f"🔗 {article.get('url', 'N/A')}")


if __name__ == "__main__":
    main()
