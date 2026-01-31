"""
Configuration for the Personal Hedge Fund Scanner
Buffett-Style Value Investing + RSI Dip Detection
"""

# =============================================================================
# WATCHLIST - Global Blue Chips (200+ Stocks)
# =============================================================================

# S&P 500 (US Large Caps) - Top 50
SP500 = [
    # Tech Giants
    "AAPL",     # Apple
    "MSFT",     # Microsoft
    "GOOGL",    # Alphabet
    "AMZN",     # Amazon
    "META",     # Meta (Facebook)
    "NVDA",     # NVIDIA
    "TSLA",     # Tesla
    "AVGO",     # Broadcom
    "ORCL",     # Oracle
    "CRM",      # Salesforce
    "ADBE",     # Adobe
    "AMD",      # AMD
    "INTC",     # Intel
    "CSCO",     # Cisco
    "IBM",      # IBM
    "QCOM",     # Qualcomm
    "TXN",      # Texas Instruments
    "NOW",      # ServiceNow
    "INTU",     # Intuit
    "AMAT",     # Applied Materials

    # Finance
    "BRK-B",    # Berkshire Hathaway
    "JPM",      # JPMorgan Chase
    "V",        # Visa
    "MA",       # Mastercard
    "BAC",      # Bank of America
    "WFC",      # Wells Fargo
    "GS",       # Goldman Sachs
    "MS",       # Morgan Stanley
    "BLK",      # BlackRock
    "SCHW",     # Charles Schwab
    "AXP",      # American Express
    "C",        # Citigroup
    "USB",      # US Bancorp
    "PNC",      # PNC Financial
    "TFC",      # Truist

    # Healthcare
    "JNJ",      # Johnson & Johnson
    "UNH",      # UnitedHealth
    "PFE",      # Pfizer
    "ABBV",     # AbbVie
    "MRK",      # Merck
    "LLY",      # Eli Lilly
    "TMO",      # Thermo Fisher
    "ABT",      # Abbott
    "DHR",      # Danaher
    "BMY",      # Bristol-Myers
    "AMGN",     # Amgen
    "GILD",     # Gilead
    "ISRG",     # Intuitive Surgical
    "VRTX",     # Vertex Pharma
    "REGN",     # Regeneron
    "MDT",      # Medtronic
    "SYK",      # Stryker
    "ZTS",      # Zoetis
    "CI",       # Cigna
    "ELV",      # Elevance Health

    # Consumer
    "PG",       # Procter & Gamble
    "KO",       # Coca-Cola
    "PEP",      # PepsiCo
    "COST",     # Costco
    "WMT",      # Walmart
    "HD",       # Home Depot
    "MCD",      # McDonald's
    "NKE",      # Nike
    "SBUX",     # Starbucks
    "TGT",      # Target
    "LOW",      # Lowe's
    "TJX",      # TJX Companies
    "EL",       # Estee Lauder
    "CL",       # Colgate-Palmolive
    "KMB",      # Kimberly-Clark
    "GIS",      # General Mills
    "K",        # Kellanova
    "HSY",      # Hershey
    "MDLZ",     # Mondelez
    "KHC",      # Kraft Heinz

    # Industrial
    "CAT",      # Caterpillar
    "DE",       # Deere & Co
    "UNP",      # Union Pacific
    "RTX",      # RTX Corp
    "HON",      # Honeywell
    "BA",       # Boeing
    "LMT",      # Lockheed Martin
    "GE",       # GE Aerospace
    "MMM",      # 3M
    "UPS",      # UPS
    "FDX",      # FedEx
    "EMR",      # Emerson
    "ITW",      # Illinois Tool Works
    "ETN",      # Eaton
    "PH",       # Parker Hannifin

    # Energy
    "XOM",      # Exxon Mobil
    "CVX",      # Chevron
    "COP",      # ConocoPhillips
    "SLB",      # Schlumberger
    "EOG",      # EOG Resources
    "PSX",      # Phillips 66
    "VLO",      # Valero
    "MPC",      # Marathon Petroleum
    "OXY",      # Occidental
    "HAL",      # Halliburton

    # Media & Entertainment
    "DIS",      # Disney
    "NFLX",     # Netflix
    "CMCSA",    # Comcast
    "WBD",      # Warner Bros Discovery
    "PARA",     # Paramount
    "EA",       # Electronic Arts
    "TTWO",     # Take-Two

    # Telecom
    "T",        # AT&T
    "VZ",       # Verizon
    "TMUS",     # T-Mobile
]

# DAX 40 (German Large Caps)
DAX = [
    "SAP.DE",       # SAP
    "SIE.DE",       # Siemens
    "ALV.DE",       # Allianz
    "DTE.DE",       # Deutsche Telekom
    "MBG.DE",       # Mercedes-Benz
    "BMW.DE",       # BMW
    "BAS.DE",       # BASF
    "MUV2.DE",      # Munich Re
    "ADS.DE",       # Adidas
    "DB1.DE",       # Deutsche Börse
    "VOW3.DE",      # Volkswagen
    "IFX.DE",       # Infineon
    "DHL.DE",       # DHL Group
    "AIR.DE",       # Airbus
    "SHL.DE",       # Siemens Healthineers
    "RWE.DE",       # RWE
    "BAYN.DE",      # Bayer
    "HEN3.DE",      # Henkel
    "CON.DE",       # Continental
    "HEI.DE",       # HeidelbergCement
    "FRE.DE",       # Fresenius
    "MTX.DE",       # MTU Aero Engines
    "ENR.DE",       # Siemens Energy
    "SY1.DE",       # Symrise
    "QIA.DE",       # Qiagen
    "MRK.DE",       # Merck KGaA
    "BEI.DE",       # Beiersdorf
    "VNA.DE",       # Vonovia
    "1COV.DE",      # Covestro
    "ZAL.DE",       # Zalando
    "PAH3.DE",      # Porsche Auto Holding
    "P911.DE",      # Porsche AG
    "RHM.DE",       # Rheinmetall
    "HNR1.DE",      # Hannover Rück
    "CBK.DE",       # Commerzbank
    "DBK.DE",       # Deutsche Bank
]

# MDAX (German Mid Caps)
MDAX = [
    "AFX.DE",       # Carl Zeiss Meditec
    "PUM.DE",       # Puma
    "LEG.DE",       # LEG Immobilien
    "EVK.DE",       # Evonik
    "FME.DE",       # Fresenius Medical Care
    "TLX.DE",       # Talanx
    "GXI.DE",       # Gerresheimer
    "BOSS.DE",      # Hugo Boss
    "RAA.DE",       # Rational
    "KGX.DE",       # Kion Group
    "NDA.DE",       # Aurubis
    "WAF.DE",       # Siltronic
    "EVD.DE",       # CTS Eventim
    "AIXA.DE",      # Aixtron
    "LXS.DE",       # Lanxess
    "TEG.DE",       # TAG Immobilien
    "DEQ.DE",       # Deutsche EuroShop
    "HAG.DE",       # Hensoldt
    "G1A.DE",       # GEA Group
    "DUE.DE",       # Dürr
]

# SDAX (German Small Caps)
SDAX = [
    "NEM.DE",       # Nemetschek
    "BC8.DE",       # Bechtle
    "FNTN.DE",      # Freenet
    "JEN.DE",       # Jenoptik
    "SFQ.DE",       # SAF-Holland
    "HHFA.DE",      # Hamburger Hafen
    "DHER.DE",      # Delivery Hero
    "S92.DE",       # SMA Solar
    "BNR.DE",       # Brenntag
    "SZG.DE",       # Salzgitter
]

# CAC 40 (French Large Caps)
CAC40 = [
    "MC.PA",        # LVMH
    "OR.PA",        # L'Oreal
    "TTE.PA",       # TotalEnergies
    "SAN.PA",       # Sanofi
    "AI.PA",        # Air Liquide
    "SU.PA",        # Schneider Electric
    "BN.PA",        # Danone
    "KER.PA",       # Kering
    "RMS.PA",       # Hermes
    "AIR.PA",       # Airbus
    "CS.PA",        # AXA
    "BNP.PA",       # BNP Paribas
    "GLE.PA",       # Societe Generale
    "CA.PA",        # Carrefour
    "CAP.PA",       # Capgemini
    "EN.PA",        # Bouygues
    "RI.PA",        # Pernod Ricard
    "VIV.PA",       # Vivendi
    "ORA.PA",       # Orange
    "PUB.PA",       # Publicis
    "DSY.PA",       # Dassault Systemes
    "STM.PA",       # STMicroelectronics
    "SGO.PA",       # Saint-Gobain
]

# FTSE 100 (UK Large Caps)
FTSE100 = [
    "SHEL.L",       # Shell
    "AZN.L",        # AstraZeneca
    "HSBA.L",       # HSBC
    "ULVR.L",       # Unilever
    "BP.L",         # BP
    "GSK.L",        # GSK
    "RIO.L",        # Rio Tinto
    "DGE.L",        # Diageo
    "BATS.L",       # BAT
    "REL.L",        # RELX
    "LSEG.L",       # London Stock Exchange
    "LLOY.L",       # Lloyds Bank
    "BARC.L",       # Barclays
    "VOD.L",        # Vodafone
    "NG.L",         # National Grid
    "RKT.L",        # Reckitt Benckiser
    "PRU.L",        # Prudential
    "AAL.L",        # Anglo American
    "BT-A.L",       # BT Group
    "BA.L",         # BAE Systems
    "RR.L",         # Rolls-Royce
    "IMB.L",        # Imperial Brands
    "ANTO.L",       # Antofagasta
    "CPG.L",        # Compass Group
    "EXPN.L",       # Experian
]

# AEX (Dutch Large Caps)
AEX = [
    "ASML.AS",      # ASML
    "SHELL.AS",     # Shell (also listed)
    "UNA.AS",       # Unilever
    "PRX.AS",       # Prosus
    "HEIA.AS",      # Heineken
    "INGA.AS",      # ING Group
    "AD.AS",        # Ahold Delhaize
    "DSM.AS",       # DSM-Firmenich
    "PHIA.AS",      # Philips
    "WKL.AS",       # Wolters Kluwer
    "ASM.AS",       # ASM International
    "RAND.AS",      # Randstad
    "ABN.AS",       # ABN AMRO
    "KPN.AS",       # KPN
    "AKZA.AS",      # Akzo Nobel
]

# SMI (Swiss Large Caps)
SMI = [
    "NESN.SW",      # Nestle
    "NOVN.SW",      # Novartis
    "ROG.SW",       # Roche
    "UBSG.SW",      # UBS
    "CSGN.SW",      # Credit Suisse (now UBS)
    "ABBN.SW",      # ABB
    "ZURN.SW",      # Zurich Insurance
    "SREN.SW",      # Swiss Re
    "LONN.SW",      # Lonza
    "GIVN.SW",      # Givaudan
    "SIKA.SW",      # Sika
    "CFR.SW",       # Richemont
    "GEBN.SW",      # Geberit
    "SLHN.SW",      # Swiss Life
    "SCMN.SW",      # Swisscom
]

# Nikkei 225 (Japan Large Caps) - Top 30
JAPAN = [
    "7203.T",       # Toyota
    "6758.T",       # Sony
    "9984.T",       # SoftBank Group
    "6861.T",       # Keyence
    "8306.T",       # Mitsubishi UFJ
    "6501.T",       # Hitachi
    "7267.T",       # Honda
    "4502.T",       # Takeda Pharma
    "9433.T",       # KDDI
    "6902.T",       # Denso
    "6098.T",       # Recruit Holdings
    "4063.T",       # Shin-Etsu Chemical
    "8035.T",       # Tokyo Electron
    "6367.T",       # Daikin
    "6954.T",       # Fanuc
    "7741.T",       # Hoya
    "4519.T",       # Chugai Pharma
    "6273.T",       # SMC Corp
    "7751.T",       # Canon
    "4661.T",       # Oriental Land (Disney Japan)
    "9432.T",       # NTT
    "6594.T",       # Nidec
    "8001.T",       # Itochu
    "8058.T",       # Mitsubishi Corp
    "8031.T",       # Mitsui & Co
    "6981.T",       # Murata Manufacturing
    "7974.T",       # Nintendo
    "6762.T",       # TDK
    "4543.T",       # Terumo
    "6971.T",       # Kyocera
]

# KOSPI (South Korea Large Caps)
KOREA = [
    "005930.KS",    # Samsung Electronics
    "000660.KS",    # SK Hynix
    "207940.KS",    # Samsung Biologics
    "005380.KS",    # Hyundai Motor
    "051910.KS",    # LG Chem
    "006400.KS",    # Samsung SDI
    "035420.KS",    # Naver
    "035720.KS",    # Kakao
    "068270.KS",    # Celltrion
    "003670.KS",    # Posco Holdings
    "105560.KS",    # KB Financial
    "055550.KS",    # Shinhan Financial
    "012330.KS",    # Hyundai Mobis
    "028260.KS",    # Samsung C&T
    "000270.KS",    # Kia
]

# Hang Seng (Hong Kong) & China ADRs
CHINA = [
    # US ADRs
    "BABA",         # Alibaba
    "JD",           # JD.com
    "PDD",          # PDD Holdings
    "BIDU",         # Baidu
    "NIO",          # NIO
    "XPEV",         # XPeng
    "LI",           # Li Auto
    "NTES",         # NetEase
    "TME",          # Tencent Music
    "BILI",         # Bilibili
    "TAL",          # TAL Education
    "ZTO",          # ZTO Express
    "YUMC",         # Yum China
    "MNSO",         # Miniso
    "FUTU",         # Futu Holdings

    # Hong Kong Listed
    "0700.HK",      # Tencent
    "9988.HK",      # Alibaba HK
    "3690.HK",      # Meituan
    "1211.HK",      # BYD
    "2318.HK",      # Ping An Insurance
    "0941.HK",      # China Mobile
    "1398.HK",      # ICBC
    "3988.HK",      # Bank of China
    "0939.HK",      # CCB
    "2628.HK",      # China Life
    "0883.HK",      # CNOOC
    "1810.HK",      # Xiaomi
    "9618.HK",      # JD.com HK
    "9999.HK",      # NetEase HK
    "2020.HK",      # Anta Sports
    "9888.HK",      # Baidu HK
    "1024.HK",      # Kuaishou
    "0388.HK",      # HKEX
    "0005.HK",      # HSBC HK
    "0011.HK",      # Hang Seng Bank
]

# ASX 200 (Australia Large Caps)
AUSTRALIA = [
    "BHP.AX",       # BHP Group
    "CBA.AX",       # Commonwealth Bank
    "CSL.AX",       # CSL Limited
    "NAB.AX",       # National Australia Bank
    "WBC.AX",       # Westpac
    "ANZ.AX",       # ANZ Bank
    "WES.AX",       # Wesfarmers
    "MQG.AX",       # Macquarie Group
    "WDS.AX",       # Woodside Energy
    "TLS.AX",       # Telstra
    "RIO.AX",       # Rio Tinto
    "FMG.AX",       # Fortescue Metals
    "WOW.AX",       # Woolworths
    "ALL.AX",       # Aristocrat Leisure
    "TCL.AX",       # Transurban
]

# India ADRs (US Listed)
INDIA = [
    "INFY",         # Infosys
    "WIT",          # Wipro
    "HDB",          # HDFC Bank
    "IBN",          # ICICI Bank
    "SIFY",         # Sify Technologies
    "TTM",          # Tata Motors
    "RDY",          # Dr. Reddy's
    "VEDL",         # Vedanta
    "WNS",          # WNS Holdings
]

# Nordic Stocks (Sweden, Denmark, Norway, Finland)
NORDIC = [
    # Sweden (OMX Stockholm)
    "ERIC-B.ST",    # Ericsson
    "VOLV-B.ST",    # Volvo
    "ATCO-B.ST",    # Atlas Copco
    "INVE-B.ST",    # Investor AB
    "SEB-A.ST",     # SEB
    "SAND.ST",      # Sandvik
    "HM-B.ST",      # H&M
    "ABB.ST",       # ABB Sweden
    "SWED-A.ST",    # Swedbank
    "ALFA.ST",      # Alfa Laval

    # Denmark (OMX Copenhagen)
    "NOVO-B.CO",    # Novo Nordisk
    "MAERSK-B.CO",  # Maersk
    "DSV.CO",       # DSV
    "CARL-B.CO",    # Carlsberg
    "VWS.CO",       # Vestas Wind
    "ORSTED.CO",    # Orsted
    "COLO-B.CO",    # Coloplast
    "DEMANT.CO",    # Demant

    # Norway (Oslo)
    "EQNR.OL",      # Equinor
    "DNB.OL",       # DNB Bank
    "TEL.OL",       # Telenor
    "MOWI.OL",      # Mowi (salmon)
    "YAR.OL",       # Yara International

    # Finland (Helsinki)
    "NOKIA.HE",     # Nokia
    "FORTUM.HE",    # Fortum
    "NESTE.HE",     # Neste
    "UPM.HE",       # UPM-Kymmene
    "STERV.HE",     # Stora Enso
]

# Spanish & Italian Large Caps
SOUTHERN_EUROPE = [
    # Spain (IBEX 35)
    "SAN.MC",       # Banco Santander
    "BBVA.MC",      # BBVA
    "ITX.MC",       # Inditex (Zara)
    "IBE.MC",       # Iberdrola
    "TEF.MC",       # Telefonica
    "REP.MC",       # Repsol
    "CABK.MC",      # CaixaBank
    "FER.MC",       # Ferrovial

    # Italy (FTSE MIB)
    "ENI.MI",       # Eni
    "ENEL.MI",      # Enel
    "ISP.MI",       # Intesa Sanpaolo
    "UCG.MI",       # UniCredit
    "G.MI",         # Generali
    "STM.MI",       # STMicroelectronics
    "RACE.MI",      # Ferrari
    "LUX.MI",       # Luxottica (EssilorLuxottica)
]

# Canadian Large Caps (TSX)
CANADA = [
    "RY.TO",        # Royal Bank of Canada
    "TD.TO",        # TD Bank
    "BNS.TO",       # Bank of Nova Scotia
    "ENB.TO",       # Enbridge
    "CNR.TO",       # CN Railway
    "CP.TO",        # CP Railway
    "BMO.TO",       # Bank of Montreal
    "SU.TO",        # Suncor Energy
    "TRP.TO",       # TC Energy
    "BCE.TO",       # BCE Inc
    "CNQ.TO",       # Canadian Natural Resources
    "SHOP.TO",      # Shopify
    "MFC.TO",       # Manulife
    "ATD.TO",       # Alimentation Couche-Tard
    "NTR.TO",       # Nutrien
]

# =============================================================================
# COMBINED WATCHLIST
# =============================================================================

WATCHLIST = (
    SP500 +
    DAX +
    MDAX +
    SDAX +
    CAC40 +
    FTSE100 +
    AEX +
    SMI +
    JAPAN +
    KOREA +
    CHINA +
    AUSTRALIA +
    INDIA +
    NORDIC +
    SOUTHERN_EUROPE +
    CANADA
)

# Remove duplicates while preserving order
WATCHLIST = list(dict.fromkeys(WATCHLIST))

# =============================================================================
# STRATEGY PARAMETERS
# =============================================================================

# Technical Indicator - The Dip
RSI_PERIOD = 14
RSI_OVERSOLD = 30           # Buy signal when RSI drops below this

# Buffett-Style Value Filters
MAX_FORWARD_PE = 25         # Reasonable earnings valuation
MAX_PRICE_TO_BOOK = 3       # Not overpaying for assets
MIN_ROE = 0.10              # 10% - Quality business (OR revenue growth)
MIN_REVENUE_GROWTH = 0.05   # 5% - Alternative to ROE for growth companies
MAX_DEBT_TO_EQUITY = 1.0    # Conservative balance sheet

# Email Settings
EMAIL_SUBJECT = "🚨 Buy the Dip Alert - Personal Hedge Fund"
