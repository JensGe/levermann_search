from utils import parse_op as parse
from utils import db_op as db
from utils import scrap_op as scrap
from utils import constants as CST


def write_index_contents_from_html_to_db():
    index_list = db.get_index_names()
    file_list = [CST.INDEX_CONTENT_PATH + index + CST.EXT_HTML for index in index_list]

    for file in file_list:
        index_content_soup = scrap.get_soup_code_from_file(file)
        stock_list = parse.get_stock_list_of_single_index(index_content_soup)
        index_URI = file.split('/')[-1][:-5]
        db.write_stock_list_to_db(stock_list, index_URI)

    return True


def write_index_histories_from_html_to_db():
    index_list = db.get_index_names()
    file_list = [CST.INDEX_HISTORY_PATH + index + CST.EXT_HTML for index in index_list]
    for file in file_list:
        index_history_soup = scrap.get_soup_code_from_file(file)
        index_history_list = parse.get_historic_prices(index_history_soup)

        index_uri = file.split('/')[-1][:-5]
        db.write_index_history_to_db(index_history_list, index_uri)


def write_stock_histories_from_html_to_db():
    stock_list = db.get_stock_names()
    file_list = [CST.STOCK_HISTORY_PATH + stock[:-6] + CST.EXT_HTML for stock in stock_list]
    for file in file_list:
        stock_history_soup = scrap.get_soup_code_from_file(file)
        stock_history_list = parse.get_historic_prices(stock_history_soup)

        stock_uri = file.split('/')[-1][:-5] + '-Aktie'
        db.write_stock_history_to_db(stock_history_list, stock_uri)



