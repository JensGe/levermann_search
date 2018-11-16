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

EXCHANGE_APPENDIX = '/FSE'
ALT_EXCHANGE_APPENDIX = '/XETRA'

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
INDEX_CONTENT_PATH = 'data/indizes/content/'
INDEX_HISTORY_PATH = 'data/indizes/history/'
STOCK_HISTORY_PATH = 'data/stocks/history/'
STOCK_OVERVIEW_PATH = 'data/stocks/overview/'


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

