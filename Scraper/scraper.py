import os
import time
import random

from utils import scrap_op as scrap
from utils import db_op as db
from utils import date_op as date
from utils import constants as CST

from selenium.common import exceptions
from loguru import logger


def scrap_index_content_sites():
    scrap_list = db.create_active_index_url_list(CST.URL_INDEX_CONTENT)
    driver = scrap.init_driver()
    for url in scrap_list:
        index_uri = url.split('/')[-1]
        file_name = CST.PATH_INDEX_CONTENT + index_uri + CST.HTML_EXTENSION
        soup = scrap.get_soup_code_from_url(driver, url)
        scrap.save_soup_to_file(soup, file_name)
    scrap.close_driver(driver)


def scrap_index_histories():
    scrap_list = db.create_active_index_url_list(CST.URL_INDEX_HISTORY)
    driver = scrap.init_driver()
    for url in scrap_list:
        index_uri = url.split('/')[-1]
        end_date = date.get_current_date()
        start_date = date.subtract_one_year(date.get_current_date())
        max_db_date = db.get_latest_date_from_index_history(index_uri)
        file_name = CST.PATH_INDEX_HISTORY + index_uri + CST.HTML_EXTENSION
        if max_db_date is None:
            logger.warning("Scrap Index Histories: MaxDate is None for %s" % url)
            pass
        elif date.add_one_day(max_db_date) == end_date:
            logger.info("Scrap Index Histories: EndDate = MaxDate")
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
    scrap_list = db.create_stock_history_url_list(CST.URL_STOCK_HISTORY)
    driver = scrap.init_driver()
    for url in scrap_list:
        stock_uri = url.split('/')[-2]
        end_date = date.get_current_date()
        start_date = date.subtract_one_year(date.get_current_date())
        max_db_date = db.get_latest_date_from_stock_history(stock_uri + '-Aktie')
        file_name = CST.PATH_STOCK_HISTORY + stock_uri + CST.HTML_EXTENSION
        if os.path.isfile(file_name):
            logger.info("Scrap Stock Histories: Skip existing File for stock: %s" % stock_uri)
            continue

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
        print(dated_url)
        soup = scrap.get_soup_from_history_url(driver, dated_url)
        scrap.save_soup_to_file(soup, file_name)
    scrap.close_driver(driver)


def scrap_stock_info(scrap_url, save_path):
    if scrap_url == CST.URL_STOCK_OVERVIEW:
        scrap_list = db.create_stock_overview_url_list(scrap_url)
    else:
        scrap_list = db.create_stock_info_url_list(scrap_url)
    driver = scrap.init_driver()
    for url in scrap_list:
        stock_uri = url.split('/')[-1]
        file_name = save_path + stock_uri + CST.HTML_EXTENSION
        if os.path.isfile(file_name):
            logger.info("Scrap Stock Histories: Skip existing File for stock: %s" % stock_uri)
            continue
        else:
            time.sleep(CST.SHORT_WAIT + random.uniform(0, CST.RANDOM_WAIT_RANGE))
        try:
            soup = scrap.get_soup_code_from_url(driver, url)
            scrap.save_soup_to_file(soup, file_name)
        except exceptions.WebDriverException:
            logger.exception('WebDriverException for URL %s' % url)
            continue

    scrap.close_driver(driver)


def scrap_stock_infos():
    scrap_stock_info(CST.URL_STOCK_OVERVIEW, CST.PATH_STOCK_OVERVIEW)
    scrap_stock_info(CST.URL_STOCK_BALANCE, CST.PATH_STOCK_BALANCE)
    scrap_stock_info(CST.URL_STOCK_DATES, CST.PATH_STOCK_DATES)
    scrap_stock_info(CST.URL_STOCK_ESTIMATES, CST.PATH_STOCK_ESTIMATES)
    scrap_stock_info(CST.URL_STOCK_TARGETS, CST.PATH_STOCK_TARGETS)




