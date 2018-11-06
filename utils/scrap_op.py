import time, os

from utils import db_op as db
from utils import date_op as date
from utils import constants as CST

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup

# urls = {'overview': ['https://www.boerse-online.de/aktie/', '-aktie'],
#         'history': ['https://www.boerse-online.de/kurse/historisch/', '/xetra/'],
#         'guv': ['https://www.boerse-online.de/bilanz_guv/', None],
#         'estimate': ['https://www.boerse-online.de/schaetzungen/', None],
#         'company': ['https://www.boerse-online.de/unternehmensprofil/', None],
#         'events': ['https://www.boerse-online.de/termine/uebersicht/', None],
#         'goals': ['https://www.boerse-online.de/kursziele/', None]}


def init_driver():
    options = Options()
    with open('utils/driver_starting_settings.txt') as f:
        start_options = f.readlines()
    for option in start_options:
        options.add_argument(option)

    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, CST.LONG_WAIT)
    return driver


def get_soup_code_from_url(driver, url):
    driver.wait = WebDriverWait(driver, CST.SHORT_WAIT)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    if not get_data_available_info(soup):
        new_url = url.replace(CST.EXCHANGE_APPENDIX, CST.ALT_EXCHANGE_APPENDIX)
        ####
        print('URL Change: %s -> %s' % (url, new_url))
        ####
        driver.wait = WebDriverWait(driver, CST.SHORT_WAIT)
        driver.get(new_url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        if not get_data_available_info(soup):
            print('*** CHECK STOCK: %s' % new_url)

    max_page = get_max_page(soup)
    if max_page == 1:
        return soup.prettify()
    else:
        for page in range(1, max_page):
            driver.get(url + '?p=' + str(page+1))
            new_soup = BeautifulSoup(driver.page_source, 'html.parser')
            soup.append(new_soup)
    return soup.prettify()


def get_data_available_info(soup):
    try:
        info = soup.find('div', {'id': 'historic-price-list'})
        return info.text.strip() != CST.NO_DATA_AVAILABLE
    except AttributeError:
        return True



def get_max_page(soup):
    try:
        pagination = soup.find('div', {'class': 'finando_paging'})
        link_list = pagination.find_all('a')
        return int(link_list[-1].text)
    except:
        return 1


def get_soup_code_from_file(file):
    with open(file, 'r') as file:
        file_content = file.read()
    return BeautifulSoup(file_content, 'html.parser')


def save_soup_to_file(soup, file):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, 'w') as file:
        file.write(soup)
    return True


# def create_stock_download_list(stock_short_link):
#     url_list = []
#     stock_shorter_link = stock_short_link[:-6]
#     date_today = date.get_todays_date()
#     date_before_one_year = date.subtract_one_year(date_today)
#     date_today_str = date.date_to_string(date_today)
#     date_before_one_year_str = date.date_to_string(date_before_one_year)
#     url_list.append(urls['overview'][0] + stock_short_link)
#     url_list.append(urls['history'][0] + stock_shorter_link + urls['history'][1] +
#                     date_before_one_year_str + '_' + date_today_str)
#     url_list.append(urls['guv'][0] + stock_shorter_link)
#     url_list.append(urls['estimate'][0] + stock_shorter_link)
#     url_list.append(urls['company'][0] + stock_shorter_link)
#     url_list.append(urls['events'][0] + stock_shorter_link)
#     url_list.append(urls['goals'][0] + stock_shorter_link)
#     return url_list


def close_driver(driver):
    driver.quit()
    return True