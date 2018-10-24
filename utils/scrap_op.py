import time, os

from utils import db_op as db
from utils import date_op as date

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup

urls = {'overview': ['https://www.boerse-online.de/aktie/', '-aktie'],
        'history': ['https://www.boerse-online.de/kurse/historisch/', '/xetra/'],
        'guv': ['https://www.boerse-online.de/bilanz_guv/', None],
        'estimate': ['https://www.boerse-online.de/schaetzungen/', None],
        'company': ['https://www.boerse-online.de/unternehmensprofil/', None],
        'events': ['https://www.boerse-online.de/termine/uebersicht/', None],
        'goals': ['https://www.boerse-online.de/kursziele/', None]}


def init_driver():
    options = Options()
    options.add_argument('--host-resolver-rules=MAP http://bacontent.de 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://s.bacontent.de 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://facebook.net 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://www.google-analytics.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://pagead2.googlesyndication.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://www.googletagservice.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://ioam.de 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://ligatus.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://a.ligatus.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://jwpcdn.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://ssl.p.jwpcdn.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://newrelic.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://js-agent.newrelic.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://nuggad.net 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://adselect.nuggad.net 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://plista.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://static-de.plista.com 127.0.0.1')

    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 5)
    return driver


def get_soup_code_of_url(driver, url):
    driver.get(url)
    return BeautifulSoup(driver.page_source, 'html.parser').prettify('utf-8')


def get_soup_code_of_file(file):
    with open(file, 'r') as file:
        file_content = file.read()
    return BeautifulSoup(file_content, 'html.parser')


def save_soup_to_file(soup, file):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, 'wb') as file:
        file.write(soup)
    return True


def create_download_list(stock_short_link):
    url_list = []
    stock_shorter_link = stock_short_link[:-6]
    date_today = date.get_todays_date()
    date_before_one_year = date.subtract_one_year(date_today)
    date_today_str = date.date_to_string(date_today)
    date_before_one_year_str = date.date_to_string(date_before_one_year)
    url_list.append(urls['overview'][0] + stock_short_link)
    url_list.append(urls['history'][0] + stock_shorter_link + urls['history'][1] + date_before_one_year_str + '_' + date_today_str)
    url_list.append(urls['guv'][0] + stock_shorter_link)
    url_list.append(urls['estimate'][0] + stock_shorter_link)
    url_list.append(urls['company'][0] + stock_shorter_link)
    url_list.append(urls['events'][0] + stock_shorter_link)
    url_list.append(urls['goals'][0] + stock_shorter_link)
    return url_list


def close_driver(driver):
    driver.quit()
    return True