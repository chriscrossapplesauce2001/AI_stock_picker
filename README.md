# Personal Hedge Fund Bot 🤖📈

A stock scanner monitoring **417 global stocks** across 16 markets for "Buy the Dip" opportunities using Buffett-style value investing.

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the scanner
python3 scanner.py
```

---

## Strategy

The bot signals when **ALL criteria** are met:

| Indicator | Threshold | Purpose |
|-----------|-----------|---------|
| RSI(14) | < 30 | Identifies oversold stocks (the dip) |
| Forward P/E | < 25 | Reasonable earnings valuation |
| Price/Book | < 3 | Not overpaying for assets |
| ROE | > 10% | Quality business |
| Revenue Growth | > 5% | *OR* Growth alternative to ROE |
| Debt/Equity | < 100% | Conservative balance sheet |

---

## Watchlist (417 Stocks)

| Market | Count | Examples |
|--------|-------|----------|
| 🇺🇸 S&P 500 | 107 | AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA, JPM, V, JNJ... |
| 🇩🇪 DAX | 36 | SAP, Siemens, Allianz, Mercedes, BMW, Porsche, Rheinmetall... |
| 🇩🇪 MDAX/SDAX | 30 | Carl Zeiss, Puma, Hugo Boss, Delivery Hero, Aixtron... |
| 🇫🇷 CAC 40 | 23 | LVMH, L'Oreal, Hermes, Kering, TotalEnergies, Sanofi... |
| 🇬🇧 FTSE 100 | 25 | Shell, AstraZeneca, HSBC, Unilever, BP, Rolls-Royce... |
| 🇳🇱 AEX | 15 | ASML, Heineken, ING, Philips, Akzo Nobel... |
| 🇨🇭 SMI | 15 | Nestle, Novartis, Roche, UBS, Richemont, Sika... |
| 🇯🇵 Nikkei | 30 | Toyota, Sony, Nintendo, Keyence, SoftBank, Honda... |
| 🇰🇷 KOSPI | 15 | Samsung, SK Hynix, Hyundai, Naver, Kakao, LG Chem... |
| 🇨🇳 China/HK | 35 | Alibaba, Tencent, BYD, PDD, JD, Xiaomi, Meituan... |
| 🇦🇺 ASX | 15 | BHP, Commonwealth Bank, CSL, Rio Tinto, Fortescue... |
| 🇮🇳 India ADRs | 9 | Infosys, HDFC Bank, ICICI, Tata Motors, Wipro... |
| 🇸🇪🇩🇰🇳🇴🇫🇮 Nordic | 23 | Novo Nordisk, Ericsson, Volvo, Maersk, Equinor, Nokia... |
| 🇪🇸🇮🇹 Southern EU | 16 | Santander, Inditex, Ferrari, Enel, UniCredit... |
| 🇨🇦 TSX | 15 | Royal Bank, TD, Shopify, Enbridge, CN Railway... |

Edit `config.py` to customize your watchlist.

---

## Output

The scanner generates a table with color-coded indicators:

| Symbol | Meaning |
|--------|---------|
| 🟢 | Good — passes threshold |
| 🟠 | Borderline — close to threshold |
| 🔴 | Bad — fails threshold |

Example output:
```
🚨 SIGNALS TRIGGERED:
   • AFX.DE @ €28.00
     RSI: 17.6 | P/E: 13.0 | P/B: 1.2
     ROE: 6.8% | Growth: 8.3% | D/E: 25%
   • PDD @ €85.25
     RSI: 24.2 | P/E: 8.1 | P/B: 2.5
     ROE: 30.5% | Growth: 9.0% | D/E: 3%
```

---

## 🔥 Hedge Fund Stress Test

**After the scanner identifies a dip, run each signal through this brutal 5-question test.**

Play the role of a cynical, ruthless hedge fund manager. Your job is capital preservation. Stress-test every trade before buying.

### 1. The "Falling Knife" Test (Structural vs. Cyclical)

> *"Is the stock down because of a temporary macro issue (e.g., interest rates, supply chain) or a permanent structural problem (e.g., nobody buys this product anymore)?"*

**Ask yourself:**
- Is this a Nokia/Kodak situation where the core business is dying?
- Or is it a temporary setback like COVID supply chains or interest rate sensitivity?
- If there's even a 10% chance this is structural decline, **walk away**.

### 2. The "20-Year Survival" Stress Test

> *"Imagine it is the year 2046. This company has gone bankrupt. Write a pre-mortem explaining exactly HOW it died."*

**Consider:**
- What competitor could kill them? (e.g., Amazon killed retail)
- What technology shift could make them obsolete? (e.g., EVs killed combustion)
- What lawsuit or regulation could destroy them? (e.g., tobacco litigation)
- Be creative and specific about the killer.

### 3. The "Moat" Integrity Check

> *"Does this company still have pricing power? If they raised prices by 10% tomorrow, would customers stay or leave?"*

**Compare to top 2 competitors:**
- Can they raise prices without losing customers?
- Do they have brand loyalty, network effects, or switching costs?
- Or are they competing purely on price (commodity business)?

### 4. The Valuation Trap

> *"Is the stock actually 'cheap' relative to its own 10-year history, or is the 'E' in P/E about to collapse?"*

**Check:**
- Is the low P/E because earnings are about to crater?
- Are margins compressing?
- Is revenue declining?
- A stock can look cheap right before it gets cheaper.

### 5. The Verdict

> *"Based only on the risks above, rate this dip:"*

| Rating | Meaning |
|--------|---------|
| **A) Golden Opportunity** | Market is wrong, business is fundamentally sound |
| **B) Value Trap** | Stock is cheap for a good reason — stay away |
| **C) Wait & See** | Too much uncertainty, let the dust settle |

**Include a confidence score (0-100%).**

---

## Workflow

```
┌─────────────────────────────────────────────────────────┐
│  1. RUN SCANNER                                         │
│     python3 scanner.py                                  │
│     → Generates list of stocks meeting criteria         │
├─────────────────────────────────────────────────────────┤
│  2. REVIEW SIGNALS                                      │
│     → Check RSI, P/E, P/B, ROE, Growth, D/E            │
│     → Sort by most green indicators                     │
├─────────────────────────────────────────────────────────┤
│  3. STRESS TEST (for each signal)                       │
│     → Falling Knife Test: Structural or cyclical?       │
│     → 20-Year Survival: How could it die?               │
│     → Moat Check: Does it have pricing power?           │
│     → Valuation Trap: Is the "E" collapsing?            │
│     → Verdict: A, B, or C?                              │
├─────────────────────────────────────────────────────────┤
│  4. DECISION                                            │
│     → Only buy "A" rated opportunities                  │
│     → Position size based on confidence score           │
└─────────────────────────────────────────────────────────┘
```

---

## Customization

Edit `config.py` to adjust:

```python
# Thresholds
RSI_OVERSOLD = 30           # Lower = stricter dip detection
MAX_FORWARD_PE = 25         # Lower = cheaper stocks only
MAX_PRICE_TO_BOOK = 3       # Lower = more asset-focused
MIN_ROE = 0.10              # Higher = quality only
MIN_REVENUE_GROWTH = 0.05   # Higher = growth only
MAX_DEBT_TO_EQUITY = 1.0    # Lower = safer balance sheets
```

---

## Project Structure

```
.
├── config.py             # Watchlist (417 stocks) & strategy parameters
├── scanner.py            # Main scanning logic
├── manager.txt           # Hedge fund stress test questions
├── requirements.txt      # Python dependencies
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

## Optional: GitHub Actions (Automated Daily Scans)

The `.github/workflows/scan.yml` file can run the scanner automatically Monday-Friday at 21:00 UTC.

To enable:
1. Push to GitHub
2. Add secrets: `EMAIL_SENDER`, `EMAIL_PASSWORD`, `EMAIL_RECEIVER`
3. Enable Actions in your repo settings

---

## Disclaimer

⚠️ **This is not financial advice.** This bot is for educational purposes only. Always do your own research before making investment decisions. Past performance does not guarantee future results.
