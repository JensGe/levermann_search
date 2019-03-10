import os
import time
import random

from utils import scrap_op as scrap
from utils import parse_op as parse
from utils import db_op as db
from utils import constants as cst

from selenium.common import exceptions
from loguru import logger


def scrap_single_page(driver, scrap_url, save_path):
    stock_uri = scrap_url.split('/')[-1]
    file_name = save_path + stock_uri + cst.HTML_EXTENSION
    if os.path.isfile(file_name):
        logger.info("Single Scrap Stock %s: Skip existing File for stock: %s" % (save_path.split('/')[-2], stock_uri))
        return
    else:
        time.sleep(cst.SHORT_WAIT + random.uniform(0, cst.RANDOM_WAIT_RANGE))

    try:
        soup = scrap.get_soup_code_from_url(driver, scrap_url)
        scrap.save_soup_to_file(soup, file_name)
    except exceptions.WebDriverException:
        logger.exception('WebDriverException for URL %s' % scrap_url)
        return


def generate_scrap_urls(stock_uri):
    return {'Overview Url': cst.URL_STOCK_OVERVIEW + stock_uri,
            'Balance Url': cst.URL_STOCK_BALANCE + stock_uri,
            'Dates Url': cst.URL_STOCK_DATES + stock_uri,
            'Estimates Url': cst.URL_STOCK_ESTIMATES + stock_uri,
            'Targets Url': cst.URL_STOCK_TARGETS + stock_uri}


def parse_dates(date_soup):
    return parse.get_bygone_dates(date_soup), parse.get_future_dates(date_soup)


def start_complete_workflow():
    stock_uri_list = db.get_list(table='Aktien_Scraping_Queue',
                                 columns='AktienURI',
                                 condition=[cst.COLUMN_ACTIVE, b'1'])

    driver = scrap.init_driver(third_party_cookies=False)
    for stock in stock_uri_list:
        scrap_urls = generate_scrap_urls(stock)

        scrap_single_page(driver=driver, scrap_url=scrap_urls['Overview Url'], save_path=cst.PATH_STOCK_OVERVIEW)
        scrap_single_page(driver=driver, scrap_url=scrap_urls['Estimates Url'], save_path=cst.PATH_STOCK_ESTIMATES)
        scrap_single_page(driver=driver, scrap_url=scrap_urls['Dates Url'], save_path=cst.PATH_STOCK_DATES)

        bygone_dates, future_dates = parse_dates(scrap.get_soup_code_from_file(cst.PATH_STOCK_DATES + stock))
        # ToDO

        #
        # if is_new_quarterly_date_since_last_run() or is_first_weekend_of_month():
        #     scrap_single_history_index_for_stock(stock)
        #
        # if not yearly_numbers_are_up_to_date():
        #     scrap_single_page(driver=driver, scrap_url=scrap_urls['Balance Url'], save_path=CST.PATH_STOCK_BALANCE)





