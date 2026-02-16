# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal Hedge Fund Bot - An automated stock scanner that monitors 417 global blue-chip stocks across 16 international markets for "Buy the Dip" opportunities using Buffett-style value investing combined with RSI-based technical analysis.

## Full Analysis Workflow

> **When asked to "run the analysis", "generate a report", or "do the full analysis", you MUST complete ALL 3 steps below. The scanner alone is not a complete analysis.**

### Step 1: Run the Scanner

```bash
python3 scanner.py
```

Captures the output. Every stock gets a percentage score (`criteria_passed / criteria_applicable`). Stocks at 100% are signals.

### Step 2: Stress Test Every Signal

For each stock that triggered a signal (100% score):
1. Read `stress_test.txt` for the 5-question prompt template
2. Research the stock using web search (current news, financials, competitive landscape)
3. Answer all 5 questions with data and brutal honesty
4. Assign a verdict: **Golden Opportunity**, **Value Trap**, or **Wait & See** + confidence score (0-100%)

**Run all signal stocks in parallel** (one agent per stock) for speed.

### Step 3: Generate the Analysis Report

Create `ANALYSIS_YYYY-MM-DD.md` with this structure:

**TOP: TL;DR section**
- Day-over-day changes vs previous report (compare with most recent `ANALYSIS_*.md`)
- Stress test scorecard table: all signals with Stock | Price | Verdict | Confidence | Core Thesis Killer
- Recommendations split into: AVOID (value traps) and WATCHLIST (wait & see, with catalysts to watch)
- "If forced to pick one right now" assessment
- Individual stress test reports in collapsible `<details>` tags

**BOTTOM: Full Scanner Data**
- All 417 stocks grouped by score percentage (100%, 80%+, 60%+, etc.)
- Tables with all metrics: RSI, 200d MA, Trailing P/E, P/B, ROE, Growth, D/E, Sector, Price

## Architecture

### Signal Flow
```
config.py (417 stocks from 16 markets)
    ↓
scanner.py main loop (per symbol)
    ├─ Fetch 1-year price history via yfinance
    ├─ Calculate RSI(14) + 200-day MA
    ├─ Fetch fundamentals (Trailing P/E, P/B, ROE, D/E, growth)
    └─ Apply sector-aware criteria filters + percentage scoring
    ↓
Signals (100%) + Near-misses (80%+) → Stress test → Analysis report
```

### Key Modules

**scanner.py** - Core scanning logic:
- `calculate_rsi()` - RSI(14) using exponential moving average
- `get_fundamentals()` - Fetches yfinance ticker data
- `check_criteria()` - Sector-aware filters returning (passed, reasons, criteria_passed, criteria_total)
- `analyze_stock()` - Full analysis returning all metrics + score percentage for every stock
- `main()` - Entry point: scans all stocks, shows signals + near-misses

**config.py** - Watchlist and strategy parameters:
- 15 regional market lists combined into deduped `WATCHLIST`
- All thresholds configurable: `RSI_OVERSOLD`, `MAX_TRAILING_PE`, `MAX_PRICE_TO_BOOK`, `MIN_ROE`, `MIN_REVENUE_GROWTH`, `MAX_DEBT_TO_EQUITY`
- Sector exemptions: `PB_EXEMPT_SECTORS` (Technology, Communication Services), `DE_EXEMPT_SECTORS` (Financial Services)

**stress_test.txt** - Hedge fund stress test prompt:
- 5-question template: Falling Knife, 20-Year Survival, Moat Check, Valuation Trap, Verdict
- Must be run on every signal stock before including in the report
