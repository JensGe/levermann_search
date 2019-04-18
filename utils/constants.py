# Scraping Settings
SHORT_WAIT = 1  # Seconds
LONG_WAIT = 4  # Seconds
RANDOM_WAIT_RANGE = 0.8  # Seconds

# Parser Settings
PARSER = "html.parser"

# Selenium Driver Settings
SELENIUM_SETTINGS = "utils/driver_host_rules.txt"

# Base Scraping URLs
URL_INDEX_CONTENT = "https://www.boerse-online.de/index/liste/"
URL_INDEX_HISTORY = "https://www.boerse-online.de/index/historisch/"
URL_STOCK_HISTORY = "https://www.boerse-online.de/kurse/historisch/"
URL_STOCK_OVERVIEW = "https://www.boerse-online.de/aktie/"
URL_STOCK_BALANCE = "https://www.boerse-online.de/bilanz_guv/"
URL_STOCK_TARGETS = "https://www.boerse-online.de/kursziele/"
URL_STOCK_DATES = "https://www.boerse-online.de/termine/uebersicht/"
URL_STOCK_ESTIMATES = "https://www.boerse-online.de/schaetzungen/"

URL_STOCK_HISTORY_EXT = ""
URL_STOCK_OVERVIEW_EXT = "-aktie"
URL_STOCK_BALANCE_EXT = ""
URL_STOCK_TARGETS_EXT = ""
URL_STOCK_DATES_EXT = ""
URL_STOCK_ESTIMATES_EXT = ""

EXCHANGE_APPENDIX = "FSE"

# Scraping Parts
NO_DATA_AVAILABLE = "Keine Daten verfügbar"
NO_DATA_AVAILABLE_LONG = "Zu diesem Datensatz liegen uns leider keine Daten vor."

TEXT_BYGONE_DATES = "vergangene Termine"
TEXT_FUTURE_DATES = "Termine"

TEXT_EPS_UNDILUTED = "Ergebnis je Aktie unverwässert"
TEXT_EPS = "Ergebnis/Aktie"
TEXT_MARKET_CAP = "Marktkapitalisierung in Euro"
TEXT_MARKET_PLACE = "Börsenplatz:"
TEXT_LISTED_INDIZES = "Zur Aktie"
TEXT_COMPANY_INFO = "Zum Unternehmen"
TEXT_RESULT_AFTER_TAX = "Ergebnis nach Steuer"
TEXT_OPERATIVE_RESULT = "Operatives Ergebnis"
TEXT_SALES_REVENUE = "Umsatzerlöse"
TEXT_BALANCE = "Bilanzsumme"
TEXT_EQUITY_CAPITAL = "Eigenkapital"
TEXT_HISTORIC_PRICES = "Historische Kurse"

# HTML Attributes
TEXT_HISTORIC_RATING = "historicRatingTdContent"
HISTORIC_PRICE_LIST = "historic-price-list"
TEXT_TEXT_RIGHT = "text-right"
TEXT_INDEX_LIST_CONTAINER = "index-list-container"
TEXT_PAGINATION = "finando_paging"


# HTML Elements
HTML_H1 = "h1"
HTML_H2 = "h2"
HTML_TD = "td"
HTML_TR = "tr"
HTML_DIV = "div"
HTML_A = "a"
HTML_CLASS = "class"
HTML_ID = "id"
HTML_SPAN = "span"
HTML_HREF = "href"


# Local Paths
PATH_INDEX_CONTENT = "data/indizes/content/"
PATH_INDEX_HISTORY = "data/indizes/history/"
PATH_STOCK_HISTORY = "data/stocks/history/"
PATH_STOCK_OVERVIEW = "data/stocks/overview/"
PATH_STOCK_BALANCE = "data/stocks/balance/"
PATH_STOCK_TARGETS = "data/stocks/targets/"
PATH_STOCK_DATES = "data/stocks/dates/"
PATH_STOCK_ESTIMATES = "data/stocks/estimates/"


# File Extensions
HTML_EXTENSION = ".html"


# Database
DATABASE = "mysql://root:toor@localhost/levermann"
TEST_DATABASE = "mysql://root:toor@localhost/levermann_test"


# Database Tables
TABLE_INDIZES = "Aktienindizes"
TABLE_INDEX_HISTORIES = "Indexhistorien"
TABLE_STOCKS = "Aktien"
TABLE_STOCKS_HISTORIES = "Aktienhistorien"
TABLE_STOCK_DATES = "Aktientermine"
TABLE_INDEX_CONTENTS = "Indexinhalte"
TABLE_COMPANY_DATA = "Unternehmensdaten"
TABLE_LEVERMANN = "Levermannscores"

VIEW_LEVERMANN_BUY = "Levermann_Latest_Buy"
VIEW_LEVERMANN_HOLD = "Levermann_Latest_Hold"


# Database Columns
COLUMN_URI = "URI"
COLUMN_ACTIVE = "Aktiv"
COLUMN_LARGECAP = "Large_Cap_Index"
COLUMN_INDEX_URI = "IndexURI"
COLUMN_INDEX_NAME = "Name"
COLUMN_PAGES = "Seiten"
COLUMN_STOCK_URI = "AktienURI"
COLUMN_EARNINGS_AT = "Ergebnis_nach_Steuern"
COLUMN_EQUITY_CAPITAL = "Eigenkapital"
COLUMN_OPERATIVE_RESULT = "Operatives_Ergebnis"
COLUMN_SALES_REVENUE = "Umsatzerloese"
COLUMN_BALANCE = "Bilanzsumme"
COLUMN_START_VALUE = "Eroeffnungswert"
COLUMN_CLOSING_VALUE = "Schlusswert"
COLUMN_EPS_M3 = "EPS_minus_3"
COLUMN_EPS_M2 = "EPS_minus_2"
COLUMN_EPS_M1 = "EPS_minus_1"
COLUMN_EPS_0 = "EPS_0"
COLUMN_EPS_P1 = "EPS_plus_1"
COLUMN_ANALYST_BUY = "Analysten_Buy"
COLUMN_ANALYST_HOLD = "Analysten_Hold"
COLUMN_ANALYST_SELL = "Analysten_Sell"
COLUMN_MARKET_CAP = "Marktkapitalisierung"
COLUMN_MARKET_PLACE = "Handelsplatz"
COLUMN_DATE = "Datum"
COLUMN_QUARTERLY = "Terminart"
COLUMN_SECTORS = "Branchen"
COLUMN_INDICES = "Indizes"
COLUMN_LEV01_VALUE = "Lev01_Wert"
COLUMN_LEV01_SCORE = "Lev01_Score"
COLUMN_LEV02_VALUE = "Lev02_Wert"
COLUMN_LEV02_SCORE = "Lev02_Score"
COLUMN_LEV03_VALUE = "Lev03_Wert"
COLUMN_LEV03_SCORE = "Lev03_Score"
COLUMN_LEV04_VALUE = "Lev04_Wert"
COLUMN_LEV04_SCORE = "Lev04_Score"
COLUMN_LEV05_VALUE = "Lev05_Wert"
COLUMN_LEV05_SCORE = "Lev05_Score"
COLUMN_LEV06_VALUE = "Lev06_Wert"
COLUMN_LEV06_SCORE = "Lev06_Score"
COLUMN_LEV07_VALUE = "Lev07_Wert"
COLUMN_LEV07_SCORE = "Lev07_Score"
COLUMN_LEV08_VALUE = "Lev08_Wert"
COLUMN_LEV08_SCORE = "Lev08_Score"
COLUMN_LEV09_VALUE = "Lev09_Wert"
COLUMN_LEV09_SCORE = "Lev09_Score"
COLUMN_LEV10_VALUE = "Lev10_Wert"
COLUMN_LEV10_SCORE = "Lev10_Score"
COLUMN_LEV11_VALUE = "Lev11_Wert"
COLUMN_LEV11_SCORE = "Lev11_Score"
COLUMN_LEV12_VALUE = "Lev12_Wert"
COLUMN_LEV12_SCORE = "Lev12_Score"
COLUMN_LEV13_VALUE = "Lev13_Wert"
COLUMN_LEV13_SCORE = "Lev13_Score"


ALL_COLUMNS = [
    COLUMN_URI,
    COLUMN_ACTIVE,
    COLUMN_LARGECAP,
    COLUMN_INDEX_URI,
    COLUMN_INDEX_NAME,
    COLUMN_PAGES,
    COLUMN_STOCK_URI,
    COLUMN_EARNINGS_AT,
    COLUMN_EQUITY_CAPITAL,
    COLUMN_OPERATIVE_RESULT,
    COLUMN_SALES_REVENUE,
    COLUMN_BALANCE,
    COLUMN_START_VALUE,
    COLUMN_CLOSING_VALUE,
    COLUMN_EPS_M3,
    COLUMN_EPS_M2,
    COLUMN_EPS_M1,
    COLUMN_EPS_0,
    COLUMN_EPS_P1,
    COLUMN_ANALYST_BUY,
    COLUMN_ANALYST_HOLD,
    COLUMN_ANALYST_SELL,
    COLUMN_MARKET_CAP,
    COLUMN_MARKET_PLACE,
    COLUMN_DATE,
    COLUMN_QUARTERLY,
    COLUMN_SECTORS,
    COLUMN_INDICES,
    COLUMN_LEV01_VALUE,
    COLUMN_LEV01_SCORE,
    COLUMN_LEV02_VALUE,
    COLUMN_LEV02_SCORE,
    COLUMN_LEV03_VALUE,
    COLUMN_LEV03_SCORE,
    COLUMN_LEV04_VALUE,
    COLUMN_LEV04_SCORE,
    COLUMN_LEV05_VALUE,
    COLUMN_LEV05_SCORE,
    COLUMN_LEV06_VALUE,
    COLUMN_LEV06_SCORE,
    COLUMN_LEV07_VALUE,
    COLUMN_LEV07_SCORE,
    COLUMN_LEV08_VALUE,
    COLUMN_LEV08_SCORE,
    COLUMN_LEV09_VALUE,
    COLUMN_LEV09_SCORE,
    COLUMN_LEV10_VALUE,
    COLUMN_LEV10_SCORE,
    COLUMN_LEV11_VALUE,
    COLUMN_LEV11_SCORE,
    COLUMN_LEV12_VALUE,
    COLUMN_LEV12_SCORE,
    COLUMN_LEV13_VALUE,
    COLUMN_LEV13_SCORE,
]

# Date Enums
DT_MINUS = "minus"
DT_PLUS = "plus"
DT_DAY = "day"
DT_MONTH = "month"

# Order Enums
ASC = "asc"
DESC = "desc"


# Data
MARKET_CAP_THRESHOLD = 5000

# Financial Sector List
FINANCE_SECTORS = [
    "Banken",
    "Finanzdienstleister",
    "Immobilien",
    "Investmentbanken / Broker",
    "Rückversicherungen",
    "Versicherungen",
]


LARGE_CAPS_INDIZES = ["CAC_40", "dax", "dow_jones", "Euro_Stoxx_50", "FTSE_100", "SMI"]
