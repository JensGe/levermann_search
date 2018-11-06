# Scraping Settings
SHORT_WAIT = 5 # Seconds
LONG_WAIT = 10 # Seconds


# Base Scraping URLs
URL_INDEX_CONTENT = 'https://www.boerse-online.de/index/liste/'
URL_INDEX_HISTORY = 'https://www.boerse-online.de/index/historisch/'
URL_STOCK_HISTORY = 'https://www.boerse-online.de/kurse/historisch/'
URL_STOCK_OVERVIEW = 'https://www.boerse-online.de/aktie/'

EXCHANGE_APPENDIX = '/FSE'
ALT_EXCHANGE_APPENDIX = '/XETRA'

# Scraping Parts
NO_DATA_AVAILABLE = 'Keine Daten verfügbar'

# Local Paths
INDEX_CONTENT_PATH = 'data/indizes/content/'
INDEX_HISTORY_PATH = 'data/indizes/history/'
STOCK_HISTORY_PATH = 'data/stocks/history/'
STOCK_OVERVIEW_PATH = 'data/stocks/overview/'


# File Extensions
EXT_HTML = '.html'


# Database
DATABASE = 'mysql://root:toor@localhost/levermann'


# Database Tables
TABLE_INDIZES = 'Aktienindizes'
TABLE_INDEX_HISTORIES = 'Indexhistorien'
TABLE_STOCKS = 'Aktien'
TABLE_STOCKS_HISTORIES = 'Aktienhistorien'
TABLE_INDEX_CONTENTS = 'Indexinhalte'


# Database Columns
COLUMN_URI = 'URI'
COLUMN_PAGES = 'Seiten'

