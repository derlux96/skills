#!/usr/bin/env python3
"""
AMIP Scanner - Adaptive Scanning Engine MVP
"""

import time
import logging
from datetime import datetime
from pathlib import Path

from config import (
    FINNHUB_API_KEY,
    DEFAULT_SCAN_INTERVAL,
    SCAN_INTERVALS,
    VOLATILITY_THRESHOLDS,
    SCAN_TARGETS,
    LOG_LEVEL,
    LOG_FILE
)
from finnhub_client import FinnhubClient, calculate_volatility
from signals import (
    format_quote,
    format_insider,
    generate_price_signal,
    get_volatility_level
)


# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AdaptiveScanner:
    """Adaptive Market Scanner"""

    def __init__(self):
        self.client = FinnhubClient(FINNHUB_API_KEY)
        self.scan_interval = DEFAULT_SCAN_INTERVAL
        self.price_history = {}  # Store last prices for alerts
        self.running = False

        # Create data directories
        Path("./data").mkdir(exist_ok=True)
        Path("./cache").mkdir(exist_ok=True)

    def get_scan_interval(self, volatility: float) -> int:
        """Calculate adaptive scan interval based on volatility"""
        if volatility < VOLATILITY_THRESHOLDS['low']:
            return SCAN_INTERVALS['low']
        elif volatility < VOLATILITY_THRESHOLDS['medium']:
            return SCAN_INTERVALS['medium']
        else:
            return SCAN_INTERVALS['high']

    def scan_symbol(self, symbol: str) -> dict:
        """Scan a single symbol"""
        logger.info(f"📡 Scanning {symbol}...")

        # Get current quote
        quote = self.client.get_quote(symbol)
        if not quote:
            logger.error(f"❌ Failed to get quote for {symbol}")
            return None

        # Get candles for volatility
        candles = self.client.get_stock_candles(symbol, count=20)
        volatility = calculate_volatility(candles) if candles else 0.0

        # Get insider transactions
        insider = self.client.get_insider_transactions(symbol, count=5)

        # Check for price alerts (significant change from last scan)
        last_price = self.price_history.get(symbol)
        alert_msg = ""
        if last_price:
            price_change_pct = ((quote['current'] - last_price) / last_price) * 100
            if abs(price_change_pct) > 1.0:  # >1% since last scan
                alert_msg = f"\n🚨 PRICE ALERT: {price_change_pct:+.2f}% since last scan!\n"

        # Store current price
        self.price_history[symbol] = quote['current']

        # Format output
        result = {
            'symbol': symbol,
            'quote': quote,
            'volatility': volatility,
            'volatility_level': get_volatility_level(volatility),
            'insider_count': len(insider),
            'scan_interval': self.get_scan_interval(volatility),
            'signal': generate_price_signal(quote),
            'alert': alert_msg
        }

        return result

    def scan_all(self) -> list:
        """Scan all target symbols"""
        results = []

        for symbol in SCAN_TARGETS:
            try:
                result = self.scan_symbol(symbol)
                if result:
                    results.append(result)
            except Exception as e:
                logger.error(f"❌ Error scanning {symbol}: {e}")

        return results

    def print_results(self, results: list):
        """Print scan results"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"\n{'='*60}")
        print(f"📊 AMIP SCANNER - Scan Results")
        print(f"{'='*60}")
        print(f"🕐 Timestamp: {timestamp}")
        print(f"📡 Targets: {len(SCAN_TARGETS)}")
        print(f"{'='*60}\n")

        # Find overall volatility level (max of all)
        max_vol = max([r['volatility'] for r in results]) if results else 0
        overall_scan_interval = self.get_scan_interval(max_vol)

        print(f"⚡ Overall Volatility: {max_vol:.2f}%")
        print(f"⏰ Next scan in: {overall_scan_interval} seconds ({overall_scan_interval//60} min)\n")

        for result in results:
            print(format_quote(result['quote'], result['volatility']))
            if result['alert']:
                print(result['alert'])

            if result['insider_count'] > 0:
                insider = self.client.get_insider_transactions(result['symbol'], count=5)
                print(format_insider(insider))

        self.scan_interval = overall_scan_interval

    def run(self):
        """Main scanner loop"""
        self.running = True
        logger.info("🚀 AMIP Scanner started")

        try:
            while self.running:
                logger.info("📡 Starting scan cycle...")

                # Scan all symbols
                results = self.scan_all()

                if results:
                    self.print_results(results)

                # Wait for next scan
                logger.info(f"⏰ Waiting {self.scan_interval} seconds for next scan...")
                time.sleep(self.scan_interval)

        except KeyboardInterrupt:
            logger.info("⏹️ Scanner stopped by user")
        except Exception as e:
            logger.error(f"❌ Scanner error: {e}")
        finally:
            self.running = False


def main():
    """Main entry point"""
    print("""
    ╔═════════════════════════════════════════════════════════╗
    ║           🤖 AMIP ADAPTIVE MARKET SCANNER 🤖             ║
    ║                                                              ║
    ║   Adaptive Scanning Engine for Proof-of-Concept            ║
    ║   Press Ctrl+C to stop                                     ║
    ╚═════════════════════════════════════════════════════════╝
    """)

    scanner = AdaptiveScanner()
    scanner.run()


if __name__ == "__main__":
    main()
