import time

from utils import db_op as db
from utils import date_op as date


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup


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
    with open(file, 'wb') as file:
        file.write(soup)
    return True
