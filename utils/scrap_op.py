import time, os

from utils import db_op as db
from utils import date_op as date
from utils import constants as CST

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
    options.add_argument('--host-resolver-rules=MAP https://adform.net 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://s1.adform.net 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://server.adform.net 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://adscale.de 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://adscale.de 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://ih.adscale.de 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://js.adscale.de 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://gaa.adscale.de 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://ih.adscale.de 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://js.adscale.de 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://audiencemanager.de 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://prf.audiencemanager.de 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://trc.audiencemanager.de 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://digitru.st 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://digitru.st 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://cdn.digitru.st 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://cdn.digitru.st 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://doubleclick.net 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://facebook.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://facebook.net 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://connect.facebook.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://www.google-analytics.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://www.google-analytics.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://googlesyndication.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://googlesyndication.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://pagead2.googlesyndication.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://pagead2.googlesyndication.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://googletagmanager.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://www.googletagmanager.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://www.googletagservice.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://ioam.de 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://ioam.de 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://qs.ioam.de 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://ligatus.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://a.ligatus.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://ssl.ligatus.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://static.ligatus.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://m6r.eu 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://cdn.m6r.eu 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://meetrics.net 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://s400.meetrics.net 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://mxcdn.net 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://s400.mxcdn.net 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://jwpcdn.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://ssl.p.jwpcdn.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://newrelic.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://js-agent.newrelic.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://nuggad.net 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://adselect.nuggad.net 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://spotx.tv 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://js.spotx.tv 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP http://plista.com 127.0.0.1')
    options.add_argument('--host-resolver-rules=MAP https://static-de.plista.com 127.0.0.1')

    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, CST.LONG_WAIT)
    return driver


def get_soup_code_of_url(driver, url):
    driver.wait = WebDriverWait(driver, CST.SHORT_WAIT)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    max_page = get_max_page(soup)
    if max_page == 1:
        return soup.prettify()
    else:
        for page in range(1, max_page):
            driver.get(url + '?p=' + str(page+1))
            new_soup = BeautifulSoup(driver.page_source, 'html.parser')
            soup.append(new_soup)
    return soup.prettify()


def get_max_page(soup):
    try:
        pagination = soup.find('div', {'class': 'finando_paging'})
        link_list = pagination.find_all('a')
        return int(link_list[-1].text)
    except:
        return 1


def get_soup_code_of_file(file):
    with open(file, 'r') as file:
        file_content = file.read()
    return BeautifulSoup(file_content, 'html.parser')


def save_soup_to_file(soup, file):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, 'w') as file:
        file.write(soup)
    return True


def create_stock_download_list(stock_short_link):
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