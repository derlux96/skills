"""
FinnHub API Client for AMIP Scanner
"""

import requests
import json
from datetime import datetime
from typing import Dict, Any, List, Optional


class FinnhubClient:
    """Simplified FinnHub Client for Scanner"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://finnhub.io/api/v1"
        self.session = requests.Session()

    def _request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Internal request method"""
        if params is None:
            params = {}
        params['token'] = self.api_key

        try:
            response = self.session.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error fetching {endpoint}: {e}")
            return {}

    def get_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get real-time quote for stock"""
        data = self._request("/quote", {"symbol": symbol})
        if 'c' in data and data['c'] > 0:
            return {
                'symbol': symbol,
                'current': data['c'],
                'change': data['d'],
                'change_percent': data['dp'],
                'high': data['h'],
                'low': data['l'],
                'open': data['o'],
                'previous_close': data['pc'],
                'timestamp': data['t']
            }
        return None

    def get_stock_candles(self, symbol: str, count: int = 20) -> Optional[Dict[str, Any]]:
        """Get stock candles for volatility calculation"""
        params = {
            "symbol": symbol,
            "resolution": "D",  # Daily candles
            "count": count
        }
        data = self._request("/stock/candle", params)
        if 's' not in data or data['s'] != 'ok':
            return None

        return {
            'symbol': symbol,
            'candles': [
                {
                    'timestamp': t,
                    'open': o,
                    'high': h,
                    'low': l,
                    'close': c,
                    'volume': v
                }
                for t, o, h, l, c, v in zip(
                    data['t'], data['o'], data['h'], data['l'], data['c'], data['v']
                )
            ]
        }

    def get_insider_transactions(self, symbol: str, count: int = 10) -> List[Dict[str, Any]]:
        """Get recent insider transactions"""
        data = self._request("/stock/insider-transactions", {"symbol": symbol})
        transactions = data.get('data', [])
        return transactions[:count]

    def get_company_news(self, symbol: str, count: int = 5) -> List[Dict[str, Any]]:
        """Get latest company news"""
        from_date = datetime.now().replace(day=1).strftime("%Y-%m-%d")
        to_date = datetime.now().strftime("%Y-%m-%d")

        data = self._request("/company-news", {
            "symbol": symbol,
            "from": from_date,
            "to": to_date
        })
        return data[:count]


def calculate_volatility(candles: List[Dict[str, Any]]) -> float:
    """Calculate daily volatility as standard deviation of returns"""
    if len(candles) < 2:
        return 0.0

    # Calculate daily returns
    returns = []
    for i in range(1, len(candles)):
        prev_close = candles[i-1]['close']
        curr_close = candles[i]['close']
        if prev_close > 0:
            ret = (curr_close - prev_close) / prev_close * 100
            returns.append(ret)

    if not returns:
        return 0.0

    # Calculate standard deviation
    import statistics
    try:
        return statistics.stdev(returns)
    except statistics.StatisticsError:
        return 0.0
