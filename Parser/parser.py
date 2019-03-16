from utils import parse_op as parse
from utils import db_op as db
from utils import scrap_op as scrap
from utils import constants as CST
from loguru import logger


def write_index_contents_from_html_to_db():
    index_list = db.get_list(
        table=CST.TABLE_INDIZES,
        columns=CST.COLUMN_URI,
        condition=[CST.COLUMN_ACTIVE, b"1"],
    )
    file_list = [
        CST.PATH_INDEX_CONTENT + index + CST.HTML_EXTENSION for index in index_list
    ]

    for file in file_list:
        index_content_soup = scrap.get_soup_code_from_file(file)
        stock_list = parse.get_stock_list_of_single_index(index_content_soup)
        index_uri = file.split("/")[-1][:-5]
        db.write_stock_list_to_db(
            stock_list, index_uri
        )  # TODO DB _mysql_exceptions.OperationalError: (1040, 'Too many connections')

    return True


def write_index_histories_from_html_to_db():
    index_list = db.get_list(
        table=CST.TABLE_INDIZES,
        columns=CST.COLUMN_URI,
        condition=[CST.COLUMN_ACTIVE, b"1"],
    )
    file_list = [
        CST.PATH_INDEX_HISTORY + index + CST.HTML_EXTENSION for index in index_list
    ]
    for file in file_list:
        index_history_soup = scrap.get_soup_code_from_file(file)
        index_history_list = parse.get_historic_prices(index_history_soup)

        index_uri = file.split("/")[-1][:-5]
        try:
            db.write_index_history_to_db(index_history_list, index_uri)
        except:
            logger.exception("")


def write_stock_overview_data_to_db():
    stock_list = db.get_list(table=CST.TABLE_STOCKS, columns=CST.COLUMN_URI)
    file_list = [
        CST.PATH_STOCK_OVERVIEW + stock + CST.HTML_EXTENSION for stock in stock_list
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
        stock_indizes = parse.get_listed_indizes(stock_overview_soup)
        stock_sectors = parse.get_sectors(stock_overview_soup)
        market_place = parse.get_market_place(stock_overview_soup)
        db.write_single_overview_data_to_db(
            stock_uri, market_cap, stock_indizes, stock_sectors, market_place
        )

        stock_history_list = parse.get_historic_prices(stock_overview_soup)
        db.write_stock_history_to_db(stock_history_list, stock_uri)


def write_stock_histories_from_html_to_db():
    stock_list = db.get_list(table=CST.TABLE_STOCKS, columns=CST.COLUMN_URI)
    file_list = [
        CST.PATH_STOCK_HISTORY + stock[:-6] + CST.HTML_EXTENSION for stock in stock_list
    ]
    for file in file_list:
        stock_history_soup = scrap.get_soup_code_from_file(file)
        if stock_history_soup is None:
            logger.warning(
                "Write Stock History Data to DB: Stock History Soup is None for %s"
                % str(file)
            )
            continue
        stock_history_list = parse.get_historic_prices(stock_history_soup)

        stock_uri = file.split("/")[-1][:-5] + "-Aktie"
        db.write_stock_history_to_db(stock_history_list, stock_uri)


def write_stock_balance_data_to_db():
    stock_list = db.get_list(table=CST.TABLE_STOCKS, columns=CST.COLUMN_URI)
    file_list = [
        CST.PATH_STOCK_BALANCE + stock[:-6] + CST.HTML_EXTENSION for stock in stock_list
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
            result_after_tax = parse.get_current_value_of_attribute(
                stock_balance_soup, CST.TEXT_RESULT_AFTER_TAX
            )
            operative_result = parse.get_current_value_of_attribute(
                stock_balance_soup, CST.TEXT_OPERATIVE_RESULT
            )
            sales_revenue = parse.get_current_value_of_attribute(
                stock_balance_soup, CST.TEXT_SALES_REVENUE
            )
            total_assets = parse.get_current_value_of_attribute(
                stock_balance_soup, CST.TEXT_TOTAL_ASSETS
            )
            equity_capital = parse.get_current_value_of_attribute(
                stock_balance_soup, CST.TEXT_EQUITY_CAPITAL
            )
            eps_minus_3, eps_minus_2, eps_minus_1 = parse.get_result_per_share_last_three_years(
                stock_balance_soup
            )

            db.write_single_balance_data_to_db(
                stock_uri,
                result_after_tax,
                operative_result,
                sales_revenue,
                total_assets,
                equity_capital,
                eps_minus_3,
                eps_minus_2,
                eps_minus_1,
            )
        except:
            logger.exception(
                "Write Stock Balance Data to DB: Exception for stock: %s" % stock_uri
            )
            continue


def write_stock_estimates_data_to_db():
    stock_list = db.get_list(table=CST.TABLE_STOCKS, columns=CST.COLUMN_URI)
    file_list = [
        CST.PATH_STOCK_ESTIMATES + stock[:-6] + CST.HTML_EXTENSION
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
            eps_0, eps_plus_1 = parse.get_result_per_share_current_and_next_year(
                stock_estimate_soup
            )

            db.write_single_estimate_data_to_db(stock_uri, eps_0, eps_plus_1)
        except:
            logger.exception(
                "Write Stock Estimate Data to DB: Exception for stock: %s" % stock_uri
            )


def write_stock_targets_data_to_db():
    stock_list = db.get_list(table=CST.TABLE_STOCKS, columns=CST.COLUMN_URI)
    file_list = [
        CST.PATH_STOCK_TARGETS + stock[:-6] + CST.HTML_EXTENSION for stock in stock_list
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
            db.write_single_targets_data_to_db(stock_uri, buy, hold, sell)
        except:
            logger.exception(
                "Write Stock Targets Data to DB: Exception for stock: %s" % stock_uri
            )


def write_stock_last_quarterly_figures_date_to_db():
    stock_list = db.get_list(table=CST.TABLE_STOCKS, columns=CST.COLUMN_URI)
    file_list = [
        CST.PATH_STOCK_DATES + stock[:-6] + CST.HTML_EXTENSION for stock in stock_list
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
                db.write_single_stock_dates_data_to_db(stock_uri, last_figures_date)
        except:
            logger.exception(
                "Write Stock Quaterly Data to DB: Exception for stock: %s" % stock_uri
            )
