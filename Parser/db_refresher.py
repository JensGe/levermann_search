from utils import db_op as db
from utils import parse_op as parse
from utils import date_op as date

from utils import scrap_op as scrap

index_history_url = "https://www.boerse-online.de/index/historisch/"
index_stocks_url = "https://www.boerse-online.de/index/liste/"
stock_history_url = "https://www.boerse-online.de/kurse/historisch/"


def select_index_intervall(index_name):
    """ calculate Intervall to be used in scrapping
        therefore uses latest date in DB + 1
        if DB is empty, the intervall will be one year ago to today
    :param index_name: the stockindex's name
    :return: start_date_str, end_date_str: as strings
    """
    today_date = date.get_todays_date()
    start_date = date.subtract_one_year(today_date)

    max_db_date = db.get_max_date_of_index_history(index_name)

    if max_db_date:
        start_date = date.add_one_day(date.string_to_date(max_db_date))

    start_date_str = date.date_to_string(start_date)
    end_date_str = date.date_to_string(today_date)

    print("Searching %s - Index from %s to %s" % (index_name, start_date_str, end_date_str))
    return start_date_str, end_date_str


def refresh_index_history(index_name, start_date_str, end_date_str):
    """
    Updates index history with most current values
    """

    if date.string_to_date(start_date_str) >= date.string_to_date(end_date_str):
        print("---- Enddate less or equal than start date --- Don't Scrap")
        return False
    # start scrapping with calculated intervall
    driver = parse.init_driver()
    content = parse.get_index_history_content(driver, index_history_url, index_name, start_date_str, end_date_str)

    index_history = parse.extract_history_table_to_list(content)
    parse.save_index_history_to_db(index_history, index_name)

    driver.quit()
    return True


def refresh_index_stocks(index_name):
    """
    Scraps the current Stocks inside selected Index
    """
    driver = parse.init_driver()
    content = parse.get_index_stocks_content(driver, index_stocks_url, index_name)
    index_stocks = []
    for index_stock_page in content:
        index_stocks.extend(parse.extract_index_stocks_to_list(index_stock_page))
    # index_stocks = ihs.extract_index_stocks_to_list(content)

    parse.update_index_stocks_db(index_stocks, index_name)
    driver.quit()


def select_stock_intervall(stock_name):
    """ calculate Intervall to be used in parsing
        therefore uses latest date in DB + 1
        if DB is empty, the intervall will be one year ago to today
    :param stock_name: the stocks name
    :return: start_date_str, end_date_str: as strings
    """
    today_date = date.get_todays_date()
    start_date = date.subtract_one_year(today_date)

    max_db_date = db.get_max_date_of_stock_history(stock_name)

    if max_db_date:
        start_date = date.add_one_day(date.string_to_date(max_db_date))

    start_date_str = date.date_to_string(start_date)
    end_date_str = date.date_to_string(today_date)

    print("Searching %s - Stock from %s to %s" % (stock_name, start_date_str, end_date_str))
    return start_date_str, end_date_str


def refresh_all_stocks_history(index_name):
    all_stocks = db.get_all_stock_infos(index_name)
    for stock in all_stocks:
        start_date_str, end_date_str = select_stock_intervall(stock[0])
        refresh_single_stock_history(stock, index_name, start_date_str, end_date_str)
    return True


def refresh_single_stock_history(stock, index_name, start_date_str, end_date_str):
    stock_name, stock_isin, stock_url_part = stock
    page_url = stock_history_url + stock_url_part

    if date.string_to_date(start_date_str) >= date.string_to_date(end_date_str):
        print("---- Enddate less or equal than start date --- Don't Scrap")
        return False

    # start scrapping with calculated intervall
    driver = parse.init_driver()
    content = parse.get_stock_history_content(driver, page_url, start_date_str, end_date_str)

    stock_history = parse.extract_history_table_to_list(content)
    parse.save_stock_history_to_db(stock_history, index_name, stock_name, stock_isin)

    driver.quit()

    return True


def download_soups_for_stock(stock_short_link):
    driver = scrap.init_driver()
    download_list = scrap.create_stock_download_list(stock_short_link)

    for url in download_list:
        soup = scrap.get_soup_code_of_url(driver, url)
        file_name = 'data/' + stock_short_link + '/' + url.split('/')[3] + '_' + date.date_to_string(date.get_todays_date()) + '.html'
        scrap.save_soup_to_file(soup, file_name)

    scrap.close_driver(driver)


# def get_levermann_score(stock_short_link):
#
#     return levermann_score
