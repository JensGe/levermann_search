from utils import parse_op as parse
from utils import db_op as db
from utils import scrap_op as scrap
from utils import constants as CST


def write_index_contents_from_html_to_db():
    index_list = db.get_index_names()
    file_list = [CST.PATH_INDEX_CONTENT + index + CST.HTML_EXTENSION for index in index_list]

    for file in file_list:
        index_content_soup = scrap.get_soup_code_from_file(file)
        stock_list = parse.get_stock_list_of_single_index(index_content_soup)
        index_uri = file.split('/')[-1][:-5]
        db.write_stock_list_to_db(stock_list, index_uri)

    return True


def write_index_histories_from_html_to_db():
    index_list = db.get_index_names()
    file_list = [CST.PATH_INDEX_HISTORY + index + CST.HTML_EXTENSION for index in index_list]
    for file in file_list:
        index_history_soup = scrap.get_soup_code_from_file(file)
        index_history_list = parse.get_historic_prices(index_history_soup)

        index_uri = file.split('/')[-1][:-5]
        db.write_index_history_to_db(index_history_list, index_uri)


def write_stock_histories_from_html_to_db():
    stock_list = db.get_stock_names()
    file_list = [CST.PATH_STOCK_HISTORY + stock[:-6] + CST.HTML_EXTENSION for stock in stock_list]
    for file in file_list:
        stock_history_soup = scrap.get_soup_code_from_file(file)
        stock_history_list = parse.get_historic_prices(stock_history_soup)

        stock_uri = file.split('/')[-1][:-5] + '-Aktie'
        db.write_stock_history_to_db(stock_history_list, stock_uri)


def write_stock_overview_data_to_db():
    stock_list = db.get_stock_names()
    file_list = [CST.PATH_STOCK_OVERVIEW + stock[:-6] + CST.HTML_EXTENSION for stock in stock_list]
    for file in file_list[:10]:
        stock_uri = file.split('/')[-1][:-5] + '-Aktie'
        stock_overview_soup = scrap.get_soup_code_from_file(file)
        market_cap = parse.get_market_cap(stock_overview_soup)
        stock_indizes = parse.get_listed_indizes(stock_overview_soup)
        stock_sectors = parse.get_sectors(stock_overview_soup)
        db.write_single_overview_data_to_db(stock_uri, market_cap, stock_indizes, stock_sectors)


def write_stock_balance_data_to_db():
    stock_list = db.get_stock_names()
    file_list = [CST.PATH_STOCK_BALANCE + stock[:-6] + CST.HTML_EXTENSION for stock in stock_list]
    for file in file_list[:5]:
        stock_uri = file.split('/')[-1][:-5] + '-Aktie'
        stock_balance_soup = scrap.get_soup_code_from_file(file)

        result_after_tax = parse.get_result_after_tax(stock_balance_soup)
        operative_result = parse.get_operative_result(stock_balance_soup)
        sales_revenue = parse.get_sales_revenue(stock_balance_soup)
        total_assets = parse.get_total_assets(stock_balance_soup)
        eps_minus_3, eps_minus_2, eps_minus_1 = parse.get_result_per_share_last_three_years(stock_balance_soup)

        db.write_single_balance_data_to_db(stock_uri, result_after_tax, operative_result, sales_revenue, total_assets,
                                            eps_minus_3, eps_minus_2, eps_minus_1)

