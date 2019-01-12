from loguru import logger

from utils import date_op as date
from utils import constants as CST
import sqlalchemy

import dataset


def get_all_index_names():
    with dataset.connect(CST.DATABASE) as database:
        index_list = [item[CST.COLUMN_URI] for item in database[CST.TABLE_INDIZES]]
    return index_list


def get_active_index_names():
    with dataset.connect(CST.DATABASE) as database:
        index_list = [item[CST.COLUMN_URI] for item in database[CST.TABLE_INDIZES] if item[CST.COLUMN_ACTIVE] == b'1']
    return index_list


def get_stock_names_and_history_url():
    with dataset.connect(CST.DATABASE) as database:
        stock_and_history_url_list = [[item[CST.COLUMN_URI], item[CST.COLUMN_MARKET_PLACE]] for item in database[CST.TABLE_STOCKS]]
    return stock_and_history_url_list


def get_stock_names():
    with dataset.connect(CST.DATABASE) as database:
        stock_list = [item[CST.COLUMN_URI] for item in database[CST.TABLE_STOCKS]]
    return stock_list


def get_pages_count(index_name):
    with dataset.connect(CST.DATABASE) as database:
        table = database[CST.TABLE_INDIZES].find(URI=index_name)
        result = [item[CST.COLUMN_PAGES] for item in table]
        return int(result[0])


def create_all_index_url_list(base_url):
    index_list = get_all_index_names()
    url_list = [base_url + index for index in index_list]
    return url_list


def create_active_index_url_list(base_url):
    index_list = get_active_index_names()
    url_list = [base_url + index for index in index_list]
    return url_list


def create_stock_history_url_list(base_url):
    stock_history_list = get_stock_names_and_history_url()
    # url_list = [base_url + stock[0] + '/' + stock[1] for stock in stock_history_list]
    url_list = []
    for stock in stock_history_list:
        stock_uri, market_place = stock[0][:-6], stock[1]
        if market_place is None:
            market_place = CST.EXCHANGE_APPENDIX
        url_list.append(base_url + stock_uri + market_place)
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
                logger.exception("Write Index History to DB: ValueError with Item: %s" % item[2])
            try:
                database[CST.TABLE_INDEX_HISTORIES].insert(dict(IndexURI=index_uri, Datum=date_,
                                                                Eroeffnungswert=start, Schlusswert=end))
            except sqlalchemy.exc.IntegrityError:
                logger.exception("Write Index History to DB: Integrity Error with Item: %s" % index_uri)
                pass


def write_stock_history_to_db(stock_history, stock_uri):
    with dataset.connect(CST.DATABASE) as database:
        for item in stock_history:
            date_ = date.string_to_date(item[0])
            try:
                start = float(item[1].replace('.', '').replace(',', '.'))
            except ValueError:
                logger.exception("ValueError: Missing start value for %s at %s" % (stock_uri, str(date_)))
                start = None
            try:
                end = float(item[2].replace('.', '').replace(',', '.'))
            except ValueError:
                logger.exception("ValueError: Missing end value for %s at %s" % (stock_uri, str(date_)))
                end = None
            try:
                database[CST.TABLE_STOCKS_HISTORIES].insert(dict(AktienURI=stock_uri, Datum=date_,
                                                                 Eroeffnungswert=start, Schlusswert=end))
            except sqlalchemy.exc.IntegrityError:
                pass


def get_latest_date_from_index_history(index_uri):
    with dataset.connect(CST.DATABASE) as database:
        results = database.query("SELECT max(Datum) as maxdate "
                                 "FROM %s WHERE IndexURI = '%s'"
                                 % (CST.TABLE_INDEX_HISTORIES, index_uri))
        try:
            result = [item for item in results][0]
        except IndexError:
            logger.exception("Get Latest Date from Index History: IndexError for %s" % index_uri)
            return False
        return result['maxdate']


def get_latest_date_from_stock_history(stock_uri):
    with dataset.connect(CST.DATABASE) as database:
        results = database.query("SELECT max(Datum) as maxdate "
                                 "FROM %s WHERE AktienURI = '%s'"
                                 % (CST.TABLE_STOCKS_HISTORIES, stock_uri))
        try:
            result = [item for item in results][0]
        except IndexError:
            logger.exception("Get Latest Date from Stock History: IndexError for %s" % stock_uri)
            return False
        return result['maxdate']


def write_single_overview_data_to_db(stock_uri, market_cap, stock_indizes, stock_sectors, market_place):
    current_date = date.get_current_date()
    with dataset.connect(CST.DATABASE) as database:
        try:
            database[CST.TABLE_COMPANY_DATA].insert(dict(AktienURI=stock_uri,
                                                         Datum=current_date,
                                                         Marktkapitalisierung=market_cap,
                                                         Indizes=str(stock_indizes),
                                                         Branchen=str(stock_sectors)))
        except sqlalchemy.exc.IntegrityError:
            database.query('UPDATE %s SET '
                           'Marktkapitalisierung = "%s", '
                           'Indizes = "%s", '
                           'Branchen = "%s" '
                           'WHERE AktienURI = "%s" AND Datum = "%s"'
                           % (CST.TABLE_COMPANY_DATA, market_cap, str(stock_indizes),
                              str(stock_sectors), stock_uri, current_date))
            pass
        try:
            database.query('UPDATE %s SET '
                           'Handelsplatz = "%s" '
                           'WHERE URI = "%s"'
                           % (CST.TABLE_STOCKS, market_place, stock_uri))
        except:
            logger.exception('Exception at Marketplace Insertation')
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
        except:
            logger.exception("Exception at get_earnings_after_tax for %s" %stock_uri)
            pass


def get_equity_capital(stock_uri):
    with dataset.connect(CST.DATABASE) as database:
        try:
            results = database.query("SELECT %s FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
                                     % (CST.COLUMN_EQUITY_CAPITAL, CST.TABLE_COMPANY_DATA, stock_uri))
            return float([item for item in results][0][CST.COLUMN_EQUITY_CAPITAL])
        except:
            logger.exception("Exception at get_equity_capital for %s" %stock_uri)
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
        except:
            logger.exception("Exception at get_operative_result for %s" %stock_uri)
            pass


def get_sales_revenue(stock_uri):
    with dataset.connect(CST.DATABASE) as database:
        try:
            results = database.query("SELECT %s FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
                                     % (CST.COLUMN_SALES_REVENUE, CST.TABLE_COMPANY_DATA, stock_uri))
            return float([item for item in results][0][CST.COLUMN_SALES_REVENUE])
        except:
            logger.exception("Exception at get_sales_revenue for %s" %stock_uri)
            pass


def check_is_financial_company(stock_uri):
    fin_list = CST.FINANCE_SECTORS
    with dataset.connect(CST.DATABASE) as database:
        try:
            results = database.query("SELECT %s FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
                                     % (CST.COLUMN_SECTORS, CST.TABLE_COMPANY_DATA, stock_uri))
            result_list = [item for item in results][0][CST.COLUMN_SECTORS]
            return any(i in result_list for i in fin_list)
        except:
            logger.exception("Exception at check_is_financial_company for %s" %stock_uri)
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
        except:
            logger.exception("Exception at get_balance for %s" % stock_uri)
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
            database.query('UPDATE %s SET '
                           'Lev03_Wert = %s, '
                           'Lev03_Score = %s '
                           'WHERE AktienURI = "%s" AND Datum = "%s"'
                           % (CST.TABLE_LEVERMANN, equity_ratio, lev_score, stock_uri, current_date))
            pass


# Levermann 04 & 05

def get_latest_stock_price(stock_uri):
    with dataset.connect(CST.DATABASE) as database:
        try:
            results = database.query("SELECT %s FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
                                     % (CST.COLUMN_CLOSING_VALUE, CST.TABLE_STOCKS_HISTORIES, stock_uri))
            return float([item for item in results][0][CST.COLUMN_CLOSING_VALUE])
        except:
            logger.exception("Exception at get_latest_stock_price for %s" % stock_uri)
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
        except:
            logger.exception("Exception at get_eps for %s" % stock_uri)
            pass


def get_older_eps(stock_uri):
    with dataset.connect(CST.DATABASE) as database:
        try:
            results = database.query("SELECT * FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
                                     % (CST.TABLE_COMPANY_DATA, stock_uri))
            eps_s = [item for item in results][1]
            eps_list = [float(eps_s[CST.COLUMN_EPS_M3]), float(eps_s[CST.COLUMN_EPS_M2]),
                        float(eps_s[CST.COLUMN_EPS_M1]), float(eps_s[CST.COLUMN_EPS_0]),
                        float(eps_s[CST.COLUMN_EPS_P1])]
            return eps_list
        except:
            logger.exception("Exception at get_older_eps for %s" % stock_uri)
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
        except:
            logger.exception("Exception at get_analyst_ratings for %s" % stock_uri)
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
            database.query('UPDATE %s SET '
                           'Lev06_Wert = %s, '
                           'Lev06_Score = %s '
                           'WHERE AktienURI = "%s" AND Datum = "%s"'
                           % (CST.TABLE_LEVERMANN, rating, rating_score, stock_uri, current_date))
            pass


def is_small_cap(stock_uri):
    with dataset.connect(CST.DATABASE) as database:
        try:
            market_cap_results = database.query("SELECT * FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC" %
                                                (CST.TABLE_COMPANY_DATA, stock_uri))
            market_cap = float([item for item in market_cap_results][0][CST.COLUMN_MARKET_CAP])
            if market_cap > CST.MARKET_CAP_THRESHOLD:
                return False
            else:
                indizes_list = get_indizes_of_stock(stock_uri)
                return not any(i in indizes_list for i in CST.LARGE_CAPS_INDIZES)

        except:
            logger.exception("Exception at is_small_cap for %s" % stock_uri)
            pass


# Levermann 07

def get_quarterly_date(stock_uri):
    with dataset.connect(CST.DATABASE) as database:
        try:
            results = database.query("SELECT * FROM %s WHERE AktienURI = '%s'"
                                     % (CST.TABLE_STOCK_DATES, stock_uri))
            quarterly_date = [item for item in results][0][CST.COLUMN_DATE]
            return quarterly_date
        except:
            logger.exception("Exception at get_quarterly_date for %s" % stock_uri)
            pass


def get_closing_stock_price(request_date, stock_uri):
    with dataset.connect(CST.DATABASE) as database:
        try:
            results = database.query("SELECT * FROM %s WHERE AktienURI = '%s' and Datum <= '%s' ORDER BY Datum DESC"
                                     % (CST.TABLE_STOCKS_HISTORIES, stock_uri, request_date))
            result = [item for item in results][0]
            closing_price = result[CST.COLUMN_CLOSING_VALUE]
            actual_date = result[CST.COLUMN_DATE]
            return closing_price, actual_date
        except:
            logger.exception("Exception at get_closing_stock_price for %s" % stock_uri)
            pass


def get_closing_index_price(request_date, index_uri):
    with dataset.connect(CST.DATABASE) as database:
        try:
            results = database.query("SELECT * FROM %s WHERE IndexURI = '%s' and Datum <= '%s' ORDER BY Datum DESC"
                                     % (CST.TABLE_INDEX_HISTORIES, index_uri, request_date))
            result = [item for item in results][0]
            closing_price = result[CST.COLUMN_CLOSING_VALUE]
            actual_date = result[CST.COLUMN_DATE]
            return closing_price, actual_date
        except:
            logger.exception("Exception at get_closing_index_price for %s" % index_uri)
            pass


def get_index_of_stock(stock_uri):
    with dataset.connect(CST.DATABASE) as database:
        try:
            results = database.query("SELECT * FROM %s WHERE AktienURI = '%s'"
                                     % (CST.TABLE_INDEX_CONTENTS, stock_uri))
            index_uri = [item for item in results][0][CST.COLUMN_INDEX_URI]
            return index_uri
        except:
            logger.exception("Exception at get_index_of_stock for %s" % stock_uri)
            pass


def get_indizes_of_stock(stock_uri):
    with dataset.connect(CST.DATABASE) as database:
        try:
            results = database.query("SELECT * FROM %s WHERE AktienURI = '%s'"
                                     % (CST.TABLE_INDEX_CONTENTS, stock_uri))
            index_uri = {item[CST.COLUMN_INDEX_URI] for item in results}
            return sorted(index_uri)
        except:
            logger.exception("Exception at get_indizes_of_stock for %s" % stock_uri)
            pass


def save_quarterly_reaction_to_db(stock_uri, quarterly_diff, lev_score):
    current_date = date.get_current_date()
    with dataset.connect(CST.DATABASE) as database:
        try:
            database[CST.TABLE_LEVERMANN].insert(dict(AktienURI=stock_uri,
                                                      Datum=current_date,
                                                      Lev07_Wert=quarterly_diff,
                                                      Lev07_Score=lev_score))
        except sqlalchemy.exc.IntegrityError:
            database.query('UPDATE %s SET '
                           'Lev07_Wert = %s, '
                           'Lev07_Score = %s '
                           'WHERE AktienURI = "%s" AND Datum = "%s"'
                           % (CST.TABLE_LEVERMANN, quarterly_diff, lev_score, stock_uri, current_date))
            pass


# Levermann 08

def save_eps_revision_to_db(stock_uri, eps_diff, lev_score):
    current_date = date.get_current_date()
    with dataset.connect(CST.DATABASE) as database:
        try:
            database[CST.TABLE_LEVERMANN].insert(dict(AktienURI=stock_uri,
                                                      Datum=current_date,
                                                      Lev08_Wert=eps_diff,
                                                      Lev08_Score=lev_score))
        except sqlalchemy.exc.IntegrityError:
            database.query('UPDATE %s SET '
                           'Lev08_Wert = %s, '
                           'Lev08_Score = %s '
                           'WHERE AktienURI = "%s" AND Datum = "%s"'
                           % (CST.TABLE_LEVERMANN, eps_diff, lev_score, stock_uri, current_date))
            pass


# Levermann 09-11

def save_6_months_ratio_to_db(stock_uri, ratio, lev_score):
    current_date = date.get_current_date()
    with dataset.connect(CST.DATABASE) as database:
        try:
            database[CST.TABLE_LEVERMANN].insert(dict(AktienURI=stock_uri,
                                                      Datum=current_date,
                                                      Lev09_Wert=ratio,
                                                      Lev09_Score=lev_score))
        except sqlalchemy.exc.IntegrityError:
            database.query('UPDATE %s SET '
                           'Lev09_Wert = %s, '
                           'Lev09_Score = %s '
                           'WHERE AktienURI = "%s" AND Datum = "%s"'
                           % (CST.TABLE_LEVERMANN, ratio, lev_score, stock_uri, current_date))
            pass


def save_12_months_ratio_to_db(stock_uri, ratio, lev_score):
    current_date = date.get_current_date()
    with dataset.connect(CST.DATABASE) as database:
        try:
            database[CST.TABLE_LEVERMANN].insert(dict(AktienURI=stock_uri,
                                                      Datum=current_date,
                                                      Lev10_Wert=ratio,
                                                      Lev10_Score=lev_score))
        except sqlalchemy.exc.IntegrityError:
            database.query('UPDATE %s SET '
                           'Lev10_Wert = %s, '
                           'Lev10_Score = %s '
                           'WHERE AktienURI = "%s" AND Datum = "%s"'
                           % (CST.TABLE_LEVERMANN, ratio, lev_score, stock_uri, current_date))
            pass


def save_momentum_to_db(stock_uri, lev_score):
    current_date = date.get_current_date()
    with dataset.connect(CST.DATABASE) as database:
        try:
            database[CST.TABLE_LEVERMANN].insert(dict(AktienURI=stock_uri,
                                                      Datum=current_date,
                                                      Lev11_Score=lev_score))
        except sqlalchemy.exc.IntegrityError:
            database.query('UPDATE %s SET '
                           'Lev11_Score = %s '
                           'WHERE AktienURI = "%s" AND Datum = "%s"'
                           % (CST.TABLE_LEVERMANN, lev_score, stock_uri, current_date))
            pass


# Levermann 12

def calculate_list_changes(value_list):
    stock_changes = []
    for i in range(len(value_list)-1):
            stock_change = (value_list[i+1] / value_list[i]) -1
            stock_changes.append(round(stock_change, 2))
    return stock_changes


def save_reversal_to_db(stock_uri, diff, lev_score):
    current_date = date.get_current_date()
    with dataset.connect(CST.DATABASE) as database:
        try:
            database[CST.TABLE_LEVERMANN].insert(dict(AktienURI=stock_uri,
                                                      Datum=current_date,
                                                      Lev12_Wert=diff,
                                                      Lev12_Score=lev_score))
        except sqlalchemy.exc.IntegrityError:
            database.query('UPDATE %s SET '
                           'Lev12_Wert = %s, '
                           'Lev12_Score = %s '
                           'WHERE AktienURI = "%s" AND Datum = "%s"'
                           % (CST.TABLE_LEVERMANN, diff, lev_score, stock_uri, current_date))
            pass


# Levermann 13

def save_profit_growth_to_db(stock_uri, diff, lev_score):
    current_date = date.get_current_date()
    with dataset.connect(CST.DATABASE) as database:
        try:
            database[CST.TABLE_LEVERMANN].insert(dict(AktienURI=stock_uri,
                                                      Datum=current_date,
                                                      Lev13_Wert=diff,
                                                      Lev13_Score=lev_score))
        except sqlalchemy.exc.IntegrityError:
            database.query('UPDATE %s SET '
                           'Lev13_Wert = %s, '
                           'Lev13_Score = %s '
                           'WHERE AktienURI = "%s" AND Datum = "%s"'
                           % (CST.TABLE_LEVERMANN, diff, lev_score, stock_uri, current_date))
            pass


def get_levermann_buy():
    with dataset.connect(CST.DATABASE) as database:
        try:
            logger.info("Query DB Levermann BUY View")
            results = database.query("SELECT * "
                                     "FROM %s " % CST.VIEW_LEVERMANN_BUY)
            return results
        except:
            logger.exception("Exception at get_levermann_buy")
            pass


def get_levermann_hold():
    with dataset.connect(CST.DATABASE) as database:
        try:
            results = database.query("SELECT * "
                                     "FROM %s " % CST.VIEW_LEVERMANN_HOLD)
            return results
        except:
            logger.exception("Exception at get_levermann_hold")
            pass

