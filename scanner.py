#!/usr/bin/env python3
"""
Personal Hedge Fund Scanner
===========================
Buffett-Style Value Investing + RSI Dip Detection

Scans blue-chip stocks for 'Buy the Dip' opportunities using:
1. Technical: RSI(14) < 30 (oversold) + 200-day MA trend filter
2. Value: Trailing P/E, P/B (sector-aware), ROE, Debt/Equity (sector-aware)
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
    MAX_TRAILING_PE,
    MAX_PRICE_TO_BOOK,
    MIN_ROE,
    MIN_REVENUE_GROWTH,
    MAX_DEBT_TO_EQUITY,
    PB_EXEMPT_SECTORS,
    DE_EXEMPT_SECTORS,
    EMAIL_SUBJECT,
    ENABLE_RSI,
    ENABLE_200D_MA,
    ENABLE_PE,
    ENABLE_PB,
    ENABLE_ROE_GROWTH,
    ENABLE_DE,
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

    Returns dict with: trailingPE, priceToBook, returnOnEquity, debtToEquity
    """
    try:
        info = ticker.info
        return {
            "trailingPE": info.get("trailingPE"),
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


def check_criteria(rsi: float, fundamentals: dict, above_200d_ma: bool = True) -> tuple[bool, list[str], int, int]:
    """
    Check if stock meets all criteria.
    Sector-aware: skips P/B for tech/comms, skips D/E for financials.

    Returns:
        Tuple of (passed: bool, failed_reasons: list, criteria_missed: int, criteria_total: int)
    """
    reasons = []
    sector = fundamentals.get("sector", "N/A")
    total_count = 0
    missed_count = 0

    # RSI Check
    if ENABLE_RSI:
        total_count += 1
        if rsi >= RSI_OVERSOLD:
            missed_count += 1
            reasons.append(f"RSI {rsi:.1f} >= {RSI_OVERSOLD}")

    # 200-Day MA Check (trend context)
    if ENABLE_200D_MA:
        total_count += 1
        if not above_200d_ma:
            missed_count += 1
            reasons.append("Price BELOW 200-day MA (falling knife risk)")

    # Trailing P/E Check
    if ENABLE_PE:
        total_count += 1
        pe = fundamentals.get("trailingPE")
        if pe is None:
            missed_count += 1
            reasons.append("No P/E data")
        elif pe > MAX_TRAILING_PE:
            missed_count += 1
            reasons.append(f"P/E {pe:.1f} > {MAX_TRAILING_PE}")

    # Price-to-Book Check (skipped for tech/comms — their value is in IP)
    if ENABLE_PB:
        if sector not in PB_EXEMPT_SECTORS:
            total_count += 1
            pb = fundamentals.get("priceToBook")
            if pb is None:
                missed_count += 1
                reasons.append("No P/B data")
            elif pb > MAX_PRICE_TO_BOOK:
                missed_count += 1
                reasons.append(f"P/B {pb:.1f} > {MAX_PRICE_TO_BOOK}")

    # ROE OR Revenue Growth Check (quality OR growth)
    if ENABLE_ROE_GROWTH:
        total_count += 1
        roe = fundamentals.get("returnOnEquity")
        rev_growth = fundamentals.get("revenueGrowth")

        roe_pass = roe is not None and roe >= MIN_ROE
        growth_pass = rev_growth is not None and rev_growth >= MIN_REVENUE_GROWTH

        if not (roe_pass or growth_pass):
            missed_count += 1
            roe_str = f"{roe*100:.1f}%" if roe else "N/A"
            growth_str = f"{rev_growth*100:.1f}%" if rev_growth else "N/A"
            reasons.append(f"ROE {roe_str} < {MIN_ROE*100:.0f}% AND Growth {growth_str} < {MIN_REVENUE_GROWTH*100:.0f}%")

    # Debt-to-Equity Check (skipped for financials — leverage is their business)
    if ENABLE_DE:
        if sector not in DE_EXEMPT_SECTORS:
            total_count += 1
            de = fundamentals.get("debtToEquity")
            if de is None:
                missed_count += 1
                reasons.append("No D/E data")
            elif de > MAX_DEBT_TO_EQUITY * 100:  # yfinance returns as percentage
                missed_count += 1
                reasons.append(f"D/E {de:.0f}% > {MAX_DEBT_TO_EQUITY*100:.0f}%")

    # Minimum criteria floor — need at least 3 active criteria for a meaningful signal
    if total_count < 3:
        all_passed = False
        reasons.append(f"Too few active criteria ({total_count})")
    else:
        all_passed = missed_count == 0

    return all_passed, reasons, missed_count, total_count


def analyze_stock(symbol: str) -> Optional[dict]:
    """
    Analyze a single stock against our criteria.
    """
    print(f"Analyzing {symbol}...")

    try:
        ticker = yf.Ticker(symbol)

        # Fetch 1-year price history for RSI + 200-day MA
        hist = ticker.history(period="1y")

        if hist.empty or len(hist) < RSI_PERIOD:
            print(f"  ⚠️  Insufficient price data for {symbol}")
            return None

        close = hist["Close"]
        current_price = close.iloc[-1]

        # Calculate RSI
        rsi_series = calculate_rsi(close, RSI_PERIOD)
        current_rsi = rsi_series.iloc[-1]

        # Calculate 200-day MA trend context
        if len(close) >= 200:
            ma_200 = close.rolling(window=200).mean().iloc[-1]
            above_200d_ma = current_price > ma_200
        else:
            # Not enough data for 200-day MA, use what we have
            ma_200 = close.mean()
            above_200d_ma = current_price > ma_200

        # Get fundamentals
        fundamentals = get_fundamentals(ticker)
        sector = fundamentals.get("sector", "N/A")

        # Display metrics
        print(f"  {fundamentals.get('shortName', symbol)}")
        print(f"  Sector: {sector}")
        print(f"  Price: ${current_price:.2f}")
        print(f"  200-day MA: ${ma_200:.2f} ({'ABOVE' if above_200d_ma else 'BELOW'})")
        print(f"  RSI(14): {current_rsi:.2f}")
        print(f"  Trailing P/E: {format_value(fundamentals.get('trailingPE'))}")
        print(f"  Price/Book: {format_value(fundamentals.get('priceToBook'))}{' [exempt]' if sector in PB_EXEMPT_SECTORS else ''}")
        print(f"  ROE: {format_value(fundamentals.get('returnOnEquity'), '.1%')}")
        print(f"  Revenue Growth: {format_value(fundamentals.get('revenueGrowth'), '.1%')}")
        print(f"  Debt/Equity: {format_value(fundamentals.get('debtToEquity'), '.0f', '%')}{' [exempt]' if sector in DE_EXEMPT_SECTORS else ''}")

        # Check criteria
        passed, reasons, criteria_missed, criteria_total = check_criteria(current_rsi, fundamentals, above_200d_ma)

        # Calculate FCF Yield if available
        fcf = fundamentals.get("freeCashflow")
        mcap = fundamentals.get("marketCap")
        fcf_yield = (fcf / mcap * 100) if fcf is not None and mcap not in (None, 0) else None

        if passed:
            print(f"  ✅ SIGNAL TRIGGERED! Missed: 0/{criteria_total}")
        else:
            print(f"  ❌ No signal (missed {criteria_missed}/{criteria_total}): {', '.join(reasons)}")

        return {
            "symbol": symbol,
            "name": fundamentals.get("shortName", symbol),
            "sector": fundamentals.get("sector", "N/A"),
            "price": current_price,
            "rsi": current_rsi,
            "ma_200": ma_200,
            "above_200d_ma": above_200d_ma,
            "trailing_pe": fundamentals.get("trailingPE"),
            "price_to_book": fundamentals.get("priceToBook"),
            "roe": fundamentals.get("returnOnEquity"),
            "revenue_growth": fundamentals.get("revenueGrowth"),
            "debt_to_equity": fundamentals.get("debtToEquity"),
            "fcf_yield": fcf_yield,
            "criteria_missed": criteria_missed,
            "criteria_total": criteria_total,
            "signal": passed,
            "failed_reasons": reasons,
        }

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
• RSI(14) < {RSI_OVERSOLD} (Oversold - The Dip){'' if ENABLE_RSI else ' [OFF]'}
• Price ABOVE 200-day MA (Uptrend confirmation){'' if ENABLE_200D_MA else ' [OFF]'}
• Trailing P/E < {MAX_TRAILING_PE} (Earnings Value - real numbers){'' if ENABLE_PE else ' [OFF]'}
• Price/Book < {MAX_PRICE_TO_BOOK} (Asset Value - skipped for Tech/Comms){'' if ENABLE_PB else ' [OFF]'}
• ROE > {MIN_ROE*100:.0f}% OR Revenue Growth > {MIN_REVENUE_GROWTH*100:.0f}% (Quality or Growth){'' if ENABLE_ROE_GROWTH else ' [OFF]'}
• Debt/Equity < {MAX_DEBT_TO_EQUITY*100:.0f}% (Conservative - skipped for Financials){'' if ENABLE_DE else ' [OFF]'}

---
"""

    for signal in signals:
        roe_str = f"{signal['roe']*100:.1f}%" if signal['roe'] else "N/A"
        growth_str = f"{signal['revenue_growth']*100:.1f}%" if signal['revenue_growth'] else "N/A"
        de_str = f"{signal['debt_to_equity']:.0f}%" if signal['debt_to_equity'] else "N/A"
        fcf_str = f"{signal['fcf_yield']:.1f}%" if signal['fcf_yield'] else "N/A"

        ma_str = "ABOVE" if signal['above_200d_ma'] else "BELOW"
        pb_str = f"{signal['price_to_book']:.2f}" if signal['price_to_book'] else "N/A"
        pe_str = f"{signal['trailing_pe']:.2f}" if signal['trailing_pe'] else "N/A"

        body += f"""
📊 {signal['symbol']} - {signal['name']}
   Sector: {signal['sector']}
   Price: ${signal['price']:.2f}

   Technical:
   • RSI(14): {signal['rsi']:.2f}
   • 200-day MA: ${signal['ma_200']:.2f} ({ma_str})

   Value Metrics:
   • Trailing P/E: {pe_str}
   • Price/Book: {pb_str}
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
    print(f"  • RSI(14) < {RSI_OVERSOLD}{'' if ENABLE_RSI else ' [OFF]'}")
    print(f"  • Price ABOVE 200-day MA{'' if ENABLE_200D_MA else ' [OFF]'}")
    print(f"  • Trailing P/E < {MAX_TRAILING_PE}{'' if ENABLE_PE else ' [OFF]'}")
    print(f"  • Price/Book < {MAX_PRICE_TO_BOOK} (skipped for Tech/Comms){'' if ENABLE_PB else ' [OFF]'}")
    print(f"  • ROE > {MIN_ROE*100:.0f}% OR Revenue Growth > {MIN_REVENUE_GROWTH*100:.0f}%{'' if ENABLE_ROE_GROWTH else ' [OFF]'}")
    print(f"  • Debt/Equity < {MAX_DEBT_TO_EQUITY*100:.0f}% (skipped for Financials){'' if ENABLE_DE else ' [OFF]'}")
    print("-" * 60)

    all_results = []

    for symbol in WATCHLIST:
        result = analyze_stock(symbol)
        if result:
            all_results.append(result)
        print()

    # Separate perfect signals from partial matches
    signals = [r for r in all_results if r["signal"]]
    # Sort all results by fewest missed criteria (best first)
    all_results.sort(key=lambda r: r["criteria_missed"])

    print("=" * 60)
    print(f"SUMMARY: {len(signals)} signal(s) out of {len(WATCHLIST)} stocks")
    print("=" * 60)

    if signals:
        print("\n🚨 SIGNALS TRIGGERED (missed 0):")
        for s in signals:
            roe_str = f"{s['roe']*100:.1f}%" if s['roe'] else "N/A"
            growth_str = f"{s['revenue_growth']*100:.1f}%" if s['revenue_growth'] else "N/A"
            de_str = f"{s['debt_to_equity']:.0f}%" if s['debt_to_equity'] else "N/A"
            pe_str = f"{s['trailing_pe']:.1f}" if s['trailing_pe'] else "N/A"
            pb_str = f"{s['price_to_book']:.1f}" if s['price_to_book'] else "N/A"
            ma_str = "ABOVE" if s['above_200d_ma'] else "BELOW"
            print(f"   • {s['symbol']} @ ${s['price']:.2f} [missed 0/{s['criteria_total']}]")
            print(f"     200d MA: {ma_str} | RSI: {s['rsi']:.1f} | P/E: {pe_str} | P/B: {pb_str}")
            print(f"     ROE: {roe_str} | Growth: {growth_str} | D/E: {de_str}")

        send_email(signals)
    else:
        print("\n✨ No signals today. Waiting for better value opportunities!")

    # Show near-misses (missed exactly 1 criterion)
    near_misses = [r for r in all_results if not r["signal"] and r["criteria_missed"] == 1]
    if near_misses:
        print(f"\n👀 NEAR MISSES ({len(near_misses)} stocks missed 1 criterion):")
        for s in near_misses:
            print(f"   • {s['symbol']} @ ${s['price']:.2f} [missed 1/{s['criteria_total']}]")
            print(f"     Failed: {', '.join(s['failed_reasons'])}")

    return len(signals)


if __name__ == "__main__":
    main()
    exit(0)
