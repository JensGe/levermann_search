from loguru import logger

from utils import date_op as date
from utils import constants as cst
import sqlalchemy

import dataset


# CRUD
def get_list(table, columns, condition=None, database=cst.DATABASE):

    if not condition:
        if isinstance(columns, str):
            with dataset.connect(database) as db:
                return [item[columns] for item in db[table]]
        elif isinstance(columns, list):
            with dataset.connect(database) as db:
                return [[item[column] for column in columns] for item in db[table]]

    else:
        if isinstance(columns, str):
            with dataset.connect(database) as db:
                return [
                    item[columns]
                    for item in db[table]
                    if item[condition[0]] == condition[1]
                ]
        elif isinstance(columns, list):
            with dataset.connect(database) as db:
                return [
                    [item[column] for column in columns]
                    for item in db[table]
                    if item[condition[0]] == condition[1]
                ]


def get_item(table, column, condition=None, database=cst.DATABASE):
    with dataset.connect(database) as db:
        results = db.query(
            "SELECT %s as result "
            "FROM %s "
            "WHERE %s = '%s'" % (column, table, condition[0], condition[1])
        )
        result = [item for item in results][0]
    return result["result"]


def insert_list(table, data, database=cst.DATABASE):

    db_data = convert_list_to_db_value_string(data)

    with dataset.connect(database) as db:
        result = db.query("INSERT IGNORE INTO %s " "VALUES %s " % (table, db_data))

    return result


def insert_item():
    pass


def update_list():
    pass


def update_item():
    pass


def delete_list():
    pass


def delete_item():
    pass


# enhanced CRUD
def write_index_content_to_stock_table(stocks, test=None):
    database = cst.DATABASE if not test else cst.DATABASE

    with dataset.connect(database) as db:
        try:
            for stock in stocks:
                db[cst.TABLE_STOCKS].insert_ignore(stock, ["URI"])
        except sqlalchemy.exc.IntegrityError:
            pass


def write_stock_to_index_contents_table(index_contents, test=None):
    database = cst.DATABASE if not test else cst.DATABASE
    with dataset.connect(database) as db:
        try:
            db[cst.TABLE_INDEX_CONTENTS].insert_many(index_contents)
        except sqlalchemy.exc.IntegrityError:
            pass


# List Calculations
def create_all_index_url_list(base_url, database=cst.DATABASE):
    index_list = get_list(
        table=cst.TABLE_INDIZES, columns=cst.COLUMN_URI, database=database
    )
    url_list = [base_url + index for index in index_list]
    return url_list


def create_active_index_url_list(base_url):
    index_list = get_list(
        table=cst.TABLE_INDIZES,
        columns=cst.COLUMN_URI,
        condition=[cst.COLUMN_ACTIVE, b"1"],
    )
    url_list = [base_url + index for index in index_list]
    return url_list


def create_stock_history_url_list(base_url):
    stock_history_list = get_list(
        table=cst.TABLE_STOCKS, columns=[cst.COLUMN_URI, cst.COLUMN_MARKET_PLACE]
    )
    url_list = []
    for stock in stock_history_list:
        stock_uri, market_place = stock[0][:-6], stock[1]
        if market_place is None or market_place == "None":
            market_place = cst.EXCHANGE_APPENDIX
        url_list.append(base_url + stock_uri + "/" + market_place)
    return url_list


def create_stock_overview_url_list(base_url):
    stock_list = get_list(table=cst.TABLE_STOCKS, columns=cst.COLUMN_URI)
    url_list = [base_url + stock for stock in stock_list]
    return url_list


def create_stock_info_url_list(base_url):
    stock_list = get_list(table=cst.TABLE_STOCKS, columns=cst.COLUMN_URI)
    url_list = [base_url + stock[:-6] for stock in stock_list]
    return url_list


def write_index_content_list_to_db(index_content, index_name):
    current_date = date.get_current_date()
    stocks = [dict(Name=stock[0], URI=stock[1]) for stock in index_content]
    write_index_content_to_stock_table(stocks)

    index_contents = [
        dict(IndexURI=index_name, AktienURI=stock[1], Abrufdatum=current_date)
        for stock in index_content
    ]
    write_stock_to_index_contents_table(index_contents)
    return True


# Information Gathering
def get_latest_date_from_index_history(index_uri):
    return get_item(
        table=cst.TABLE_INDEX_HISTORIES,
        column="max(Datum)",
        condition=[cst.COLUMN_INDEX_URI, index_uri],
    )


def get_latest_date_from_stock_history(stock_uri):
    return get_item(
        table=cst.TABLE_STOCKS_HISTORIES,
        column="max(Datum)",
        condition=[cst.COLUMN_STOCK_URI, stock_uri],
    )


# Conversions
def convert_list_to_db_value_string(data):
    db_data_string = ""
    for row in data:
        db_data_string += "('%s'), " % "', '".join(row)

    return db_data_string[:-2]


# ToDo Refactor below


def write_index_history_to_db(index_history, index_uri, database=cst.DATABASE):
    with dataset.connect(database) as db:
        for item in index_history:
            date_ = date.string_to_date(item[0])
            try:
                start = float(item[1].replace(".", "").replace(",", "."))
            except ValueError:
                logger.warning(
                    "ValueError: Missing start value for %s at %s"
                    % (index_uri, str(date_))
                )
                start = None
            try:
                end = float(item[2].replace(".", "").replace(",", "."))
            except ValueError:
                logger.warning(
                    "ValueError: Missing end value for %s at %s"
                    % (index_uri, str(date_))
                )
                end = None
            try:
                db[cst.TABLE_INDEX_HISTORIES].insert(
                    dict(
                        IndexURI=index_uri,
                        Datum=date_,
                        Eroeffnungswert=start,
                        Schlusswert=end,
                    )
                )
            except sqlalchemy.exc.IntegrityError:
                logger.warning(
                    "Write Index History to DB: Integrity Error with Item: %s"
                    % index_uri
                )
                pass


def write_stock_history_to_db(stock_history, stock_uri, database=cst.DATABASE):
    with dataset.connect(database) as db:
        for item in stock_history:
            date_ = date.string_to_date(item[0])
            try:
                start = float(item[1].replace(".", "").replace(",", "."))
            except ValueError:
                logger.warning(
                    "ValueError: Missing start value for %s at %s"
                    % (stock_uri, str(date_))
                )
                start = None
            try:
                end = float(item[2].replace(".", "").replace(",", "."))
            except ValueError:
                logger.warning(
                    "ValueError: Missing end value for %s at %s"
                    % (stock_uri, str(date_))
                )
                end = None
            try:
                db[cst.TABLE_STOCKS_HISTORIES].insert(
                    dict(
                        AktienURI=stock_uri,
                        Datum=date_,
                        Eroeffnungswert=start,
                        Schlusswert=end,
                    )
                )
            except sqlalchemy.exc.IntegrityError:
                pass


def write_stock_overview_history_to_db(stock_history, stock_uri, database=cst.DATABASE):
    with dataset.connect(database) as db:
        for item in stock_history:
            date_ = date.string_to_date(item[0])
            try:
                end = float(item[1].replace(".", "").replace(",", "."))
            except ValueError:
                logger.warning(
                    "ValueError: Missing end value for %s at %s"
                    % (stock_uri, str(date_))
                )
                end = None
            try:
                db[cst.TABLE_STOCKS_HISTORIES].insert(
                    dict(AktienURI=stock_uri, Datum=date_, Schlusswert=end)
                )
            except sqlalchemy.exc.IntegrityError:
                pass
    return True


def write_single_overview_data_to_db(
    stock_uri,
    market_cap,
    stock_indizes,
    stock_sectors,
    market_place,
    database=cst.DATABASE,
):
    current_date = date.get_current_date()
    with dataset.connect(database) as db:
        try:
            db[cst.TABLE_COMPANY_DATA].insert(
                dict(
                    AktienURI=stock_uri,
                    Datum=current_date,
                    Marktkapitalisierung=market_cap,
                    Indizes=str(stock_indizes),
                    Branchen=str(stock_sectors),
                )
            )
        except sqlalchemy.exc.IntegrityError:
            db.query(
                "UPDATE %s SET "
                'Marktkapitalisierung = "%s", '
                'Indizes = "%s", '
                'Branchen = "%s" '
                'WHERE AktienURI = "%s" AND Datum = "%s"'
                % (
                    cst.TABLE_COMPANY_DATA,
                    market_cap,
                    str(stock_indizes),
                    str(stock_sectors),
                    stock_uri,
                    current_date,
                )
            )
            pass
        try:
            db.query(
                "UPDATE %s SET "
                'Handelsplatz = "%s" '
                'WHERE URI = "%s"' % (cst.TABLE_STOCKS, market_place, stock_uri)
            )
        except:
            logger.exception("Exception at Marketplace Insertion")
            pass


def write_single_balance_data_to_db(
    stock_uri,
    result_after_tax,
    operative_result,
    sales_revenue,
    total_assets,
    equity_capital,
    eps_minus_3,
    eps_minus_2,
    eps_minus_1,
    database=cst.DATABASE,
):
    current_date = date.get_current_date()
    with dataset.connect(database) as db:
        try:
            db[cst.TABLE_COMPANY_DATA].insert(
                dict(
                    AktienURI=stock_uri,
                    Datum=current_date,
                    Ergebnis_nach_Steuern=result_after_tax,
                    Operatives_Ergebnis=operative_result,
                    Umsatzerloese=sales_revenue,
                    Bilanzsumme=total_assets,
                    Eigenkapital=equity_capital,
                    EPS_minus_3=eps_minus_3,
                    EPS_minus_2=eps_minus_2,
                    EPS_minus_1=eps_minus_1,
                )
            )
        except sqlalchemy.exc.IntegrityError:
            db.query(
                "UPDATE %s SET "
                "Ergebnis_nach_Steuern = %s, "
                "Operatives_Ergebnis = %s, "
                "Umsatzerloese = %s, "
                "Bilanzsumme = %s, "
                "Eigenkapital = %s, "
                "EPS_minus_3 = %s, "
                "EPS_minus_2 = %s, "
                "EPS_minus_1 = %s "
                'WHERE AktienURI = "%s" AND Datum = "%s"'
                % (
                    cst.TABLE_COMPANY_DATA,
                    result_after_tax,
                    operative_result,
                    sales_revenue,
                    total_assets,
                    equity_capital,
                    eps_minus_3,
                    eps_minus_2,
                    eps_minus_1,
                    stock_uri,
                    current_date,
                )
            )
            pass


def write_single_estimate_data_to_db(
    stock_uri, eps_0, eps_plus_1, database=cst.DATABASE
):
    current_date = date.get_current_date()
    with dataset.connect(database) as db:
        try:
            db[cst.TABLE_COMPANY_DATA].insert(
                dict(
                    AktienURI=stock_uri,
                    Datum=current_date,
                    EPS_0=eps_0,
                    EPS_plus_1=eps_plus_1,
                )
            )
        except sqlalchemy.exc.IntegrityError:
            db.query(
                "UPDATE %s SET "
                "EPS_0 = %s, "
                "EPS_plus_1 = %s "
                'WHERE AktienURI = "%s" AND Datum = "%s"'
                % (cst.TABLE_COMPANY_DATA, eps_0, eps_plus_1, stock_uri, current_date)
            )
            pass


def write_single_targets_data_to_db(
    stock_uri, analyst_buy, analyst_hold, analyst_sell, database=cst.DATABASE
):
    current_date = date.get_current_date()
    with dataset.connect(database) as db:
        try:
            db[cst.TABLE_COMPANY_DATA].insert(
                dict(
                    AktienURI=stock_uri,
                    Datum=current_date,
                    Analysten_Buy=analyst_buy,
                    Analysten_Hold=analyst_hold,
                    Analysten_Sell=analyst_sell,
                )
            )
        except sqlalchemy.exc.IntegrityError:
            db.query(
                "UPDATE %s SET "
                "Analysten_Buy = %s, "
                "Analysten_Hold = %s, "
                "Analysten_Sell = %s "
                'WHERE AktienURI = "%s" AND Datum = "%s"'
                % (
                    cst.TABLE_COMPANY_DATA,
                    analyst_buy,
                    analyst_hold,
                    analyst_sell,
                    stock_uri,
                    current_date,
                )
            )
            pass


def write_single_stock_dates_data_to_db(stock_uri, figures_date, database=cst.DATABASE):
    with dataset.connect(database) as db:
        try:
            db[cst.TABLE_STOCK_DATES].insert(
                dict(
                    AktienURI=stock_uri,
                    Datum=figures_date,
                    Terminart="Quarterly/Yearly",
                )
            )
        except sqlalchemy.exc.IntegrityError:
            db.query(
                "UPDATE %s SET "
                "Datum = %s "
                'WHERE AktienURI = "%s"'
                % (cst.TABLE_COMPANY_DATA, figures_date, stock_uri)
            )
            pass


def write_date_list_to_db(date_list):
    """
    Datelist are e.g.:
            [["adidas AG", "2018-11-07", "Quartalszahlen", "Future"],
             ["adidas AG", "2018-03-07", "Quartalszahlen", "Future"],
             ["adidas AG", "2019-05-02", "Quartalszahlen", "Future"],
            ]
    or:

            [["adidas AG", "2018-08-09", "Q2 2018 Earnings Release", "Past"],
             ["adidas AG", "2018-05-09", "Hauptversammlung", "Past"],
             ["adidas AG", "2017-11-09", "Q3 2017", "Past"]]

    :param date_list:
    :return:
    """


# Levermann 01


def get_earnings_after_tax(stock_uri, database=cst.DATABASE):
    with dataset.connect(database) as db:
        try:
            results = db.query(
                "SELECT %s FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
                % (cst.COLUMN_EARNINGS_AT, cst.TABLE_COMPANY_DATA, stock_uri)
            )
            return float([item for item in results][0][cst.COLUMN_EARNINGS_AT])
        except:
            logger.exception("Exception at get_earnings_after_tax for %s" % stock_uri)
            pass


def get_equity_capital(stock_uri, database=cst.DATABASE):
    with dataset.connect(database) as db:
        try:
            results = db.query(
                "SELECT %s FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
                % (cst.COLUMN_EQUITY_CAPITAL, cst.TABLE_COMPANY_DATA, stock_uri)
            )
            return float([item for item in results][0][cst.COLUMN_EQUITY_CAPITAL])
        except:
            logger.exception("Exception at get_equity_capital for %s" % stock_uri)
            pass


def save_roe_to_db(stock_uri, roe, lev_score, database=cst.DATABASE):
    current_date = date.get_current_date()
    with dataset.connect(database) as db:
        try:
            db[cst.TABLE_LEVERMANN].insert(
                dict(
                    AktienURI=stock_uri,
                    Datum=current_date,
                    Lev01_Wert=roe,
                    Lev01_Score=lev_score,
                )
            )
        except sqlalchemy.exc.IntegrityError:
            db.query(
                "UPDATE %s SET "
                "Lev01_Wert = %s, "
                "Lev01_Score = %s "
                'WHERE AktienURI = "%s" AND Datum = "%s"'
                % (cst.TABLE_LEVERMANN, roe, lev_score, stock_uri, current_date)
            )
            pass


# Levermann 02


def get_operative_result(stock_uri, database=cst.DATABASE):
    with dataset.connect(database) as db:
        try:
            results = db.query(
                "SELECT %s FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
                % (cst.COLUMN_OPERATIVE_RESULT, cst.TABLE_COMPANY_DATA, stock_uri)
            )
            return float([item for item in results][0][cst.COLUMN_OPERATIVE_RESULT])
        except:
            logger.exception("Exception at get_operative_result for %s" % stock_uri)
            pass


def get_sales_revenue(stock_uri, database=cst.DATABASE):
    with dataset.connect(database) as db:
        try:
            results = db.query(
                "SELECT %s FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
                % (cst.COLUMN_SALES_REVENUE, cst.TABLE_COMPANY_DATA, stock_uri)
            )
            return float([item for item in results][0][cst.COLUMN_SALES_REVENUE])
        except:
            logger.exception("Exception at get_sales_revenue for %s" % stock_uri)
            pass


def check_is_financial_company(stock_uri, database=cst.DATABASE):
    fin_list = cst.FINANCE_SECTORS
    with dataset.connect(database) as db:
        try:
            results = db.query(
                "SELECT %s FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
                % (cst.COLUMN_SECTORS, cst.TABLE_COMPANY_DATA, stock_uri)
            )
            result_list = [item for item in results][0][cst.COLUMN_SECTORS]
            return any(i in result_list for i in fin_list)
        except:
            logger.exception(
                "Exception at check_is_financial_company for %s" % stock_uri
            )
            pass


def save_ebit_to_db(stock_uri, ebit, lev_score, database=cst.DATABASE):
    current_date = date.get_current_date()
    with dataset.connect(database) as db:
        try:
            db[cst.TABLE_LEVERMANN].insert(
                dict(
                    AktienURI=stock_uri,
                    Datum=current_date,
                    Lev02_Wert=ebit,
                    Lev02_Score=lev_score,
                )
            )
        except sqlalchemy.exc.IntegrityError:
            db.query(
                "UPDATE %s SET "
                "Lev02_Wert = %s, "
                "Lev02_Score = %s "
                'WHERE AktienURI = "%s" AND Datum = "%s"'
                % (cst.TABLE_LEVERMANN, ebit, lev_score, stock_uri, current_date)
            )
            pass


# Levermann 03


def get_balance(stock_uri, database=cst.DATABASE):
    with dataset.connect(database) as db:
        try:
            results = db.query(
                "SELECT %s FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
                % (cst.COLUMN_BALANCE, cst.TABLE_COMPANY_DATA, stock_uri)
            )
            return float([item for item in results][0][cst.COLUMN_BALANCE])
        except:
            logger.exception("Exception at get_balance for %s" % stock_uri)
            pass


def save_equity_ratio_to_db(stock_uri, equity_ratio, lev_score, database=cst.DATABASE):
    current_date = date.get_current_date()
    with dataset.connect(database) as db:
        try:
            db[cst.TABLE_LEVERMANN].insert(
                dict(
                    AktienURI=stock_uri,
                    Datum=current_date,
                    Lev03_Wert=equity_ratio,
                    Lev03_Score=lev_score,
                )
            )
        except sqlalchemy.exc.IntegrityError:
            db.query(
                "UPDATE %s SET "
                "Lev03_Wert = %s, "
                "Lev03_Score = %s "
                'WHERE AktienURI = "%s" AND Datum = "%s"'
                % (
                    cst.TABLE_LEVERMANN,
                    equity_ratio,
                    lev_score,
                    stock_uri,
                    current_date,
                )
            )
            pass


# Levermann 04 & 05


def get_latest_stock_price(stock_uri, database=cst.DATABASE):
    with dataset.connect(database) as db:
        try:
            results = db.query(
                "SELECT %s FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
                % (cst.COLUMN_CLOSING_VALUE, cst.TABLE_STOCKS_HISTORIES, stock_uri)
            )
            return float([item for item in results][0][cst.COLUMN_CLOSING_VALUE])
        except:
            logger.exception(
                "Unhandled Exception at get_latest_stock_price for %s" % stock_uri
            )
            pass


def get_eps(stock_uri, database=cst.DATABASE):
    with dataset.connect(database) as db:
        try:
            results = db.query(
                "SELECT * FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
                % (cst.TABLE_COMPANY_DATA, stock_uri)
            )
            eps_s = [item for item in results][0]
            eps_list = [
                float(eps_s[cst.COLUMN_EPS_M3]),
                float(eps_s[cst.COLUMN_EPS_M2]),
                float(eps_s[cst.COLUMN_EPS_M1]),
                float(eps_s[cst.COLUMN_EPS_0]),
                float(eps_s[cst.COLUMN_EPS_P1]),
            ]
            return eps_list
        except:
            logger.exception("Unhandled Exception at get_eps for %s" % stock_uri)
            pass


def get_older_eps(stock_uri, database=cst.DATABASE):
    with dataset.connect(database) as db:
        try:
            results = db.query(
                "SELECT * FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
                % (cst.TABLE_COMPANY_DATA, stock_uri)
            )
            eps_s = [item for item in results][1]
            eps_list = [
                float(eps_s[cst.COLUMN_EPS_M3]),
                float(eps_s[cst.COLUMN_EPS_M2]),
                float(eps_s[cst.COLUMN_EPS_M1]),
                float(eps_s[cst.COLUMN_EPS_0]),
                float(eps_s[cst.COLUMN_EPS_P1]),
            ]
            return eps_list
        except:
            logger.exception("Exception at get_older_eps for %s" % stock_uri)
            pass


def save_kgv5_to_db(stock_uri, kgv5, kgv5_score, database=cst.DATABASE):
    current_date = date.get_current_date()
    with dataset.connect(database) as db:
        try:
            db[cst.TABLE_LEVERMANN].insert(
                dict(
                    AktienURI=stock_uri,
                    Datum=current_date,
                    Lev04_Wert=kgv5,
                    Lev04_Score=kgv5_score,
                )
            )
        except sqlalchemy.exc.IntegrityError:
            db.query(
                "UPDATE %s SET "
                "Lev04_Wert = %s, "
                "Lev04_Score = %s "
                'WHERE AktienURI = "%s" AND Datum = "%s"'
                % (cst.TABLE_LEVERMANN, kgv5, kgv5_score, stock_uri, current_date)
            )
            pass


def save_kgv0_to_db(stock_uri, kgv0, kgv0_score, database=cst.DATABASE):
    current_date = date.get_current_date()
    with dataset.connect(database) as db:
        try:
            db[cst.TABLE_LEVERMANN].insert(
                dict(
                    AktienURI=stock_uri,
                    Datum=current_date,
                    Lev05_Wert=kgv0,
                    Lev05_Score=kgv0_score,
                )
            )
        except sqlalchemy.exc.IntegrityError:
            db.query(
                "UPDATE %s SET "
                "Lev05_Wert = %s, "
                "Lev05_Score = %s "
                'WHERE AktienURI = "%s" AND Datum = "%s"'
                % (cst.TABLE_LEVERMANN, kgv0, kgv0_score, stock_uri, current_date)
            )
            pass


# Levermann 06


def get_analyst_ratings(stock_uri, database=cst.DATABASE):
    with dataset.connect(database) as db:
        try:
            results = db.query(
                "SELECT * FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
                % (cst.TABLE_COMPANY_DATA, stock_uri)
            )
            ratings = [item for item in results][0]
            rating_list = [
                int(ratings[cst.COLUMN_ANALYST_BUY]),
                int(ratings[cst.COLUMN_ANALYST_HOLD]),
                int(ratings[cst.COLUMN_ANALYST_SELL]),
            ]
            return rating_list
        except:
            logger.exception(
                "Unhandled Exception at get_analyst_ratings for %s" % stock_uri
            )
            pass


def save_rating_to_db(stock_uri, rating, rating_score, database=cst.DATABASE):
    current_date = date.get_current_date()
    with dataset.connect(database) as db:
        try:
            db[cst.TABLE_LEVERMANN].insert(
                dict(
                    AktienURI=stock_uri,
                    Datum=current_date,
                    Lev06_Wert=rating,
                    Lev06_Score=rating_score,
                )
            )
        except sqlalchemy.exc.IntegrityError:
            db.query(
                "UPDATE %s SET "
                "Lev06_Wert = %s, "
                "Lev06_Score = %s "
                'WHERE AktienURI = "%s" AND Datum = "%s"'
                % (cst.TABLE_LEVERMANN, rating, rating_score, stock_uri, current_date)
            )
            pass


def is_small_cap(stock_uri, database=cst.DATABASE):
    with dataset.connect(database) as db:
        try:
            market_cap_results = db.query(
                "SELECT * FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
                % (cst.TABLE_COMPANY_DATA, stock_uri)
            )
            market_cap = float(
                [item for item in market_cap_results][0][cst.COLUMN_MARKET_CAP]
            )
            if market_cap > cst.MARKET_CAP_THRESHOLD:
                return False
            else:
                indizes_list = get_indices_of_stock(stock_uri)
                return not any(
                    i in indizes_list for i in cst.LARGE_CAPS_INDIZES
                )  # ToDO abhängig von Spalte LargeCapIndex machen, dann auch in Constants löschen

        except:
            logger.exception("Unhandled Exception at is_small_cap for %s" % stock_uri)
            pass


# Levermann 07


def get_quarterly_date(stock_uri, database=cst.DATABASE):
    with dataset.connect(database) as db:
        try:
            results = db.query(
                "SELECT * FROM %s WHERE AktienURI = '%s'"
                % (cst.TABLE_STOCK_DATES, stock_uri)
            )
            quarterly_date = [item for item in results][0][cst.COLUMN_DATE]
            return quarterly_date
        except TypeError:
            logger.error("TypeError in get_quaterly_date at %s" % stock_uri)
        except:
            logger.exception("Exception at get_quarterly_date for %s" % stock_uri)
            pass


def get_closing_stock_price(request_date, stock_uri, database=cst.DATABASE):
    with dataset.connect(database) as db:
        try:
            results = db.query(
                "SELECT * FROM %s "
                "WHERE AktienURI = '%s' and Datum <= '%s' "
                "ORDER BY Datum DESC"
                % (cst.TABLE_STOCKS_HISTORIES, stock_uri, request_date)
            )
            result = [item for item in results][0]
            closing_price = result[cst.COLUMN_CLOSING_VALUE]
            actual_date = result[cst.COLUMN_DATE]
            return closing_price, actual_date
        except IndexError:
            logger.error(
                "IndexError while getting closing_stock_price for %s. "
                "The sql_query returns an empty result."
                "Probably is there no date in database before request_date"
            )
            pass
        except:
            logger.exception(
                "Unhandled Exception at get_closing_stock_price for %s" % stock_uri
            )
            pass


def get_closing_index_price(request_date, index_uri, database=cst.DATABASE):
    with dataset.connect(database) as db:
        try:
            results = db.query(
                "SELECT * FROM %s "
                "WHERE IndexURI = '%s' and Datum <= '%s' "
                "ORDER BY Datum DESC"
                % (cst.TABLE_INDEX_HISTORIES, index_uri, request_date)
            )
            result = [item for item in results][0]
            closing_price = result[cst.COLUMN_CLOSING_VALUE]
            actual_date = result[cst.COLUMN_DATE]
            return closing_price, actual_date
        except:
            logger.exception(
                "Unhandled Exception at get_closing_index_price for %s" % index_uri
            )
            pass


# ToDo Recreate next two Methods, check index of Stock through Companydata-Table
def get_main_index_of_stock(stock_uri, database=cst.DATABASE):
    with dataset.connect(database) as db:
        try:
            results = db.query(
                "SELECT * FROM %s WHERE AktienURI = '%s'"
                % (cst.TABLE_INDEX_CONTENTS, stock_uri)
            )
            index_uri = [item for item in results][0][cst.COLUMN_INDEX_URI]
            return index_uri
        except:
            logger.exception(
                "Unhandled Exception at get_index_of_stock for %s" % stock_uri
            )
            pass


def get_indices_of_stock(stock_uri, database=cst.DATABASE):
    with dataset.connect(database) as db:
        try:
            results = db.query(
                "SELECT * FROM %s WHERE AktienURI = '%s'"
                % (cst.TABLE_INDEX_CONTENTS, stock_uri)
            )
            index_uri = {item[cst.COLUMN_INDEX_URI] for item in results}
            return sorted(index_uri)
        except:
            logger.exception(
                "Unhandled Exception at get_indizes_of_stock for %s" % stock_uri
            )
            pass


def save_quarterly_reaction_to_db(
    stock_uri, quarterly_diff, lev_score, database=cst.DATABASE
):
    current_date = date.get_current_date()
    with dataset.connect(database) as db:
        try:
            db[cst.TABLE_LEVERMANN].insert(
                dict(
                    AktienURI=stock_uri,
                    Datum=current_date,
                    Lev07_Wert=quarterly_diff,
                    Lev07_Score=lev_score,
                )
            )
        except sqlalchemy.exc.IntegrityError:
            db.query(
                "UPDATE %s SET "
                "Lev07_Wert = %s, "
                "Lev07_Score = %s "
                'WHERE AktienURI = "%s" AND Datum = "%s"'
                % (
                    cst.TABLE_LEVERMANN,
                    quarterly_diff,
                    lev_score,
                    stock_uri,
                    current_date,
                )
            )
            pass


# Levermann 08


def save_eps_revision_to_db(stock_uri, eps_diff, lev_score, database=cst.DATABASE):
    current_date = date.get_current_date()
    with dataset.connect(database) as db:
        try:
            db[cst.TABLE_LEVERMANN].insert(
                dict(
                    AktienURI=stock_uri,
                    Datum=current_date,
                    Lev08_Wert=eps_diff,
                    Lev08_Score=lev_score,
                )
            )
        except sqlalchemy.exc.IntegrityError:
            db.query(
                "UPDATE %s SET "
                "Lev08_Wert = %s, "
                "Lev08_Score = %s "
                'WHERE AktienURI = "%s" AND Datum = "%s"'
                % (cst.TABLE_LEVERMANN, eps_diff, lev_score, stock_uri, current_date)
            )
            pass


# Levermann 09-11


def save_6_months_ratio_to_db(stock_uri, ratio, lev_score, database=cst.DATABASE):
    current_date = date.get_current_date()
    with dataset.connect(database) as db:
        try:
            db[cst.TABLE_LEVERMANN].insert(
                dict(
                    AktienURI=stock_uri,
                    Datum=current_date,
                    Lev09_Wert=ratio,
                    Lev09_Score=lev_score,
                )
            )
        except sqlalchemy.exc.IntegrityError:
            db.query(
                "UPDATE %s SET "
                "Lev09_Wert = %s, "
                "Lev09_Score = %s "
                'WHERE AktienURI = "%s" AND Datum = "%s"'
                % (cst.TABLE_LEVERMANN, ratio, lev_score, stock_uri, current_date)
            )
            pass


def save_12_months_ratio_to_db(stock_uri, ratio, lev_score, database=cst.DATABASE):
    current_date = date.get_current_date()
    with dataset.connect(database) as db:
        try:
            db[cst.TABLE_LEVERMANN].insert(
                dict(
                    AktienURI=stock_uri,
                    Datum=current_date,
                    Lev10_Wert=ratio,
                    Lev10_Score=lev_score,
                )
            )
        except sqlalchemy.exc.IntegrityError:
            db.query(
                "UPDATE %s SET "
                "Lev10_Wert = %s, "
                "Lev10_Score = %s "
                'WHERE AktienURI = "%s" AND Datum = "%s"'
                % (cst.TABLE_LEVERMANN, ratio, lev_score, stock_uri, current_date)
            )
            pass


def save_momentum_to_db(stock_uri, lev_score, database=cst.DATABASE):
    current_date = date.get_current_date()
    with dataset.connect(database) as db:
        try:
            db[cst.TABLE_LEVERMANN].insert(
                dict(AktienURI=stock_uri, Datum=current_date, Lev11_Score=lev_score)
            )
        except sqlalchemy.exc.IntegrityError:
            db.query(
                "UPDATE %s SET "
                "Lev11_Score = %s "
                'WHERE AktienURI = "%s" AND Datum = "%s"'
                % (cst.TABLE_LEVERMANN, lev_score, stock_uri, current_date)
            )
            pass


# Levermann 12


def calculate_list_changes(value_list):
    stock_changes = []
    for i in range(len(value_list) - 1):
        stock_change = (value_list[i + 1] / value_list[i]) - 1
        stock_changes.append(round(stock_change, 2))
    return stock_changes


def save_reversal_to_db(stock_uri, diff, lev_score, database=cst.DATABASE):
    current_date = date.get_current_date()
    with dataset.connect(database) as db:
        try:
            db[cst.TABLE_LEVERMANN].insert(
                dict(
                    AktienURI=stock_uri,
                    Datum=current_date,
                    Lev12_Wert=diff,
                    Lev12_Score=lev_score,
                )
            )
        except sqlalchemy.exc.IntegrityError:
            db.query(
                "UPDATE %s SET "
                "Lev12_Wert = %s, "
                "Lev12_Score = %s "
                'WHERE AktienURI = "%s" AND Datum = "%s"'
                % (cst.TABLE_LEVERMANN, diff, lev_score, stock_uri, current_date)
            )
            pass


# Levermann 13


def save_profit_growth_to_db(stock_uri, diff, lev_score, database=cst.DATABASE):
    current_date = date.get_current_date()
    with dataset.connect(database) as db:
        try:
            db[cst.TABLE_LEVERMANN].insert(
                dict(
                    AktienURI=stock_uri,
                    Datum=current_date,
                    Lev13_Wert=diff,
                    Lev13_Score=lev_score,
                )
            )
        except sqlalchemy.exc.IntegrityError:
            db.query(
                "UPDATE %s SET "
                "Lev13_Wert = %s, "
                "Lev13_Score = %s "
                'WHERE AktienURI = "%s" AND Datum = "%s"'
                % (cst.TABLE_LEVERMANN, diff, lev_score, stock_uri, current_date)
            )
            pass


def get_levermann_buy(database=cst.DATABASE):
    with dataset.connect(database) as db:
        try:
            logger.info("Query DB Levermann BUY View")
            results = db.query("SELECT * " "FROM %s " % cst.VIEW_LEVERMANN_BUY)
            return results
        except:
            logger.exception("Exception at get_levermann_buy")
            pass


def get_levermann_hold(database=cst.DATABASE):
    with dataset.connect(database) as db:
        try:
            results = db.query("SELECT * " "FROM %s " % cst.VIEW_LEVERMANN_HOLD)
            return results
        except:
            logger.exception("Exception at get_levermann_hold")
            pass
