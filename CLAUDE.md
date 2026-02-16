# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal Hedge Fund Bot - An automated stock scanner that monitors 417 global blue-chip stocks across 16 international markets for "Buy the Dip" opportunities using Buffett-style value investing combined with RSI-based technical analysis.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the scanner
python3 scanner.py

# Run with email notifications (optional)
export EMAIL_SENDER="your-gmail@gmail.com"
export EMAIL_PASSWORD="your-app-password"
export EMAIL_RECEIVER="receiver@email.com"
python3 scanner.py
```

## Architecture

### Signal Flow
```
config.py (417 stocks from 16 markets)
    ↓
scanner.py main loop (per symbol)
    ├─ Fetch 1-month price history via yfinance
    ├─ Calculate RSI(14)
    ├─ Fetch fundamentals (P/E, P/B, ROE, D/E, growth)
    └─ Apply 6 criteria filters
    ↓
Accumulate passing signals → Output + optional email
```

### Key Modules

**scanner.py** - Core scanning logic:
- `calculate_rsi()` - RSI(14) using exponential moving average
- `get_fundamentals()` - Fetches yfinance ticker data
- `check_criteria()` - Validates against all filters (RSI<30, P/E<25, P/B<3, ROE>10% OR Growth>5%, D/E<100%)
- `analyze_stock()` - Full analysis of single stock
- `main()` - Entry point orchestrating the scan

**config.py** - Watchlist and strategy parameters:
- 15 regional market lists combined into deduped `WATCHLIST`
- All thresholds configurable: `RSI_OVERSOLD`, `MAX_FORWARD_PE`, `MAX_PRICE_TO_BOOK`, `MIN_ROE`, `MIN_REVENUE_GROWTH`, `MAX_DEBT_TO_EQUITY`

**manager.txt** - Stress-testing framework:
- 5-question investment decision template designed to be fed to Claude
- Used for due diligence on triggered signals before entry

### Automation

GitHub Actions workflow (`.github/workflows/scan.yml`):
- Runs Monday-Friday at 21:00 UTC (post-US market close)
- Requires repository secrets: `EMAIL_SENDER`, `EMAIL_PASSWORD`, `EMAIL_RECEIVER`
