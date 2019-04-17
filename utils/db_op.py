from loguru import logger

from utils import date_op as date
from utils import constants as cst
from sqlalchemy.exc import IntegrityError

import dataset


# CRUD
def get_list(table, columns, condition=None, order=None, database=cst.DATABASE):
    order_by = "ORDER BY %s %s " % (order[0], order[1]) if order is not None else ""
    where = (
        "WHERE %s = '%s' " % (condition[0], condition[1])
        if condition is not None
        else ""
    )
    from_table = "FROM %s " % table

    with dataset.connect(database) as db:
        if isinstance(columns, list):
            select = "SELECT %s " % ",".join(columns)
            results = db.query("%s %s %s %s" % (select, from_table, where, order_by))
            result = [[item[column] for column in columns] for item in results]
        else:
            select = "SELECT %s " % columns
            results = db.query("%s %s %s %s" % (select, from_table, where, order_by))
            result = [item[columns] for item in results]

    return result

    #
    # if not condition:
    #     if isinstance(columns, str):
    #         with dataset.connect(database) as db:
    #             return [item[columns] for item in db[table]]
    #     elif isinstance(columns, list):
    #         with dataset.connect(database) as db:
    #             return [[item[column] for column in columns] for item in db[table]]
    #
    # else:
    #     if isinstance(columns, str):
    #         with dataset.connect(database) as db:
    #             return [
    #                 item[columns]
    #                 for item in db[table]
    #                 if item[condition[0]] == condition[1]
    #             ]
    #     elif isinstance(columns, list):
    #         with dataset.connect(database) as db:
    #             return [
    #                 [item[column] for column in columns]
    #                 for item in db[table]
    #                 if item[condition[0]] == condition[1]
    #             ]


def get_item(table, column, condition=None, order=None, database=cst.DATABASE):
    order_by = "ORDER BY %s %s" % (order[0], order[1]) if order is not None else ""
    where = (
        "WHERE %s = '%s' " % (condition[0], condition[1])
        if condition is not None
        else ""
    )

    with dataset.connect(database) as db:
        results = db.query(
            "SELECT %s as result FROM %s %s %s" % (column, table, where, order_by)
        )
        try:
            result = [item for item in results][0]
        except IndexError:
            logger.info(
                "Index Error while trying to get first Item of Result, "
                "probably no data for search found"
            )
            return None
    return result["result"]


def insert_list(table, data, database=cst.DATABASE):

    db_data = convert_list_to_db_value_string(data)

    with dataset.connect(database) as db:
        result = db.query("INSERT IGNORE INTO %s " "VALUES %s " % (table, db_data))

    return result


def upsert_item(
    table,
    primary_keys,
    database=cst.DATABASE,
    uri=None,
    active=None,
    large_cap=None,
    index_uri=None,
    index_name=None,
    pages=None,
    stock_uri=None,
    equity_capital=None,
    earnings_after_tax=None,
    operative_result=None,
    sales_revenue=None,
    balance=None,
    start_value=None,
    closing_value=None,
    eps_m3=None,
    eps_m2=None,
    eps_m1=None,
    eps_0=None,
    eps_p1=None,
    analyst_buy=None,
    analyst_hold=None,
    analyst_sell=None,
    market_cap=None,
    market_place=None,
    current_date=None,
    quarterly=None,
    stock_sectors=None,
    stock_indices=None,
    lev_01_val=None,
    lev_01_sco=None,
    lev_02_val=None,
    lev_02_sco=None,
    lev_03_val=None,
    lev_03_sco=None,
    lev_04_val=None,
    lev_04_sco=None,
    lev_05_val=None,
    lev_05_sco=None,
    lev_06_val=None,
    lev_06_sco=None,
    lev_07_val=None,
    lev_07_sco=None,
    lev_08_val=None,
    lev_08_sco=None,
    lev_09_val=None,
    lev_09_sco=None,
    lev_10_val=None,
    lev_10_sco=None,
    lev_11_val=None,
    lev_11_sco=None,
    lev_12_val=None,
    lev_12_sco=None,
    lev_13_val=None,
    lev_13_sco=None,
):

    default_dict = dict(
        zip(
            cst.ALL_COLUMNS,
            [
                uri,
                active,
                large_cap,
                index_uri,
                index_name,
                pages,
                stock_uri,
                earnings_after_tax,
                equity_capital,
                operative_result,
                sales_revenue,
                balance,
                start_value,
                closing_value,
                eps_m3,
                eps_m2,
                eps_m1,
                eps_0,
                eps_p1,
                analyst_buy,
                analyst_hold,
                analyst_sell,
                market_cap,
                market_place,
                current_date,
                quarterly,
                stock_sectors,
                stock_indices,
                lev_01_val,
                lev_01_sco,
                lev_02_val,
                lev_02_sco,
                lev_03_val,
                lev_03_sco,
                lev_04_val,
                lev_04_sco,
                lev_05_val,
                lev_05_sco,
                lev_06_val,
                lev_06_sco,
                lev_07_val,
                lev_07_sco,
                lev_08_val,
                lev_08_sco,
                lev_09_val,
                lev_09_sco,
                lev_10_val,
                lev_10_sco,
                lev_11_val,
                lev_11_sco,
                lev_12_val,
                lev_12_sco,
                lev_13_val,
                lev_13_sco,
            ],
        )
    )

    upsert_dict = {k: v for k, v in default_dict.items() if v is not None}

    with dataset.connect(database) as db:
        try:
            db[table].upsert(upsert_dict, primary_keys)

        except:
            logger.warning("Unhandled Upsert Error")
    pass


def update_item(
    table,
    primary_keys,
    database=cst.DATABASE,
    uri=None,
    active=None,
    large_cap=None,
    index_uri=None,
    pages=None,
    stock_uri=None,
    earnings_at=None,
    equity_capital=None,
    operative_result=None,
    sales_revenue=None,
    balance=None,
    start_value=None,
    closing_value=None,
    eps_m3=None,
    eps_m2=None,
    eps_m1=None,
    eps_0=None,
    eps_p1=None,
    analyst_buy=None,
    analyst_hold=None,
    analyst_sell=None,
    market_cap=None,
    market_place=None,
    current_date=None,
    quarterly=None,
    stock_sectors=None,
    stock_indices=None,
):

    default_dict = dict(
        zip(
            cst.ALL_COLUMNS,
            [
                uri,
                active,
                large_cap,
                index_uri,
                pages,
                stock_uri,
                earnings_at,
                equity_capital,
                operative_result,
                sales_revenue,
                balance,
                start_value,
                closing_value,
                eps_m3,
                eps_m2,
                eps_m1,
                eps_0,
                eps_p1,
                analyst_buy,
                analyst_hold,
                analyst_sell,
                market_cap,
                market_place,
                current_date,
                quarterly,
                str(stock_sectors),
                str(stock_indices),
            ],
        )
    )

    upsert_dict = {k: v for k, v in default_dict.items() if v is not None}

    with dataset.connect(database) as db:
        try:
            db[table].update(upsert_dict, primary_keys)
        except:
            logger.warning("Unhandled Update Error")
    pass


def delete_list():
    pass


def delete_item():
    pass


# Enhanced CRUD
#
# get_list Calculations
def create_active_index_url_list(base_url, database=cst.DATABASE):
    index_list = get_list(
        table=cst.TABLE_INDIZES,
        columns=cst.COLUMN_URI,
        condition=[cst.COLUMN_ACTIVE, 1],
        database=database,
    )
    url_list = [base_url + index for index in index_list]
    return url_list


def create_stock_url_list(base_url, database=cst.DATABASE):
    stock_list = get_list(
        table=cst.TABLE_STOCKS,
        columns=[cst.COLUMN_URI, cst.COLUMN_MARKET_PLACE],
        database=database,
    )
    if base_url == cst.URL_STOCK_HISTORY:
        return [
            base_url
            + stock[0][:-6]
            + "/"
            + (
                cst.EXCHANGE_APPENDIX
                if stock[1] is None or stock[1] == "None"
                else stock[1]
            )
            for stock in stock_list
        ]

    elif base_url == cst.URL_STOCK_OVERVIEW:
        return [base_url + stock[0] for stock in stock_list]
    else:
        return [base_url + stock[0][:-6] for stock in stock_list]


# insert ignore / many
def write_index_content_to_stock_table(stocks, database=cst.DATABASE):
    with dataset.connect(database) as db:
        try:
            for stock in stocks:
                db[cst.TABLE_STOCKS].insert_ignore(stock, ["URI"])
        except IntegrityError:
            pass


def write_stock_to_index_contents_table(index_contents, database=cst.DATABASE):
    with dataset.connect(database) as db:
        try:
            db[cst.TABLE_INDEX_CONTENTS].insert_many(index_contents)
        except IntegrityError:
            pass


def write_index_content_list_to_db(index_content, index_name, database=cst.DATABASE):
    current_date = date.get_current_date()
    stocks = [dict(Name=stock[0], URI=stock[1]) for stock in index_content]
    write_index_content_to_stock_table(stocks, database=database)

    index_contents = [
        dict(IndexURI=index_name, AktienURI=stock[1], Abrufdatum=current_date)
        for stock in index_content
    ]
    write_stock_to_index_contents_table(index_contents, database=database)
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


# ToDo Clean, combine, refactor, delete from here
# Todo write next two functions as one insert_many function
# Write
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
            except IntegrityError:
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
            except IntegrityError:
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
            except IntegrityError:
                pass
    return True


# Levermann 01


# def get_earnings_after_tax(stock_uri, database=cst.DATABASE):
#     with dataset.connect(database) as db:
#         try:
#             results = db.query(
#                 "SELECT %s FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
#                 % (cst.COLUMN_EARNINGS_AT, cst.TABLE_COMPANY_DATA, stock_uri)
#             )
#             return float([item for item in results][0][cst.COLUMN_EARNINGS_AT])
#         except:
#             logger.exception("Exception at get_earnings_after_tax for %s" % stock_uri)
#             pass
#
#
# def get_earnings_after_tax_2(stock_uri, database=cst.DATABASE):
#     return get_item(
#         table=cst.TABLE_COMPANY_DATA,
#         column=cst.COLUMN_EARNINGS_AT,
#         condition=[cst.COLUMN_STOCK_URI, stock_uri],
#         database=database,
#     )

#
# def get_equity_capital(stock_uri, database=cst.DATABASE):
#     with dataset.connect(database) as db:
#         try:
#             results = db.query(
#                 "SELECT %s FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
#                 % (cst.COLUMN_EQUITY_CAPITAL, cst.TABLE_COMPANY_DATA, stock_uri)
#             )
#             return float([item for item in results][0][cst.COLUMN_EQUITY_CAPITAL])
#         except:
#             logger.exception("Exception at get_equity_capital for %s" % stock_uri)
#             pass


# def save_roe_to_db(stock_uri, roe, lev_score, database=cst.DATABASE):
#     current_date = date.get_current_date()
#     with dataset.connect(database) as db:
#         try:
#             db[cst.TABLE_LEVERMANN].insert(
#                 dict(
#                     AktienURI=stock_uri,
#                     Datum=current_date,
#                     Lev01_Wert=roe,
#                     Lev01_Score=lev_score,
#                 )
#             )
#         except IntegrityError:
#             db.query(
#                 "UPDATE %s SET "
#                 "Lev01_Wert = %s, "
#                 "Lev01_Score = %s "
#                 'WHERE AktienURI = "%s" AND Datum = "%s"'
#                 % (cst.TABLE_LEVERMANN, roe, lev_score, stock_uri, current_date)
#             )
#             pass


# Levermann 02


# def get_operative_result(stock_uri, database=cst.DATABASE):
#     with dataset.connect(database) as db:
#         try:
#             results = db.query(
#                 "SELECT %s FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
#                 % (cst.COLUMN_OPERATIVE_RESULT, cst.TABLE_COMPANY_DATA, stock_uri)
#             )
#             return float([item for item in results][0][cst.COLUMN_OPERATIVE_RESULT])
#         except:
#             logger.exception("Exception at get_operative_result for %s" % stock_uri)
#             pass
#
#
#
#
# def get_sales_revenue(stock_uri, database=cst.DATABASE):
#     with dataset.connect(database) as db:
#         try:
#             results = db.query(
#                 "SELECT %s FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
#                 % (cst.COLUMN_SALES_REVENUE, cst.TABLE_COMPANY_DATA, stock_uri)
#             )
#             return float([item for item in results][0][cst.COLUMN_SALES_REVENUE])
#         except:
#             logger.exception("Exception at get_sales_revenue for %s" % stock_uri)
#             pass


# def check_is_financial_company(stock_uri, database=cst.DATABASE):
#     fin_list = cst.FINANCE_SECTORS
#     with dataset.connect(database) as db:
#         try:
#             results = db.query(
#                 "SELECT %s FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
#                 % (cst.COLUMN_SECTORS, cst.TABLE_COMPANY_DATA, stock_uri)
#             )
#             result_list = [item for item in results][0][cst.COLUMN_SECTORS]
#             return any(i in result_list for i in fin_list)
#         except:
#             logger.exception(
#                 "Exception at check_is_financial_company for %s" % stock_uri
#             )
#             pass


def check_is_financial_company(stock_uri, database=cst.DATABASE):
    fin_list = cst.FINANCE_SECTORS
    results = get_item(
        table=cst.TABLE_COMPANY_DATA,
        column=cst.COLUMN_SECTORS,
        condition=[cst.COLUMN_STOCK_URI, stock_uri],
        order=[cst.COLUMN_DATE, cst.DESC],
        database=database,
    )
    return any(i in results for i in fin_list)


# def save_ebit_to_db(stock_uri, ebit, lev_score, database=cst.DATABASE):
#     current_date = date.get_current_date()
#     with dataset.connect(database) as db:
#         try:
#             db[cst.TABLE_LEVERMANN].insert(
#                 dict(
#                     AktienURI=stock_uri,
#                     Datum=current_date,
#                     Lev02_Wert=ebit,
#                     Lev02_Score=lev_score,
#                 )
#             )
#         except IntegrityError:
#             db.query(
#                 "UPDATE %s SET "
#                 "Lev02_Wert = %s, "
#                 "Lev02_Score = %s "
#                 'WHERE AktienURI = "%s" AND Datum = "%s"'
#                 % (cst.TABLE_LEVERMANN, ebit, lev_score, stock_uri, current_date)
#             )
#             pass


# Levermann 03

#
# def get_balance(stock_uri, database=cst.DATABASE):
#     with dataset.connect(database) as db:
#         try:
#             results = db.query(
#                 "SELECT %s FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
#                 % (cst.COLUMN_BALANCE, cst.TABLE_COMPANY_DATA, stock_uri)
#             )
#             return float([item for item in results][0][cst.COLUMN_BALANCE])
#         except:
#             logger.exception("Exception at get_balance for %s" % stock_uri)
#             pass


# def save_equity_ratio_to_db(stock_uri, equity_ratio, lev_score, database=cst.DATABASE):
#     current_date = date.get_current_date()
#     with dataset.connect(database) as db:
#         try:
#             db[cst.TABLE_LEVERMANN].insert(
#                 dict(
#                     AktienURI=stock_uri,
#                     Datum=current_date,
#                     Lev03_Wert=equity_ratio,
#                     Lev03_Score=lev_score,
#                 )
#             )
#         except IntegrityError:
#             db.query(
#                 "UPDATE %s SET "
#                 "Lev03_Wert = %s, "
#                 "Lev03_Score = %s "
#                 'WHERE AktienURI = "%s" AND Datum = "%s"'
#                 % (
#                     cst.TABLE_LEVERMANN,
#                     equity_ratio,
#                     lev_score,
#                     stock_uri,
#                     current_date,
#                 )
#             )
#             pass


# Levermann 04 & 05


# def get_latest_stock_price(stock_uri, database=cst.DATABASE):
#     with dataset.connect(database) as db:
#         try:
#             results = db.query(
#                 "SELECT %s FROM %s WHERE AktienURI = '%s' ORDER BY Datum DESC"
#                 % (cst.COLUMN_CLOSING_VALUE, cst.TABLE_STOCKS_HISTORIES, stock_uri)
#             )
#             return float([item for item in results][0][cst.COLUMN_CLOSING_VALUE])
#         except:
#             logger.exception(
#                 "Unhandled Exception at get_latest_stock_price for %s" % stock_uri
#             )
#             pass


def get_current_eps(stock_uri, database=cst.DATABASE):

    eps_s = get_list(
        table=cst.TABLE_COMPANY_DATA,
        columns=[
            cst.COLUMN_EPS_M3,
            cst.COLUMN_EPS_M2,
            cst.COLUMN_EPS_M1,
            cst.COLUMN_EPS_0,
            cst.COLUMN_EPS_P1,
        ],
        condition=[cst.COLUMN_STOCK_URI, stock_uri],
        order=[cst.COLUMN_DATE, cst.DESC],
        database=database,
    )
    return [float(i) for i in eps_s[0]]


def get_last_eps(stock_uri, database=cst.DATABASE):
    eps_s = get_list(
        table=cst.TABLE_COMPANY_DATA,
        columns=[
            cst.COLUMN_EPS_M3,
            cst.COLUMN_EPS_M2,
            cst.COLUMN_EPS_M1,
            cst.COLUMN_EPS_0,
            cst.COLUMN_EPS_P1,
        ],
        condition=[cst.COLUMN_STOCK_URI, stock_uri],
        order=[cst.COLUMN_DATE, cst.DESC],
        database=database,
    )
    return [float(i) for i in eps_s[1]]


# def save_kgv5_to_db(stock_uri, kgv5, kgv5_score, database=cst.DATABASE):
#     current_date = date.get_current_date()
#     with dataset.connect(database) as db:
#         try:
#             db[cst.TABLE_LEVERMANN].insert(
#                 dict(
#                     AktienURI=stock_uri,
#                     Datum=current_date,
#                     Lev04_Wert=kgv5,
#                     Lev04_Score=kgv5_score,
#                 )
#             )
#         except IntegrityError:
#             db.query(
#                 "UPDATE %s SET "
#                 "Lev04_Wert = %s, "
#                 "Lev04_Score = %s "
#                 'WHERE AktienURI = "%s" AND Datum = "%s"'
#                 % (cst.TABLE_LEVERMANN, kgv5, kgv5_score, stock_uri, current_date)
#             )
#             pass
#
#
# def save_kgv0_to_db(stock_uri, kgv0, kgv0_score, database=cst.DATABASE):
#     current_date = date.get_current_date()
#     with dataset.connect(database) as db:
#         try:
#             db[cst.TABLE_LEVERMANN].insert(
#                 dict(
#                     AktienURI=stock_uri,
#                     Datum=current_date,
#                     Lev05_Wert=kgv0,
#                     Lev05_Score=kgv0_score,
#                 )
#             )
#         except IntegrityError:
#             db.query(
#                 "UPDATE %s SET "
#                 "Lev05_Wert = %s, "
#                 "Lev05_Score = %s "
#                 'WHERE AktienURI = "%s" AND Datum = "%s"'
#                 % (cst.TABLE_LEVERMANN, kgv0, kgv0_score, stock_uri, current_date)
#             )
#             pass


# Levermann 06


def get_analyst_ratings(stock_uri, database=cst.DATABASE):
    ratings_list = get_list(
        table=cst.TABLE_COMPANY_DATA,
        columns=[
            cst.COLUMN_ANALYST_BUY,
            cst.COLUMN_ANALYST_HOLD,
            cst.COLUMN_ANALYST_SELL,
        ],
        condition=[cst.COLUMN_STOCK_URI, stock_uri],
        order=[cst.COLUMN_DATE, cst.DESC],
        database=database,
    )
    return [int(i) for i in ratings_list[0]]


# def save_rating_to_db(stock_uri, rating, rating_score, database=cst.DATABASE):
#     current_date = date.get_current_date()
#     with dataset.connect(database) as db:
#         try:
#             db[cst.TABLE_LEVERMANN].insert(
#                 dict(
#                     AktienURI=stock_uri,
#                     Datum=current_date,
#                     Lev06_Wert=rating,
#                     Lev06_Score=rating_score,
#                 )
#             )
#         except IntegrityError:
#             db.query(
#                 "UPDATE %s SET "
#                 "Lev06_Wert = %s, "
#                 "Lev06_Score = %s "
#                 'WHERE AktienURI = "%s" AND Datum = "%s"'
#                 % (cst.TABLE_LEVERMANN, rating, rating_score, stock_uri, current_date)
#             )
#             pass


def get_main_index_of_stock(stock_uri, database=cst.DATABASE):
    index_names = get_item(
        table=cst.TABLE_COMPANY_DATA,
        column=cst.COLUMN_INDICES,
        condition=[cst.COLUMN_STOCK_URI, stock_uri],
        order=[cst.COLUMN_DATE, cst.DESC],
        database=database,
    )

    if index_names is None:
        return None
    else:
        main_index = (
            index_names.replace("'", "")
            .replace('"', "")
            .replace("[", "")
            .replace("]", "")
            .split(", ")[0]
        )

    return get_item(
        table=cst.TABLE_INDIZES,
        column=cst.COLUMN_URI,
        condition=[cst.COLUMN_INDEX_NAME, main_index],
        database=database,
    )


def is_small_cap(stock_uri, database=cst.DATABASE):
    market_cap = float(
        get_item(
            table=cst.TABLE_COMPANY_DATA,
            column=cst.COLUMN_MARKET_CAP,
            condition=[cst.COLUMN_STOCK_URI, stock_uri],
            order=[cst.COLUMN_DATE, cst.DESC],
            database=database,
        )
    )

    return market_cap < cst.MARKET_CAP_THRESHOLD


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
        except IntegrityError:
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
        except IntegrityError:
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
        except IntegrityError:
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
        except IntegrityError:
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
        except IntegrityError:
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
        except IntegrityError:
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
        except IntegrityError:
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
