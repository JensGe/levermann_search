from utils import parse_op as parse
from utils import db_op as db
from utils import scrap_op as scrap
from utils import date_op as date
from utils import constants as cst
from loguru import logger


def write_index_contents_from_html_to_db():
    index_list = db.get_list(
        table=cst.TABLE_INDIZES,
        columns=cst.COLUMN_URI,
        condition=[cst.COLUMN_ACTIVE, 1],
    )
    file_list = [
        cst.PATH_INDEX_CONTENT + index + cst.HTML_EXTENSION for index in index_list
    ]

    for file in file_list:
        index_content_soup = scrap.get_soup_code_from_file(file)
        stock_list = parse.get_stock_list_of_single_index(index_content_soup)
        index_uri = file.split("/")[-1][:-5]
        db.write_index_content_list_to_db(stock_list, index_uri)

    return True


def write_index_histories_from_html_to_db():
    index_list = db.get_list(
        table=cst.TABLE_INDIZES,
        columns=cst.COLUMN_URI,
        condition=[cst.COLUMN_ACTIVE, 1],
    )
    file_list = [
        cst.PATH_INDEX_HISTORY + index + cst.HTML_EXTENSION for index in index_list
    ]
    for file in file_list:
        index_history_soup = scrap.get_soup_code_from_file(file)
        index_history_list = parse.get_historic_prices_from_history(index_history_soup)

        index_uri = file.split("/")[-1][:-5]
        try:
            db.write_index_history_to_db(index_history_list, index_uri)
        except:
            logger.exception(
                "Unhandled Exceptions at parse.write_index_histories_from_html_to_db"
            )


def write_stock_overview_data_to_db():
    stock_list = db.get_list(table=cst.TABLE_STOCKS, columns=cst.COLUMN_URI)
    file_list = [
        cst.PATH_STOCK_OVERVIEW + stock + cst.HTML_EXTENSION for stock in stock_list
    ]
    for file in file_list:
        stock_uri = file.split("/")[-1][:-5]
        stock_overview_soup = scrap.get_soup_code_from_file(file)
        if stock_overview_soup is None:
            logger.warning(
                "Write Stock Overview Data to DB: Stock Overview Soup is None for %s"
                % str(file)
            )
            continue

        market_cap = parse.get_market_cap(stock_overview_soup)
        if market_cap is None:
            logger.warning(
                "Write Stock Overview Data to DB: Market Cap is None for %s" % str(file)
            )
            market_cap = -1.00

        stock_indices = str(parse.get_listed_indizes(stock_overview_soup))
        stock_sectors = str(parse.get_sectors(stock_overview_soup))
        market_place = parse.get_market_place(stock_overview_soup)

        db.upsert_item(table=cst.TABLE_COMPANY_DATA,
                       primary_keys=[cst.COLUMN_STOCK_URI, cst.COLUMN_DATE],
                       stock_uri=stock_uri,
                       market_cap=market_cap,
                       current_date=date.get_current_date(),
                       stock_indices=stock_indices,
                       stock_sectors=stock_sectors)

        db.update_item(table=cst.TABLE_STOCKS,
                       primary_keys=cst.COLUMN_URI,
                       uri=stock_uri,
                       market_place=market_place)

        stock_history_list = parse.get_historic_stock_prices_from_overview(
            stock_overview_soup
        )
        if stock_history_list is not None:
            db.write_stock_overview_history_to_db(stock_history_list, stock_uri)


def write_stock_histories_from_html_to_db():
    stock_list = db.get_list(table=cst.TABLE_STOCKS, columns=cst.COLUMN_URI)
    file_list = [
        cst.PATH_STOCK_HISTORY + stock[:-6] + cst.HTML_EXTENSION for stock in stock_list
    ]
    for file in file_list:
        stock_history_soup = scrap.get_soup_code_from_file(file)
        if stock_history_soup is None:
            logger.warning(
                "Write Stock History Data to DB: Stock History Soup is None for %s"
                % str(file)
            )
            continue
        stock_history_list = parse.get_historic_prices_from_history(stock_history_soup)

        stock_uri = file.split("/")[-1][:-5] + "-Aktie"
        db.write_stock_history_to_db(stock_history_list, stock_uri)


def write_stock_balance_data_to_db():
    stock_list = db.get_list(table=cst.TABLE_STOCKS, columns=cst.COLUMN_URI)
    file_list = [
        cst.PATH_STOCK_BALANCE + stock[:-6] + cst.HTML_EXTENSION for stock in stock_list
    ]
    for file in file_list:
        stock_uri = file.split("/")[-1][:-5] + "-Aktie"
        stock_balance_soup = scrap.get_soup_code_from_file(file)

        if stock_balance_soup is None:
            logger.warning(
                "Write Stock Balance Data to DB: Soup is None for %s" % str(file)
            )
            continue

        if not parse.is_data_available(stock_balance_soup):
            logger.warning(
                "Write Stock Balance Data to DB: No Data Available for %s" % str(file)
            )
            continue

        try:
            earnings_after_tax = parse.get_current_value_of_attribute(
                stock_balance_soup, cst.TEXT_RESULT_AFTER_TAX
            )
            operative_result = parse.get_current_value_of_attribute(
                stock_balance_soup, cst.TEXT_OPERATIVE_RESULT
            )
            sales_revenue = parse.get_current_value_of_attribute(
                stock_balance_soup, cst.TEXT_SALES_REVENUE
            )
            balance = parse.get_current_value_of_attribute(
                stock_balance_soup, cst.TEXT_BALANCE
            )
            equity_capital = parse.get_current_value_of_attribute(
                stock_balance_soup, cst.TEXT_EQUITY_CAPITAL
            )
            eps_m3, eps_m2, eps_m1 = parse.get_result_per_share_last_three_years(
                stock_balance_soup
            )

            db.upsert_item(table=cst.TABLE_COMPANY_DATA,
                           primary_keys=[cst.COLUMN_STOCK_URI, cst.COLUMN_DATE],
                           current_date=date.get_current_date(),
                           stock_uri=stock_uri,
                           equity_capital=equity_capital,
                           earnings_after_tax=earnings_after_tax,
                           operative_result=operative_result,
                           sales_revenue=sales_revenue,
                           balance=balance,
                           eps_m3=eps_m3,
                           eps_m2=eps_m2,
                           eps_m1=eps_m1
                           )


        except:
            logger.exception(
                "Write Stock Balance Data to DB: Exception for stock: %s" % stock_uri
            )
            continue


def write_stock_estimates_data_to_db():
    stock_list = db.get_list(table=cst.TABLE_STOCKS, columns=cst.COLUMN_URI)
    file_list = [
        cst.PATH_STOCK_ESTIMATES + stock[:-6] + cst.HTML_EXTENSION
        for stock in stock_list
    ]
    for file in file_list:
        stock_uri = file.split("/")[-1][:-5] + "-Aktie"
        stock_estimate_soup = scrap.get_soup_code_from_file(file)

        if stock_estimate_soup is None:
            logger.warning(
                "Write Stock Estimate Data to DB: Soup is None for %s" % str(file)
            )
            continue

        try:
            eps_0, eps_p1 = parse.get_result_per_share_current_and_next_year(
                stock_estimate_soup
            )

            db.upsert_item(table=cst.TABLE_COMPANY_DATA,
                           primary_keys=[cst.COLUMN_STOCK_URI, cst.COLUMN_DATE],
                           current_date=date.get_current_date(),
                           stock_uri=stock_uri,
                           eps_0=eps_0,
                           eps_p1=eps_p1)
        except:
            logger.exception(
                "Write Stock Estimate Data to DB: Exception for stock: %s" % stock_uri
            )


def write_stock_targets_data_to_db():
    stock_list = db.get_list(table=cst.TABLE_STOCKS, columns=cst.COLUMN_URI)
    file_list = [
        cst.PATH_STOCK_TARGETS + stock[:-6] + cst.HTML_EXTENSION for stock in stock_list
    ]
    for file in file_list:
        stock_uri = file.split("/")[-1][:-5] + "-Aktie"
        stock_targets_soup = scrap.get_soup_code_from_file(file)

        if stock_targets_soup is None:
            logger.warning(
                "Write Stock Targets Data to DB: Soup is None for %s" % str(file)
            )
            continue

        try:
            buy, hold, sell = parse.get_analyst_ratings(stock_targets_soup)
            db.upsert_item(table=cst.TABLE_COMPANY_DATA,
                           primary_keys=[cst.COLUMN_STOCK_URI, cst.COLUMN_DATE],
                           current_date=date.get_current_date(),
                           stock_uri=stock_uri,
                           analyst_buy=buy,
                           analyst_hold=hold,
                           analyst_sell=sell,
                           )


        except:
            logger.exception(
                "Write Stock Targets Data to DB: Exception for stock: %s" % stock_uri
            )


# ToDo write all Dates, not only latest
def write_stock_last_quarterly_figures_date_to_db():
    stock_list = db.get_list(table=cst.TABLE_STOCKS, columns=cst.COLUMN_URI)
    file_list = [
        cst.PATH_STOCK_DATES + stock[:-6] + cst.HTML_EXTENSION for stock in stock_list
    ]
    for file in file_list:
        stock_uri = file.split("/")[-1][:-5] + "-Aktie"
        stock_targets_soup = scrap.get_soup_code_from_file(file)

        if stock_targets_soup is None:
            logger.warning(
                "Write Stock Quaterlyfigures Data to DB: Soup is None for %s"
                % str(file)
            )
            continue
        try:
            last_figures_date = parse.get_last_quarterly_figures_date(
                stock_targets_soup
            )
            if last_figures_date is None:
                continue
            else:
                # db.write_single_stock_dates_data_to_db(stock_uri, last_figures_date)
                db.upsert_item(table=cst.TABLE_STOCK_DATES,
                               primary_keys=[cst.COLUMN_STOCK_URI, cst.COLUMN_DATE],
                               current_date=last_figures_date,
                               quarterly="Quarterly/Yearly",
                               )


        except:
            logger.exception(
                "Write Stock Quaterly Data to DB: Exception for stock: %s" % stock_uri
            )
