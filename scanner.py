#!/usr/bin/env python3
"""
Personal Hedge Fund Scanner
===========================
Buffett-Style Value Investing + RSI Dip Detection

Scans blue-chip stocks for 'Buy the Dip' opportunities using:
1. Technical: RSI(14) < 30 (oversold)
2. Value: Forward P/E, P/B, ROE, Debt/Equity filters
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Optional

import numpy as np
import pandas as pd
import yfinance as yf

from config import (
    WATCHLIST,
    RSI_PERIOD,
    RSI_OVERSOLD,
    MAX_FORWARD_PE,
    MAX_PRICE_TO_BOOK,
    MIN_ROE,
    MIN_REVENUE_GROWTH,
    MAX_DEBT_TO_EQUITY,
    EMAIL_SUBJECT,
)


def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate Relative Strength Index (RSI).
    """
    delta = prices.diff()

    gains = delta.where(delta > 0, 0.0)
    losses = (-delta).where(delta < 0, 0.0)

    avg_gains = gains.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    avg_losses = losses.ewm(alpha=1/period, min_periods=period, adjust=False).mean()

    rs = avg_gains / avg_losses
    rsi = 100 - (100 / (1 + rs))

    return rsi


def get_fundamentals(ticker: yf.Ticker) -> dict:
    """
    Fetch fundamental data from yfinance.

    Returns dict with: forwardPE, priceToBook, returnOnEquity, debtToEquity
    """
    try:
        info = ticker.info
        return {
            "forwardPE": info.get("forwardPE"),
            "priceToBook": info.get("priceToBook"),
            "returnOnEquity": info.get("returnOnEquity"),
            "revenueGrowth": info.get("revenueGrowth"),
            "debtToEquity": info.get("debtToEquity"),
            "marketCap": info.get("marketCap"),
            "freeCashflow": info.get("freeCashflow"),
            "sector": info.get("sector", "N/A"),
            "shortName": info.get("shortName", "N/A"),
        }
    except Exception as e:
        print(f"  ⚠️  Error fetching fundamentals: {e}")
        return {}


def format_value(value, fmt=".2f", suffix="", prefix=""):
    """Format a value for display, handling None."""
    if value is None:
        return "N/A"
    return f"{prefix}{value:{fmt}}{suffix}"


def check_criteria(rsi: float, fundamentals: dict) -> tuple[bool, list[str]]:
    """
    Check if stock meets all criteria.

    Returns:
        Tuple of (passed: bool, failed_reasons: list)
    """
    reasons = []

    # RSI Check
    if rsi >= RSI_OVERSOLD:
        reasons.append(f"RSI {rsi:.1f} >= {RSI_OVERSOLD}")

    # Forward P/E Check
    pe = fundamentals.get("forwardPE")
    if pe is None:
        reasons.append("No P/E data")
    elif pe > MAX_FORWARD_PE:
        reasons.append(f"P/E {pe:.1f} > {MAX_FORWARD_PE}")

    # Price-to-Book Check
    pb = fundamentals.get("priceToBook")
    if pb is None:
        reasons.append("No P/B data")
    elif pb > MAX_PRICE_TO_BOOK:
        reasons.append(f"P/B {pb:.1f} > {MAX_PRICE_TO_BOOK}")

    # ROE OR Revenue Growth Check (quality OR growth)
    roe = fundamentals.get("returnOnEquity")
    rev_growth = fundamentals.get("revenueGrowth")

    roe_pass = roe is not None and roe >= MIN_ROE
    growth_pass = rev_growth is not None and rev_growth >= MIN_REVENUE_GROWTH

    if not roe_pass and not growth_pass:
        roe_str = f"{roe*100:.1f}%" if roe else "N/A"
        growth_str = f"{rev_growth*100:.1f}%" if rev_growth else "N/A"
        reasons.append(f"ROE {roe_str} < {MIN_ROE*100:.0f}% AND Growth {growth_str} < {MIN_REVENUE_GROWTH*100:.0f}%")

    # Debt-to-Equity Check
    de = fundamentals.get("debtToEquity")
    if de is None:
        # Some companies (especially financials) may not have this
        pass  # Don't fail on missing D/E
    elif de > MAX_DEBT_TO_EQUITY * 100:  # yfinance returns as percentage
        reasons.append(f"D/E {de:.0f}% > {MAX_DEBT_TO_EQUITY*100:.0f}%")

    return len(reasons) == 0, reasons


def analyze_stock(symbol: str) -> Optional[dict]:
    """
    Analyze a single stock against our criteria.
    """
    print(f"Analyzing {symbol}...")

    try:
        ticker = yf.Ticker(symbol)

        # Fetch price history for RSI
        hist = ticker.history(period="1mo")

        if hist.empty or len(hist) < RSI_PERIOD:
            print(f"  ⚠️  Insufficient price data for {symbol}")
            return None

        close = hist["Close"]
        current_price = close.iloc[-1]

        # Calculate RSI
        rsi_series = calculate_rsi(close, RSI_PERIOD)
        current_rsi = rsi_series.iloc[-1]

        # Get fundamentals
        fundamentals = get_fundamentals(ticker)

        # Display metrics
        print(f"  {fundamentals.get('shortName', symbol)}")
        print(f"  Price: ${current_price:.2f}")
        print(f"  RSI(14): {current_rsi:.2f}")
        print(f"  Forward P/E: {format_value(fundamentals.get('forwardPE'))}")
        print(f"  Price/Book: {format_value(fundamentals.get('priceToBook'))}")
        print(f"  ROE: {format_value(fundamentals.get('returnOnEquity'), '.1%')}")
        print(f"  Revenue Growth: {format_value(fundamentals.get('revenueGrowth'), '.1%')}")
        print(f"  Debt/Equity: {format_value(fundamentals.get('debtToEquity'), '.0f', '%')}")

        # Check criteria
        passed, reasons = check_criteria(current_rsi, fundamentals)

        if passed:
            print(f"  ✅ SIGNAL TRIGGERED!")

            # Calculate FCF Yield if available
            fcf = fundamentals.get("freeCashflow")
            mcap = fundamentals.get("marketCap")
            fcf_yield = (fcf / mcap * 100) if fcf and mcap else None

            return {
                "symbol": symbol,
                "name": fundamentals.get("shortName", symbol),
                "sector": fundamentals.get("sector", "N/A"),
                "price": current_price,
                "rsi": current_rsi,
                "forward_pe": fundamentals.get("forwardPE"),
                "price_to_book": fundamentals.get("priceToBook"),
                "roe": fundamentals.get("returnOnEquity"),
                "revenue_growth": fundamentals.get("revenueGrowth"),
                "debt_to_equity": fundamentals.get("debtToEquity"),
                "fcf_yield": fcf_yield,
            }
        else:
            print(f"  ❌ No signal: {', '.join(reasons)}")
            return None

    except Exception as e:
        print(f"  ⚠️  Error analyzing {symbol}: {e}")
        return None


def format_email_body(signals: list[dict]) -> str:
    """
    Format the email body with signal details.
    """
    body = f"""
Personal Hedge Fund - Buy the Dip Alert
========================================
Scan Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}

{len(signals)} stock(s) triggered the Buffett-Style Value Dip criteria:

Criteria:
• RSI(14) < {RSI_OVERSOLD} (Oversold - The Dip)
• Forward P/E < {MAX_FORWARD_PE} (Earnings Value)
• Price/Book < {MAX_PRICE_TO_BOOK} (Asset Value)
• ROE > {MIN_ROE*100:.0f}% OR Revenue Growth > {MIN_REVENUE_GROWTH*100:.0f}% (Quality or Growth)
• Debt/Equity < {MAX_DEBT_TO_EQUITY*100:.0f}% (Conservative)

---
"""

    for signal in signals:
        roe_str = f"{signal['roe']*100:.1f}%" if signal['roe'] else "N/A"
        growth_str = f"{signal['revenue_growth']*100:.1f}%" if signal['revenue_growth'] else "N/A"
        de_str = f"{signal['debt_to_equity']:.0f}%" if signal['debt_to_equity'] else "N/A"
        fcf_str = f"{signal['fcf_yield']:.1f}%" if signal['fcf_yield'] else "N/A"

        body += f"""
📊 {signal['symbol']} - {signal['name']}
   Sector: {signal['sector']}
   Price: ${signal['price']:.2f}

   Technical:
   • RSI(14): {signal['rsi']:.2f}

   Value Metrics:
   • Forward P/E: {signal['forward_pe']:.2f}
   • Price/Book: {signal['price_to_book']:.2f}
   • ROE: {roe_str}
   • Revenue Growth: {growth_str}
   • Debt/Equity: {de_str}
   • FCF Yield: {fcf_str}

"""

    body += """
---
⚠️  Disclaimer: This is not financial advice. Do your own research.
🤖 Generated by Personal Hedge Fund Bot (Buffett Edition)
"""

    return body


def send_email(signals: list[dict]) -> bool:
    """
    Send email notification with signals.
    """
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")

    if not all([sender, password, receiver]):
        print("⚠️  Email credentials not configured. Skipping email notification.")
        print("   Set EMAIL_SENDER, EMAIL_PASSWORD, and EMAIL_RECEIVER environment variables.")
        return False

    try:
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = receiver
        msg["Subject"] = EMAIL_SUBJECT

        body = format_email_body(signals)
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)

        print(f"✅ Email sent successfully to {receiver}")
        return True

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False


def main():
    """Main entry point for the scanner."""
    print("=" * 60)
    print("Personal Hedge Fund Scanner (Buffett Edition)")
    print(f"Scan Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 60)
    print(f"\nWatchlist: {', '.join(WATCHLIST)}")
    print(f"\nCriteria:")
    print(f"  • RSI(14) < {RSI_OVERSOLD}")
    print(f"  • Forward P/E < {MAX_FORWARD_PE}")
    print(f"  • Price/Book < {MAX_PRICE_TO_BOOK}")
    print(f"  • ROE > {MIN_ROE*100:.0f}% OR Revenue Growth > {MIN_REVENUE_GROWTH*100:.0f}%")
    print(f"  • Debt/Equity < {MAX_DEBT_TO_EQUITY*100:.0f}%")
    print("-" * 60)

    signals = []

    for symbol in WATCHLIST:
        result = analyze_stock(symbol)
        if result:
            signals.append(result)
        print()

    print("=" * 60)
    print(f"SUMMARY: {len(signals)} signal(s) out of {len(WATCHLIST)} stocks")
    print("=" * 60)

    if signals:
        print("\n🚨 SIGNALS TRIGGERED:")
        for signal in signals:
            roe_str = f"{signal['roe']*100:.1f}%" if signal['roe'] else "N/A"
            growth_str = f"{signal['revenue_growth']*100:.1f}%" if signal['revenue_growth'] else "N/A"
            de_str = f"{signal['debt_to_equity']:.0f}%" if signal['debt_to_equity'] else "N/A"
            print(f"   • {signal['symbol']} @ ${signal['price']:.2f}")
            print(f"     RSI: {signal['rsi']:.1f} | P/E: {signal['forward_pe']:.1f} | P/B: {signal['price_to_book']:.1f}")
            print(f"     ROE: {roe_str} | Growth: {growth_str} | D/E: {de_str}")

        send_email(signals)
    else:
        print("\n✨ No signals today. Waiting for better value opportunities!")

    return len(signals)


if __name__ == "__main__":
    main()
    exit(0)
