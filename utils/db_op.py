from utils import date_op as date
from utils import constants as CST
import sqlalchemy

import dataset


def get_index_names():
    with dataset.connect(CST.DATABASE) as database:
        index_list = [item[CST.COLUMN_URI] for item in database[CST.TABLE_INDIZES]]
    return index_list


def get_stock_names():
    with dataset.connect(CST.DATABASE) as database:
        stock_list = [item[CST.COLUMN_URI] for item in database[CST.TABLE_STOCKS]]
    return stock_list


def get_pages_count(index_name):
    with dataset.connect(CST.DATABASE) as database:
        table = database[CST.TABLE_INDIZES].find(URI=index_name)
        result = [item[CST.COLUMN_PAGES] for item in table]
        return int(result[0])


def create_index_url_list(base_url):
    index_list = get_index_names()
    url_list = [base_url + index for index in index_list]
    return url_list


def create_stock_history_url_list(base_url):
    stock_list = get_stock_names()
    url_list = [base_url + stock + CST.EXCHANGE_APPENDIX for stock in stock_list]
    return url_list


def create_stock_overview_url_list(base_url):
    stock_list = get_stock_names()
    url_list = [base_url + stock for stock in stock_list]
    return url_list


def create_stock_info_url_list(base_url):
    stock_list = get_stock_names()
    url_list = [base_url + stock[:-6] for stock in stock_list]
    return url_list


def check_if_exists(search, table, column):
    with dataset.connect(CST.DATABASE) as database:
        results = database.query("SELECT %s FROM %s WHERE %s = '%s'" % (column, table, column, search))
        try:
            result = [item for item in results][0]
        except IndexError:
            return False
        return result[column] == search


def write_stock_list_to_db(stock_list, index_name):
    for stock in stock_list:
        if not check_if_exists(stock[1], 'Aktien', 'ISIN'):
            write_stock_to_stock_table(stock)
        write_stock_to_stock_contents_table(stock[1], index_name, date.get_current_date())
    return True


def write_stock_to_stock_table(stock):
    with dataset.connect(CST.DATABASE) as database:
        try:
            database[CST.TABLE_STOCKS].insert(dict(Name=stock[0], URI=stock[1]))
        except sqlalchemy.exc.IntegrityError:
            pass


def write_stock_to_stock_contents_table(aktien_uri, index_name, current_date):
    with dataset.connect(CST.DATABASE) as database:
        try:
            database[CST.TABLE_INDEX_CONTENTS].insert(dict(IndexURI=index_name,
                                                           AktienURI=aktien_uri,
                                                           Abrufdatum=current_date))
        except sqlalchemy.exc.IntegrityError:
            pass


def write_index_history_to_db(index_history, index_uri):
    with dataset.connect(CST.DATABASE) as database:
        for item in index_history:
            date_ = date.string_to_date(item[0])
            start = float(item[1].replace('.', '').replace(',', '.'))
            try:
                end = float(item[2].replace('.', '').replace(',', '.'))
            except ValueError:
                print(item[2])
            try:
                database[CST.TABLE_INDEX_HISTORIES].insert(dict(IndexURI=index_uri, Datum=date_,
                                                                Eroeffnungswert=start, Schlusswert=end))
            except sqlalchemy.exc.IntegrityError:
                pass


def write_stock_history_to_db(stock_history, stock_uri):
    with dataset.connect(CST.DATABASE) as database:
        for item in stock_history:
            date_ = date.string_to_date(item[0])
            try:
                start = float(item[1].replace('.', '').replace(',', '.'))
                end = float(item[2].replace('.', '').replace(',', '.'))
            except ValueError:
                print('Missing Value for %s at %s' % (stock_uri, date))
                print('startdate: %s' % str(item[1]))
                print('enddate: %s' % str(item[2]))
            try:
                database[CST.TABLE_STOCKS_HISTORIES].insert(dict(AktienURI=stock_uri, Datum=date_,
                                                                Eroeffnungswert=start, Schlusswert=end))
            except sqlalchemy.exc.IntegrityError:
                print('IntegrityError')
                pass


def get_latest_date_from_index_history(index_uri):
    with dataset.connect(CST.DATABASE) as database:
        results = database.query("SELECT max(Datum) as maxdate FROM %s WHERE IndexURI = '%s'" %(CST.TABLE_INDEX_HISTORIES, index_uri))
        try:
            result = [item for item in results][0]
        except IndexError:
            return False
        return result['maxdate']


def get_latest_date_from_stock_history(stock_uri):
    with dataset.connect(CST.DATABASE) as database:
        results = database.query("SELECT max(Datum) as maxdate FROM %s WHERE URI = '%s'" %(CST.TABLE_STOCKS_HISTORIES, stock_uri))
        try:
            result = [item for item in results][0]
        except IndexError:
            return False
        return result['maxdate']


def write_single_overview_data_to_db(stock_uri, market_cap, stock_indizes, stock_sectors):
    current_date = date.get_current_date()
    with dataset.connect(CST.DATABASE) as database:
        try:
            database[CST.TABLE_COMPANY_DATA].insert(dict(AktienURI=stock_uri,
                                                         Datum=current_date,
                                                         Marktkapitalisierung=market_cap,
                                                         Indizes=str(stock_indizes),
                                                         Branchen=str(stock_sectors)))
        except sqlalchemy.exc.IntegrityError:
            database.query('UPDATE %s SET Marktkapitalisierung = "%s", Indizes = "%s", Branchen = "%s" '
                           'WHERE AktienURI = "%s" AND Datum = "%s"'
                           % (CST.TABLE_COMPANY_DATA, market_cap, str(stock_indizes),
                              str(stock_sectors), stock_uri, current_date))
            pass


def write_single_balance_data_to_db(stock_uri, result_after_tax, operative_result, sales_revenue, total_assets,
                                    equity_capital, eps_minus_3, eps_minus_2, eps_minus_1):
    current_date = date.get_current_date()
    with dataset.connect(CST.DATABASE) as database:
        try:
            database[CST.TABLE_COMPANY_DATA].insert(dict(AktienURI=stock_uri,
                                                         Datum=current_date,
                                                         Ergebnis_nach_Steuern=result_after_tax,
                                                         Operatives_Ergebnis=operative_result,
                                                         Umsatzerloese=sales_revenue,
                                                         Bilanzsumme=total_assets,
                                                         Eigenkapital=equity_capital,
                                                         EPS_minus_3=eps_minus_3,
                                                         EPS_minus_2=eps_minus_2,
                                                         EPS_minus_1=eps_minus_1))
        except sqlalchemy.exc.IntegrityError:
            print('Primary Key Existent - Update')
            database.query('UPDATE %s SET '
                           'Ergebnis_nach_Steuern = %s, '
                           'Operatives_Ergebnis = %s, '
                           'Umsatzerloese = %s, '
                           'Bilanzsumme = %s, '
                           'Eigenkapital = %s, '
                           'EPS_minus_3 = %s, '
                           'EPS_minus_2 = %s, '
                           'EPS_minus_1 = %s '
                           'WHERE AktienURI = "%s" AND Datum = "%s"'
                           % (CST.TABLE_COMPANY_DATA, result_after_tax, operative_result, sales_revenue, total_assets,
                              equity_capital, eps_minus_3, eps_minus_2, eps_minus_1, stock_uri, current_date))
            pass


def write_single_estimate_data_to_db(stock_uri, eps_0, eps_plus_1):
    current_date = date.get_current_date()
    with dataset.connect(CST.DATABASE) as database:
        try:
            database[CST.TABLE_COMPANY_DATA].insert(dict(AktienURI=stock_uri,
                                                         Datum=current_date,
                                                         EPS_0=eps_0,
                                                         EPS_plus_1=eps_plus_1))
        except sqlalchemy.exc.IntegrityError:
            print('Primary Key Existent - Update')
            database.query('UPDATE %s SET '
                           'EPS_0 = %s, '
                           'EPS_plus_1 = %s '
                           'WHERE AktienURI = "%s" AND Datum = "%s"'
                           % (CST.TABLE_COMPANY_DATA, eps_0, eps_plus_1, stock_uri, current_date))
            pass


def write_single_targets_data_to_db(stock_uri, analyst_buy, analyst_hold, analyst_sell):
    current_date = date.get_current_date()
    with dataset.connect(CST.DATABASE) as database:
        try:
            database[CST.TABLE_COMPANY_DATA].insert(dict(AktienURI=stock_uri,
                                                         Datum=current_date,
                                                         Analysten_Buy=analyst_buy,
                                                         Analysten_Hold=analyst_hold,
                                                         Analysten_Sell=analyst_sell))
        except sqlalchemy.exc.IntegrityError:
            print('Primary Key Existent - Update')
            database.query('UPDATE %s SET '
                           'Analysten_Buy = %s, '
                           'Analysten_Hold = %s, '
                           'Analysten_Sell = %s '
                           'WHERE AktienURI = "%s" AND Datum = "%s"'
                           % (CST.TABLE_COMPANY_DATA, analyst_buy, analyst_hold, analyst_sell, stock_uri, current_date))
            pass


def write_single_stock_dates_data_to_db(stock_uri, figures_date):
    with dataset.connect(CST.DATABASE) as database:
        try:
            database[CST.TABLE_STOCK_DATES].insert(dict(AktienURI=stock_uri,
                                                        Datum=figures_date,
                                                        Terminart='Quarterly/Yearly'))
        except sqlalchemy.exc.IntegrityError:
            print('Primary Key Existent - Update')
            database.query('UPDATE %s SET '
                           'Datum = %s '
                           'WHERE AktienURI = "%s"'
                           % (CST.TABLE_COMPANY_DATA, figures_date, stock_uri))
            pass


# Levermann 01

def get_earnings_after_tax(stock_uri):
    with dataset.connect(CST.DATABASE) as database:
        try:
            results = database.query("SELECT %s FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
                                     % (CST.COLUMN_EARNINGS_AT, CST.TABLE_COMPANY_DATA, stock_uri))
            return float([item for item in results][0][CST.COLUMN_EARNINGS_AT])
        except ValueError:
            pass
        except IndexError:
            pass


def get_equity_capital(stock_uri):
    with dataset.connect(CST.DATABASE) as database:
        try:
            results = database.query("SELECT %s FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
                                     % (CST.COLUMN_EQUITY_CAPITAL, CST.TABLE_COMPANY_DATA, stock_uri))
            return float([item for item in results][0][CST.COLUMN_EQUITY_CAPITAL])
        except ValueError:
            pass
        except IndexError:
            pass


def save_roe_to_db(stock_uri, roe, lev_score):
    current_date = date.get_current_date()
    with dataset.connect(CST.DATABASE) as database:
        try:
            database[CST.TABLE_LEVERMANN].insert(dict(AktienURI=stock_uri,
                                                      Datum=current_date,
                                                      Lev01_Wert=roe,
                                                      Lev01_Score=lev_score))
        except sqlalchemy.exc.IntegrityError:
            print('Primary Key Existent - Update')
            database.query('UPDATE %s SET '
                           'Lev01_Wert = %s, '
                           'Lev01_Score = %s '
                           'WHERE AktienURI = "%s" AND Datum = "%s"'
                           % (CST.TABLE_LEVERMANN, roe, lev_score, stock_uri, current_date))
            pass


# Levermann 02

def get_operative_result(stock_uri):
    with dataset.connect(CST.DATABASE) as database:
        try:
            results = database.query("SELECT %s FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
                                     % (CST.COLUMN_OPERATIVE_RESULT, CST.TABLE_COMPANY_DATA, stock_uri))
            return float([item for item in results][0][CST.COLUMN_OPERATIVE_RESULT])
        except ValueError:
            pass
        except IndexError:
            pass


def get_sales_revenue(stock_uri):
    with dataset.connect(CST.DATABASE) as database:
        try:
            results = database.query("SELECT %s FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
                                     % (CST.COLUMN_SALES_REVENUE, CST.TABLE_COMPANY_DATA, stock_uri))
            return float([item for item in results][0][CST.COLUMN_SALES_REVENUE])
        except ValueError:
            pass
        except IndexError:
            pass


def save_ebit_to_db(stock_uri, ebit, lev_score):
    current_date = date.get_current_date()
    with dataset.connect(CST.DATABASE) as database:
        try:
            database[CST.TABLE_LEVERMANN].insert(dict(AktienURI=stock_uri,
                                                      Datum=current_date,
                                                      Lev02_Wert=ebit,
                                                      Lev02_Score=lev_score))
        except sqlalchemy.exc.IntegrityError:
            print('Primary Key Existent - Update')
            database.query('UPDATE %s SET '
                           'Lev02_Wert = %s, '
                           'Lev02_Score = %s '
                           'WHERE AktienURI = "%s" AND Datum = "%s"'
                           % (CST.TABLE_LEVERMANN, ebit, lev_score, stock_uri, current_date))
            pass


# Levermann 03

def get_balance(stock_uri):
    with dataset.connect(CST.DATABASE) as database:
        try:
            results = database.query("SELECT %s FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
                                     % (CST.COLUMN_BALANCE, CST.TABLE_COMPANY_DATA, stock_uri))
            return float([item for item in results][0][CST.COLUMN_BALANCE])
        except ValueError:
            pass
        except IndexError:
            pass


def save_equity_ratio_to_db(stock_uri, equity_ratio, lev_score):
    current_date = date.get_current_date()
    with dataset.connect(CST.DATABASE) as database:
        try:
            database[CST.TABLE_LEVERMANN].insert(dict(AktienURI=stock_uri,
                                                      Datum=current_date,
                                                      Lev03_Wert=equity_ratio,
                                                      Lev03_Score=lev_score))
        except sqlalchemy.exc.IntegrityError:
            print('Primary Key Existent - Update')
            database.query('UPDATE %s SET '
                           'Lev03_Wert = %s, '
                           'Lev03_Score = %s '
                           'WHERE AktienURI = "%s" AND Datum = "%s"'
                           % (CST.TABLE_LEVERMANN, equity_ratio, lev_score, stock_uri, current_date))
            pass


# Levermann 04 & 05

def get_current_stock_price(stock_uri):
    with dataset.connect(CST.DATABASE) as database:
        try:
            results = database.query("SELECT %s FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
                                     % (CST.COLUMN_CLOSING_VALUE, CST.TABLE_STOCKS_HISTORIES, stock_uri))
            return float([item for item in results][0][CST.COLUMN_CLOSING_VALUE])
        except ValueError:
            pass
        except IndexError:
            pass


def get_eps(stock_uri):
    with dataset.connect(CST.DATABASE) as database:
        try:
            results = database.query("SELECT * FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
                                     % (CST.TABLE_COMPANY_DATA, stock_uri))
            eps_s = [item for item in results][0]
            eps_list = [float(eps_s[CST.COLUMN_EPS_M3]), float(eps_s[CST.COLUMN_EPS_M2]),
                        float(eps_s[CST.COLUMN_EPS_M1]), float(eps_s[CST.COLUMN_EPS_0]),
                        float(eps_s[CST.COLUMN_EPS_P1])]
            return eps_list
        except ValueError:
            pass
        except IndexError:
            pass


def save_kgv5_to_db(stock_uri, kgv5, kgv5_score):
    current_date = date.get_current_date()
    with dataset.connect(CST.DATABASE) as database:
        try:
            database[CST.TABLE_LEVERMANN].insert(dict(AktienURI=stock_uri,
                                                      Datum=current_date,
                                                      Lev04_Wert=kgv5,
                                                      Lev04_Score=kgv5_score))
        except sqlalchemy.exc.IntegrityError:
            print('Primary Key Existent - Update')
            database.query('UPDATE %s SET '
                           'Lev04_Wert = %s, '
                           'Lev04_Score = %s '
                           'WHERE AktienURI = "%s" AND Datum = "%s"'
                           % (CST.TABLE_LEVERMANN, kgv5, kgv5_score, stock_uri, current_date))
            pass


def save_kgv0_to_db(stock_uri, kgv0, kgv0_score):
    current_date = date.get_current_date()
    with dataset.connect(CST.DATABASE) as database:
        try:
            database[CST.TABLE_LEVERMANN].insert(dict(AktienURI=stock_uri,
                                                      Datum=current_date,
                                                      Lev05_Wert=kgv0,
                                                      Lev05_Score=kgv0_score))
        except sqlalchemy.exc.IntegrityError:
            print('Primary Key Existent - Update')
            database.query('UPDATE %s SET '
                           'Lev05_Wert = %s, '
                           'Lev05_Score = %s '
                           'WHERE AktienURI = "%s" AND Datum = "%s"'
                           % (CST.TABLE_LEVERMANN, kgv0, kgv0_score, stock_uri, current_date))
            pass


# Levermann 06

def get_analyst_ratings(stock_uri):
    with dataset.connect(CST.DATABASE) as database:
        try:
            results = database.query("SELECT * FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
                                     % (CST.TABLE_COMPANY_DATA, stock_uri))
            ratings = [item for item in results][0]
            rating_list = [int(ratings[CST.COLUMN_ANALYST_BUY]),
                           int(ratings[CST.COLUMN_ANALYST_HOLD]),
                           int(ratings[CST.COLUMN_ANALYST_SELL])]
            return rating_list
        except ValueError:
            pass
        except IndexError:
            pass


def save_rating_to_db(stock_uri, rating, rating_score):
    current_date = date.get_current_date()
    with dataset.connect(CST.DATABASE) as database:
        try:
            database[CST.TABLE_LEVERMANN].insert(dict(AktienURI=stock_uri,
                                                      Datum=current_date,
                                                      Lev06_Wert=rating,
                                                      Lev06_Score=rating_score))
        except sqlalchemy.exc.IntegrityError:
            print('Primary Key Existent - Update')
            database.query('UPDATE %s SET '
                           'Lev06_Wert = %s, '
                           'Lev06_Score = %s '
                           'WHERE AktienURI = "%s" AND Datum = "%s"'
                           % (CST.TABLE_LEVERMANN, rating, rating_score, stock_uri, current_date))
            pass


def is_small_cap(stock_uri):
    # ToDo Check if in Large Cap Index (if market Cap low)
    with dataset.connect(CST.DATABASE) as database:
        try:
            results = database.query("SELECT * FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
                                     % (CST.TABLE_COMPANY_DATA, stock_uri))
            market_cap = float([item for item in results][0][CST.COLUMN_MARKET_CAP])
            return True if market_cap < CST.MARKET_CAP_THRESHOLD else False
        except ValueError:
            pass
        except IndexError:
            pass


# Levermann 07

def get_quarterly_date(stock_uri):
    with dataset.connect(CST.DATABASE) as database:
        try:
            results = database.query("SELECT * FROM %s WHERE AktienURI = '%s'"
                                     % (CST.TABLE_STOCK_DATES, stock_uri))
            quarterly_date = [item for item in results][0][CST.COLUMN_DATE]
            return quarterly_date
        except ValueError:
            pass
        except IndexError:
            pass


def get_closing_stock_price(request_date, aktien_uri):
    with dataset.connect(CST.DATABASE) as database:
        try:
            results = database.query("SELECT * FROM %s WHERE AktienURI = '%s' and Datum <= '%s' ORDER BY Datum DESC"
                                     % (CST.TABLE_STOCKS_HISTORIES, aktien_uri, request_date))
            closing_price = [item for item in results][0][CST.COLUMN_CLOSING_VALUE]
            return closing_price
        except ValueError:
            pass
        except IndexError:
            pass


def get_closing_index_price(request_date, index_uri):
    with dataset.connect(CST.DATABASE) as database:
        try:
            results = database.query("SELECT * FROM %s WHERE IndexURI = '%s' and Datum = '%s'"
                                     % (CST.TABLE_INDEX_HISTORIES, index_uri, request_date))
            closing_price = [item for item in results][0][CST.COLUMN_CLOSING_VALUE]
            return closing_price
        except ValueError:
            pass
        except IndexError:
            pass


def get_index_of_stock(aktien_uri):
    with dataset.connect(CST.DATABASE) as database:
        try:
            results = database.query("SELECT * FROM %s WHERE AktienURI = '%s'"
                                     % (CST.TABLE_INDEX_CONTENTS, aktien_uri))
            index_uri = [item for item in results][0][CST.COLUMN_INDEX_URI]
            return index_uri
        except ValueError:
            pass
        except IndexError:
            pass


def save_quaterly_reaction_to_db(stock_uri, rating, rating_score):
    current_date = date.get_current_date()
    with dataset.connect(CST.DATABASE) as database:
        try:
            database[CST.TABLE_LEVERMANN].insert(dict(AktienURI=stock_uri,
                                                      Datum=current_date,
                                                      Lev06_Wert=rating,
                                                      Lev06_Score=rating_score))
        except sqlalchemy.exc.IntegrityError:
            print('Primary Key Existent - Update')
            database.query('UPDATE %s SET '
                           'Lev06_Wert = %s, '
                           'Lev06_Score = %s '
                           'WHERE AktienURI = "%s" AND Datum = "%s"'
                           % (CST.TABLE_LEVERMANN, rating, rating_score, stock_uri, current_date))
            pass


#################
#
# OLD TODO DELETE
# >>>>>>>>>>>>>>
#
#################


def select_data(table):
    with dataset.connect(CST.DATABASE) as tx:
        print(tx[table])


def write_data(table_name, dictionary):
    with dataset.connect(CST.DATABASE) as tx:
        tx[table_name].insert(dictionary)

# def write_data(table_name, dictionary):
#     with dataset.connect('sqlite:///data/stockbase.db') as tx:
#         tx[table_name].insert(dictionary)


def clear_index_contents(table_name, index_name):
    """
    Deletes all rows in a table with a given index_name
    :param table_name: table, where the deletion has to be
    :param index_name: filtering one index_name, which will be cleared
    :return:
    """
    with dataset.connect('sqlite:///data/stockbase.db') as tx:
        tx[table_name].delete(index=index_name)
    return True


def get_max_date_of_index_history(index_name):
    db = dataset.connect('sqlite:///data/stockbase.db')
    try:
        dates = db.get_table('index_histories').find(index=index_name)
    except:
        return False

    date_list = []
    for item in dates:
        date_list.append(date.string_to_date(item['datum']))

    if len(date_list) == 0:
        return False
    max_date = sorted(date_list, reverse=True)[0]
    max_date_str = date.date_to_string(max_date)
    return max_date_str


def get_max_date_of_stock_history(stock_name):
    db = dataset.connect('sqlite:///data/stockbase.db')
    try:
        dates = db.get_table('stock_histories').find(stock=stock_name)
    except:
        return False

    date_list = []
    for item in dates:
        date_list.append(date.string_to_date(item['datum']))

    if len(date_list) == 0:
        return False
    max_date = sorted(date_list, reverse=True)[0]
    max_date_str = date.date_to_string(max_date)
    return max_date_str


def get_closing_price_from_date(request_date, index_name):
    db = dataset.connect('sqlite:///data/stockbase.db')
    q_date = date.date_to_string(request_date)
    result = db.get_table('index_histories').find(datum=q_date, index=index_name)
    for value in result:
        return value['schluss']


def get_all_stock_infos(index_name):
    db = dataset.connect('sqlite:///data/stockbase.db')
    try:
        urls = db.get_table('index_stocks').find(index=index_name)
    except:
        return False
    url_list = []
    for url in urls:
        url_list.append([url['stock_name'], url['ISIN'], url['stock_link']])
    return url_list
