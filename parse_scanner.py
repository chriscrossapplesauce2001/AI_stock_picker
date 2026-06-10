"""Parse scanner_output_2026-06-01.txt into structured markdown tables per missed-count bucket."""
import re
import sys
from collections import defaultdict


def parse(path):
    with open(path, encoding="utf-8") as f:
        txt = f.read()

    blocks = re.findall(
        r"Analyzing (\S+)\.\.\.\n"
        r"\s+(.+?)\n"
        r"\s+Sector: (.+?)\n"
        r"\s+Price: \$([0-9.]+)\n"
        r"\s+200-day MA: \$([0-9.]+) \((ABOVE|BELOW)\)\n"
        r"\s+RSI\(14\): ([0-9.]+)\n"
        r"\s+Trailing P/E: (.+?)\n"
        r"\s+Price/Book: (.+?)\n"
        r"\s+ROE: (.+?)\n"
        r"\s+Revenue Growth: (.+?)\n"
        r"\s+Debt/Equity: (.+?)\n"
        r"\s+(?:✅ SIGNAL TRIGGERED! Missed: (\d+)/(\d+)|❌ No signal \(missed (\d+)/(\d+)\): .+?)\n",
        txt,
    )

    results = []
    for m in blocks:
        (ticker, name, sector, price, ma, ma_dir, rsi, pe, pb, roe, growth, de,
         sig_m, sig_t, fail_m, fail_t) = m
        missed = int(sig_m) if sig_m else int(fail_m)
        total = int(sig_t) if sig_t else int(fail_t)
        results.append({
            "ticker": ticker,
            "name": name.strip(),
            "sector": sector.strip(),
            "price": float(price),
            "ma": float(ma),
            "ma_dir": ma_dir,
            "rsi": float(rsi),
            "pe": pe.strip(),
            "pb": pb.strip(),
            "roe": roe.strip(),
            "growth": growth.strip(),
            "de": de.strip(),
            "missed": missed,
            "total": total,
        })
    return results


def light(val_str, thresh, op, exempt=False):
    """Return colored circle for a metric value vs. threshold."""
    if exempt or val_str in ("N/A", ""):
        return "⚪"
    s = val_str.replace("%", "").replace("[exempt]", "").strip()
    try:
        v = float(s)
    except ValueError:
        return "⚪"
    margin = abs(thresh) * 0.15 if thresh else 5
    if op == "<":
        if v < thresh:
            return "🟢" if (thresh - v) >= margin else "🟠"
        return "🔴"
    if op == ">":
        if v > thresh:
            return "🟢" if (v - thresh) >= margin else "🟠"
        return "🔴"
    return "⚪"


def fmt_row(r):
    rsi_l = light(f"{r['rsi']:.1f}", 30, "<")
    ma_l = "🟢" if r["ma_dir"] == "ABOVE" else "🔴"
    pe_exempt = "[exempt]" in r["pe"]
    pb_exempt = "[exempt]" in r["pb"]
    de_exempt = "[exempt]" in r["de"]
    pe_l = light(r["pe"], 25, "<", pe_exempt)
    pb_l = light(r["pb"], 3, "<", pb_exempt)
    roe_l = light(r["roe"], 10, ">")
    g_l = light(r["growth"], 5, ">")
    de_l = light(r["de"], 100, "<", de_exempt)

    return (
        f"| {r['ticker']} | ${r['price']:.2f} | {rsi_l} {r['rsi']:.1f} | "
        f"{ma_l} ${r['ma']:.2f} | {pe_l} {r['pe']} | {pb_l} {r['pb']} | "
        f"{roe_l} {r['roe']} | {g_l} {r['growth']} | {de_l} {r['de']} | "
        f"{r['sector']} |"
    )


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "scanner_output_2026-06-01.txt"
    data = parse(path)
    buckets = defaultdict(list)
    for r in data:
        buckets[r["missed"]].append(r)

    out = []
    out.append("## Full Scanner Data (417 stocks)\n")
    out.append(
        "Legend: 🟢 passes / 🟠 borderline / 🔴 fails / ⚪ exempt or N/A. "
        "RSI<30 pass; Price>200MA pass; P/E<25 pass; P/B<3 pass; "
        "ROE>10% pass; Growth>5% pass; D/E<100% pass.\n"
    )

    headers = (
        "| Ticker | Price | RSI | 200d MA | P/E | P/B | ROE | Growth | D/E | Sector |"
    )
    sep = "|--------|-------|-----|---------|-----|-----|-----|--------|-----|--------|"

    for missed in sorted(buckets.keys()):
        rows = sorted(buckets[missed], key=lambda x: x["rsi"])
        label = "SIGNALS" if missed == 0 else f"Near-Misses" if missed == 1 else ""
        title = f"### Missed {missed}"
        if label:
            title += f" -- {label}"
        title += f" ({len(rows)} stocks)\n"
        out.append(title)
        out.append(headers)
        out.append(sep)
        for r in rows:
            out.append(fmt_row(r))
        out.append("")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
