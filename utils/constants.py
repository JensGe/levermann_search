# Scraping Settings
SHORT_WAIT = 5 # Seconds
LONG_WAIT = 10 # Seconds

# Parser Settings
PARSER = 'html.parser'

# Selenium Driver Settings
SELENIUM_SETTINGS = 'utils/driver_starting_settings.txt'

# Base Scraping URLs
URL_INDEX_CONTENT = 'https://www.boerse-online.de/index/liste/'
URL_INDEX_HISTORY = 'https://www.boerse-online.de/index/historisch/'
URL_STOCK_HISTORY = 'https://www.boerse-online.de/kurse/historisch/'
URL_STOCK_OVERVIEW = 'https://www.boerse-online.de/aktie/'
URL_STOCK_BALANCE = 'https://www.boerse-online.de/bilanz_guv/'
URL_STOCK_TARGETS = 'https://www.boerse-online.de/kursziele/'
URL_STOCK_DATES = 'https://www.boerse-online.de/termine/uebersicht/'
URL_STOCK_ESTIMATES = 'https://www.boerse-online.de/schaetzungen/'


EXCHANGE_APPENDIX = '/FSE'
ALT_EXCHANGE_APPENDIX = '/XETRA'
# Laut Levermann eigentlich primär XETRA, dann FSE oder entpr. des Landes

# Scraping Parts
NO_DATA_AVAILABLE = 'Keine Daten verfügbar'

TEXT_LAST_DATES = 'vergangene Termine'
TEXT_EPS_UNDILUTED = 'Ergebnis je Aktie unverwässert'
TEXT_EPS = 'Ergebnis/Aktie'
TEXT_MARKET_CAP = 'Marktkapitalisierung'
TEXT_LISTED_INDIZES = 'Zur Aktie'
TEXT_COMPANY_INFO = 'Zum Unternehmen'
TEXT_RESULT_AFTER_TAX = 'Ergebnis nach Steuer'
TEXT_OPERATIVE_RESULT = 'Operatives Ergebnis'
TEXT_SALES_REVENUE = 'Umsatzerlöse'
TEXT_TOTAL_ASSETS = 'Bilanzsumme'
TEXT_EQUITY_CAPITAL = 'Eigenkapital'

# HTML Attributes
TEXT_HISTORIC_RATING = 'historicRatingTdContent'
HISTORIC_PRICE_LIST = 'historic-price-list'
TEXT_TEXT_RIGHT = 'text-right'
TEXT_INDEX_LIST_CONTAINER = 'index-list-container'
TEXT_PAGINATION = 'finando_paging'


# HTML Elements
HTML_H2 = 'h2'
HTML_TD = 'td'
HTML_TR = 'tr'
HTML_DIV = 'div'
HTML_A = 'a'
HTML_CLASS = 'class'
HTML_ID = 'id'
HTML_SPAN = 'span'
HTML_HREF = 'href'



# Local Paths
PATH_INDEX_CONTENT = 'data/indizes/content/'
PATH_INDEX_HISTORY = 'data/indizes/history/'
PATH_STOCK_HISTORY = 'data/stocks/history/'
PATH_STOCK_OVERVIEW = 'data/stocks/overview/'
PATH_STOCK_BALANCE = 'data/stocks/balance/'
PATH_STOCK_TARGETS = 'data/stocks/targets/'
PATH_STOCK_DATES = 'data/stocks/dates/'
PATH_STOCK_ESTIMATES = 'data/stocks/estimates/'


# File Extensions
HTML_EXTENSION = '.html'


# Database
DATABASE = 'mysql://root:toor@localhost/levermann'


# Database Tables
TABLE_INDIZES = 'Aktienindizes'
TABLE_INDEX_HISTORIES = 'Indexhistorien'
TABLE_STOCKS = 'Aktien'
TABLE_STOCKS_HISTORIES = 'Aktienhistorien'
TABLE_INDEX_CONTENTS = 'Indexinhalte'
TABLE_COMPANY_DATA = 'Unternehmensdaten'


# Database Columns
COLUMN_URI = 'URI'
COLUMN_PAGES = 'Seiten'

