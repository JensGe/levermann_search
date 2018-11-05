from utils import scrap_op as scrap
from utils import db_op as db
from utils import date_op as date
from utils import constants as CST


def scrap_index_content_sites():
    scrap_list = db.create_index_url_list(CST.URL_INDEX_CONTENT)
    driver = scrap.init_driver()
    for url in scrap_list:
        index_uri = url.split('/')[-1]
        file_name = CST.INDEX_CONTENT_PATH + index_uri + CST.EXT_HTML
        soup = scrap.get_soup_code_from_url(driver, url)
        scrap.save_soup_to_file(soup, file_name)
    scrap.close_driver(driver)


def scrap_index_histories():
    scrap_list = db.create_index_url_list(CST.URL_INDEX_HISTORY)
    driver = scrap.init_driver()
    for url in scrap_list:
        index_uri = url.split('/')[-1]
        end_date = date.get_todays_date()
        start_date = date.subtract_one_year(date.get_todays_date())
        max_db_date = db.get_latest_date_from_index_history(index_uri)
        file_name = CST.INDEX_HISTORY_PATH + index_uri + CST.EXT_HTML
        if max_db_date is None:
            pass
        elif date.add_one_day(max_db_date) == end_date:
            scrap.save_soup_to_file('', file_name)
            continue
        elif max_db_date > start_date:
            start_date = date.add_one_day(max_db_date)

        date_interval = '/' + date.date_to_string(start_date) +\
                        '_' + date.date_to_string(end_date)
        dated_url = url + date_interval

        soup = scrap.get_soup_code_from_url(driver, dated_url)
        scrap.save_soup_to_file(soup, file_name)
    scrap.close_driver(driver)


def scrap_stock_histories():
    scrap_list = db.create_stock_url_list(CST.URL_STOCK_HISTORY)
    driver = scrap.init_driver()
    for url in scrap_list:
        stock_uri = url.split('/')[-2]
        short_stock_uri = stock_uri[:-6]
        end_date = date.get_todays_date()
        start_date = date.subtract_one_year(date.get_todays_date())
        max_db_date = db.get_latest_date_from_index_history(stock_uri)
        file_name = CST.STOCK_HISTORY_PATH + short_stock_uri + CST.EXT_HTML
        if max_db_date is None:
            pass
        elif date.add_one_day(max_db_date) == end_date:
            scrap.save_soup_to_file('', file_name)
            continue
        elif max_db_date > start_date:
            start_date = date.add_one_day(max_db_date)

        date_interval = '/' + date.date_to_string(start_date) +\
                        '_' + date.date_to_string(end_date)
        dated_url = url.replace(stock_uri, short_stock_uri) + date_interval
        soup = scrap.get_soup_code_from_url(driver, dated_url)
        scrap.save_soup_to_file(soup, file_name)
    scrap.close_driver(driver)

# https://www.boerse-online.de/kurse/historisch/ab_inbev-aktie/xetra/04.11.2017_04.11.2018