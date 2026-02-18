# Personal Hedge Fund Bot

A stock scanner monitoring **417 global stocks** across 16 markets for "Buy the Dip" opportunities using Buffett-style value investing with sector-aware filtering.

---

## How to Run a Full Analysis

> **IMPORTANT: A complete analysis is NOT just running the scanner. It is a 3-step process. All 3 steps must be completed to produce a useful report.**

### Step 1: Run the Scanner

```bash
pip install -r requirements.txt
python3 scanner.py
```

This scans all 417 stocks and outputs which ones pass ALL criteria (missed 0), plus near-misses (missed 1). Each stock gets a **criteria_missed** count — the number of criteria it failed. This makes comparison fair across sectors regardless of how many criteria apply.

### Step 2: Stress Test Every Signal

Stress test ALL stocks that missed at most 1 criterion (`criteria_missed <= 1`). Even if no stock missed 0, the near-misses (missed 1) are the most promising and must be evaluated.

For each stock:
1. Read `stress_test_based.txt` for the prompt template
2. Fill in `[TICKER]`, `[COMPANY_NAME]`, `[SECTOR]`, `[PRICE]`
3. Research the stock using current news, financials, and competitive landscape
4. Answer all 9 questions with data and specifics
5. Assign a verdict: **Asymmetric Opportunity**, **Value Trap**, or **Wait & See** with a confidence score

When using an LLM: run all signal stocks in parallel (one agent per stock) for speed.

### Step 3: Generate the Analysis Report

Create a file named `ANALYSIS_YYYY-MM-DD.md` with this structure:

```
1. TL;DR section (TOP of the report)
   - Day-over-day changes vs previous report (if one exists)
   - Stress test scorecard table (all signals with verdict + confidence + thesis killer)
   - Recommendations split into AVOID (value traps) and WATCHLIST (wait & see)
   - "If forced to pick one" assessment

2. Full Scanner Data (below the TL;DR)
   - All 417 stocks grouped by score percentage (100%, 80%+, 60%+, etc.)
   - Tables with all metrics: RSI, 200d MA, Trailing P/E, P/B, ROE, Growth, D/E
   - Sector and price for each stock
```

The TL;DR with stress test verdicts is the most important part of the report. Without it, the scanner data is just numbers without context.

---

## Strategy

The scanner signals when **ALL applicable criteria** are met:

| Indicator | Threshold | Purpose | Sector Exemptions |
|-----------|-----------|---------|-------------------|
| RSI(14) | < 30 | Identifies oversold stocks (the dip) | None |
| 200-day MA | Price above | Confirms uptrend (filters falling knives) | None |
| Trailing P/E | < 25 | Reasonable earnings valuation (real numbers) | None |
| Price/Book | < 3 | Not overpaying for assets | Skipped for Technology & Communication Services |
| ROE | > 10% | Quality business | None |
| Revenue Growth | > 5% | *OR* alternative to ROE for growth companies | None |
| Debt/Equity | < 100% | Conservative balance sheet | Skipped for Financial Services |

**Scoring:** Each stock is scored by `criteria_missed` — the number of criteria it failed. A stock that missed 0 is a signal. A stock that missed 1 is a near-miss. This makes comparison fair across sectors with different numbers of applicable criteria.

---

## Stress Test (stress_test_based.txt)

After the scanner identifies a dip, each signal is stress-tested with 9 questions using the "based" (balanced, objective) prompt:

| # | Test | Question |
|---|------|----------|
| 1 | Falling Knife vs. Mispricing | Temporary macro headwind or permanent structural impairment? Assign probabilities. |
| 2 | Tail-Risk Stress Test | 10-year pre-mortem (how it dies) + post-mortem (how it multi-bags). Which is more probable? |
| 3 | Moat Integrity Check | If they raised prices 10%, would customers stay? Compare to top 2 competitors. |
| 4 | Valuation Reality | Cheap vs own 10-year history and peers? Is the "E" sustainable, expanding, or deteriorating? |
| 5 | Cash Flow Autopsy | FCF vs net income over 3 years. Is cash conversion strong or leaking? |
| 6 | Smart Money Test | Insider buying/selling in past 6 months? Institutional accumulation or dumping? |
| 7 | Catalyst Calendar | 1-2 specific events in 3-12 months that could re-rate the stock. |
| 8 | Synthesis | Strongest short-seller pitch vs strongest activist pitch. Which has stronger structural backing? |
| 9 | Verdict | Asymmetric Opportunity / Value Trap / Wait & See + confidence % |

---

## Watchlist (417 Stocks)

| Market | Count | Examples |
|--------|-------|----------|
| S&P 500 | 107 | AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA, JPM, V, JNJ... |
| DAX | 36 | SAP, Siemens, Allianz, Mercedes, BMW, Porsche, Rheinmetall... |
| MDAX/SDAX | 30 | Carl Zeiss, Puma, Hugo Boss, Delivery Hero, Aixtron... |
| CAC 40 | 23 | LVMH, L'Oreal, Hermes, Kering, TotalEnergies, Sanofi... |
| FTSE 100 | 25 | Shell, AstraZeneca, HSBC, Unilever, BP, Rolls-Royce... |
| AEX | 15 | ASML, Heineken, ING, Philips, Akzo Nobel... |
| SMI | 15 | Nestle, Novartis, Roche, UBS, Richemont, Sika... |
| Nikkei | 30 | Toyota, Sony, Nintendo, Keyence, SoftBank, Honda... |
| KOSPI | 15 | Samsung, SK Hynix, Hyundai, Naver, Kakao, LG Chem... |
| China/HK | 35 | Alibaba, Tencent, BYD, PDD, JD, Xiaomi, Meituan... |
| ASX | 15 | BHP, Commonwealth Bank, CSL, Rio Tinto, Fortescue... |
| India ADRs | 9 | Infosys, HDFC Bank, ICICI, Tata Motors, Wipro... |
| Nordic | 23 | Novo Nordisk, Ericsson, Volvo, Maersk, Equinor, Nokia... |
| Southern EU | 16 | Santander, Inditex, Ferrari, Enel, UniCredit... |
| TSX | 15 | Royal Bank, TD, Shopify, Enbridge, CN Railway... |

Edit `config.py` to customize your watchlist.

---

## Customization

Edit `config.py` to adjust thresholds:

```python
RSI_OVERSOLD = 30           # Lower = stricter dip detection
MAX_TRAILING_PE = 25        # Lower = cheaper stocks only
MAX_PRICE_TO_BOOK = 3       # Lower = more asset-focused
MIN_ROE = 0.10              # Higher = quality only
MIN_REVENUE_GROWTH = 0.05   # Higher = growth only
MAX_DEBT_TO_EQUITY = 1.0    # Lower = safer balance sheets

# Sectors where specific criteria are skipped
PB_EXEMPT_SECTORS = {"Technology", "Communication Services"}
DE_EXEMPT_SECTORS = {"Financial Services"}
```

---

## Project Structure

```
.
├── config.py             # Watchlist (417 stocks) & strategy parameters
├── scanner.py            # Main scanning logic (RSI, 200d MA, sector-aware filters)
├── stress_test_based.txt  # Balanced hedge fund stress test prompt (9 questions)
├── stress_test_pessimist.txt # Bearish/cynical stress test prompt (9 questions)
├── requirements.txt      # Python dependencies
├── ANALYSIS_*.md         # Generated analysis reports
├── CLAUDE.md             # Instructions for Claude Code
└── README.md
```

---

## Optional: Email Notifications

```bash
export EMAIL_SENDER="your-gmail@gmail.com"
export EMAIL_PASSWORD="your-app-password"
export EMAIL_RECEIVER="receiver@email.com"
python3 scanner.py
```

---

## Disclaimer

This is not financial advice. This bot is for educational purposes only. Always do your own research before making investment decisions.
