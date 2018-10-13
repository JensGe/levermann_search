from Scrapper import db_refresher
import time


index_names = ['DAX', 'Dow_Jones', 'Nasdaq_100', 'FTSE_100', 'Euro_Stoxx_50', 'SMI',
               'S&P-TSX-60', 'OMXH25', 'OSEBX', 'OMX', 'OMXC20', 'RTS', 'CAC_40',
               'IBEX_35', 'Shanghai_Composite', 'Nikkei_225', 'SENSEX', 'BOVESPA',
               'Hang_Seng', 'S&P_ASX_20', 'Straits_Times']

print('Skip*==== Index History Refresh ====')
# for index in index_names[:4]:
#     print('---- wait 10 s')
#     time.sleep(10)
#     print('---- next Index: %s' % index)
#     start, end = db_refresher.select_intervall(index)
#     db_refresher.refresh_index_history(index, start, end)


print('Skip*==== Index Stock Refresh ====')
# for index in index_names[:4]:
#     print('---- wait 10 s')
#     time.sleep(10)
#     print('---- next Index: %s' % index)
#     db_refresher.refresh_index_stocks(index)

print('==== Stock Index Refresh ====')
for index in index_names[:4]:
    print('---- wait 10 s')
    time.sleep(10)
    print('---- next Index: %s' % index)
    db_refresher.refresh_all_stocks_history(index)
