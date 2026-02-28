#!/usr/bin/env python3.12
"""
pyonvista Test Script für TradePeter
SECURITY: Analyzed & Safe (Code-Level)
LEGAL: Grauzone (nicht-öffentliche API)
USE: Research/Testing only, Rate-Limited
"""

import asyncio
import sys
import re
from datetime import datetime, timedelta

# Rate-Limiting (max 10 requests/minute)
RATE_LIMIT_DELAY = 6  # seconds between requests


async def find_derivatives(ticker: str, derivative_type: str = "Turbo Long"):
    """
    Sucht Derivate für einen Ticker auf OnVista
    
    Args:
        ticker: Aktien-Ticker (z.B. "AAPL", "VLO")
        derivative_type: Typ (z.B. "Turbo Long", "Call", "Put")
    
    Returns:
        Liste von Instrumenten mit WKNs
    """
    try:
        # Lazy import (nur wenn gebraucht)
        try:
            from pyonvista import PyOnVista
            import aiohttp
        except ImportError as e:
            print(f"❌ Module nicht installiert: {e}")
            print("Installation: pip install pyonvista --break-system-packages")
            return []
        
        async with aiohttp.ClientSession() as client:
            api = PyOnVista()
            await api.install_client(client)
            
            # Search query
            search_query = f"{ticker} {derivative_type}"
            print(f"🔍 Suche: {search_query}")
            
            # Rate-Limiting
            await asyncio.sleep(RATE_LIMIT_DELAY)
            
            # Search
            instruments = await api.search_instrument(search_query)
            
            if not instruments:
                print(f"❌ Keine Derivate gefunden für: {ticker}")
                return []
            
            print(f"✅ {len(instruments)} Instrumente gefunden\n")
            
            results = []
            for i, inst in enumerate(instruments[:10], 1):  # Limit to 10
                # Extract WKN from ISIN or use fallback
                wkn = inst.isin[-6:] if inst.isin else "N/A"
                
                # Try to get more details (with rate-limiting)
                if i <= 3:  # Only first 3 for details
                    await asyncio.sleep(RATE_LIMIT_DELAY)
                    try:
                        detailed = await api.request_instrument(inst)
                        quote_price = detailed.quote.close if detailed.quote else "N/A"
                    except:
                        quote_price = "N/A"
                else:
                    quote_price = "N/A"
                
                result = {
                    "index": i,
                    "name": inst.name,
                    "isin": inst.isin,
                    "wkn": wkn,
                    "type": inst.type,
                    "symbol": inst.symbol,
                    "price": quote_price
                }
                results.append(result)
                
                # Print result
                print(f"{i:2d}. {inst.name}")
                print(f"    ISIN: {inst.isin}")
                print(f"    WKN:  {wkn}")
                print(f"    Typ:  {inst.type}")
                if quote_price != "N/A":
                    print(f"    Preis: {quote_price}€")
                print()
            
            return results
            
    except Exception as e:
        print(f"❌ Fehler: {e}")
        import traceback
        traceback.print_exc()
        return []


async def get_stock_info(ticker: str):
    """Holt Basis-Info für Aktie"""
    try:
        from pyonvista import PyOnVista
        import aiohttp
    except ImportError as e:
        print(f"❌ Module nicht installiert: {e}")
        return None
    
    async with aiohttp.ClientSession() as client:
        api = PyOnVista()
        await api.install_client(client)
        
        print(f"📊 Suche Aktie: {ticker}")
        
        await asyncio.sleep(RATE_LIMIT_DELAY)
        instruments = await api.search_instrument(ticker)
        
        if not instruments:
            print(f"❌ Aktie nicht gefunden: {ticker}")
            return None
        
        # First result should be the stock
        stock = instruments[0]
        
        await asyncio.sleep(RATE_LIMIT_DELAY)
        detailed = await api.request_instrument(stock)
        
        print(f"\n✅ {detailed.name}")
        print(f"   ISIN:   {detailed.isin}")
        print(f"   Symbol: {detailed.symbol}")
        print(f"   Typ:    {detailed.type}")
        
        if detailed.quote:
            print(f"\n📈 Quote:")
            print(f"   Preis:  {detailed.quote.close}€")
            print(f"   Open:   {detailed.quote.open}€")
            print(f"   High:   {detailed.quote.high}€")
            print(f"   Low:    {detailed.quote.low}€")
            print(f"   Datum:  {detailed.quote.timestamp}")
        
        return detailed


async def main():
    """Main test function"""
    if len(sys.argv) < 2:
        print("Verwendung: python3 pyonvista_test.py <TICKER> [DERIVAT-TYP]")
        print()
        print("Beispiele:")
        print("  python3 pyonvista_test.py AAPL")
        print("  python3 pyonvista_test.py VLO 'Turbo Long'")
        print("  python3 pyonvista_test.py PLTR Call")
        print()
        print("⚠️  WICHTIG: Rate-Limited auf 10 Requests/Min")
        print("⚠️  LEGAL: Grauzone (nicht-öffentliche API)")
        sys.exit(1)
    
    ticker = sys.argv[1].upper()
    derivative_type = sys.argv[2] if len(sys.argv) > 2 else "Turbo Long"
    
    print("=" * 70)
    print("pyonvista Test Script")
    print("=" * 70)
    print(f"Ticker: {ticker}")
    print(f"Derivat-Typ: {derivative_type}")
    print()
    print("⚠️  Rate-Limited: 6s zwischen Requests")
    print("⚠️  LEGAL: Grauzone - nur für Testing!")
    print("=" * 70)
    print()
    
    # Step 1: Get stock info (optional)
    # await get_stock_info(ticker)
    # print()
    
    # Step 2: Find derivatives
    results = await find_derivatives(ticker, derivative_type)
    
    print("=" * 70)
    print(f"Gefunden: {len(results)} Derivate")
    print("=" * 70)
    
    # Extract WKNs for easy copy-paste
    if results:
        print("\nWKNs (Copy-Paste):")
        wkns = [r["wkn"] for r in results if r["wkn"] != "N/A"]
        print(" | ".join(wkns[:5]))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Abgebrochen durch User")
    except Exception as e:
        print(f"\n❌ Fehler: {e}")
        import traceback
        traceback.print_exc()
