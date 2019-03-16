import time
import os

from utils import date_op as date
from utils import constants as CST

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.common import exceptions

from bs4 import BeautifulSoup
from loguru import logger


def init_driver(third_party_cookies=True):
    options = Options()
    with open(CST.SELENIUM_SETTINGS) as f:
        start_options = f.readlines()
    for option in start_options:
        options.add_argument(option)

    if third_party_cookies:
        # Third Party Cookies activated
        logger.info("Using Firefox Profile with Third Party Cookies activated")
        firefox_profile_path = (
            "/home/jens/.mozilla/firefox/xjpzl3z6.Driver_3P_activated"
        )
    else:
        # Third Party Cookies deactivated
        logger.info("Using Firefox Profile with Third Party Cookies deactivated")
        firefox_profile_path = (
            "/home/jens/.mozilla/firefox/ietjlzx1.Driver_3P_deactivated"
        )

    driver_profile = webdriver.FirefoxProfile(firefox_profile_path)
    driver = webdriver.Firefox(driver_profile)
    driver.wait = WebDriverWait(driver, date.long_waiting_time())
    time.sleep(date.long_waiting_time())
    return driver


def get_soup_code_from_url(driver, url):
    driver.wait = WebDriverWait(driver, date.long_waiting_time())
    time.sleep(date.short_random_waiting_time())
    try:
        driver.get(url)
    except exceptions.TimeoutException:
        logger.warning("Get Soup Code TimeoutException for %s" % url)
        return ""

    try:
        soup = BeautifulSoup(driver.page_source, CST.PARSER)
    except exceptions.UnexpectedAlertPresentException:
        logger.warning("Make Soup UnexpectedAlertPresentException for %s" % url)
        return ""
    except exceptions.NoSuchWindowException:
        logger.warning("Make Soup NoSuchWindowException for %s" % url)
        return ""

    max_page = get_max_page(soup)
    if max_page == 1:
        return soup.prettify()
    else:
        for page in range(1, max_page):
            driver.get(url + "?p=" + str(page + 1))
            new_soup = BeautifulSoup(driver.page_source, CST.PARSER)
            soup.append(new_soup)
    return soup.prettify()


def get_soup_from_history_url(driver, url):
    driver.wait = WebDriverWait(driver, date.long_waiting_time())
    time.sleep(date.long_random_waiting_time())
    try:
        driver.get(url)
    except exceptions.TimeoutException:
        logger.warning("Get Soup Code from History URL: TimeoutException for %s" % url)
        return ""

    soup = BeautifulSoup(driver.page_source, CST.PARSER)

    if not is_data_available(soup):
        logger.warning("Get Soup Code from History URL: No Data Available for %s" % url)

    return soup.prettify()


def is_data_available(soup):
    try:
        info = soup.find(CST.HTML_DIV, {CST.HTML_ID: CST.HISTORIC_PRICE_LIST})
        return info.text.strip() != CST.NO_DATA_AVAILABLE
    except AttributeError:
        logger.warning("Data Available Check: AttributeError")
        return True


def get_max_page(soup):
    try:
        pagination = soup.find(CST.HTML_DIV, {CST.HTML_CLASS: CST.TEXT_PAGINATION})
        link_list = pagination.find_all("a")
        return int(link_list[-1].text)
    except AttributeError:
        return 1
    except:
        logger.exception("Exception at Getting Max Pagination")
        pass


def get_soup_code_from_file(file):
    try:
        with open(file, "r", encoding="UTF-8") as file:
            file_content = file.read()
        return BeautifulSoup(file_content, CST.PARSER)
    except FileNotFoundError:
        logger.warning("get_soup_code_from_file : FileNotFoundError for %s" % str(file))
        pass


def save_soup_to_file(soup, file):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, "w", encoding="UTF-8") as file:
        file.write(soup)
    return True


def close_driver(driver):
    driver.quit()
    return True
