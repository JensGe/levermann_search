import time

from utils import db_op as db
from utils import date_op as date


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup


def init_driver():
    options = Options()
    options.add_argument("--host-resolver-rules=MAP http://bacontent.de 127.0.0.1")
    options.add_argument("--host-resolver-rules=MAP https://s.bacontent.de 127.0.0.1")
    options.add_argument("--host-resolver-rules=MAP http://facebook.net 127.0.0.1")
    options.add_argument("--host-resolver-rules=MAP https://www.google-analytics.com 127.0.0.1")
    options.add_argument("--host-resolver-rules=MAP https://pagead2.googlesyndication.com 127.0.0.1")
    options.add_argument("--host-resolver-rules=MAP https://www.googletagservice.com 127.0.0.1")
    options.add_argument("--host-resolver-rules=MAP http://ioam.de 127.0.0.1")
    options.add_argument("--host-resolver-rules=MAP http://ligatus.com 127.0.0.1")
    options.add_argument("--host-resolver-rules=MAP https://a.ligatus.com 127.0.0.1")
    options.add_argument("--host-resolver-rules=MAP http://jwpcdn.com 127.0.0.1")
    options.add_argument("--host-resolver-rules=MAP https://ssl.p.jwpcdn.com 127.0.0.1")
    options.add_argument("--host-resolver-rules=MAP http://newrelic.com 127.0.0.1")
    options.add_argument("--host-resolver-rules=MAP https://js-agent.newrelic.com 127.0.0.1")
    options.add_argument("--host-resolver-rules=MAP http://nuggad.net 127.0.0.1")
    options.add_argument("--host-resolver-rules=MAP https://adselect.nuggad.net 127.0.0.1")
    options.add_argument("--host-resolver-rules=MAP http://plista.com 127.0.0.1")
    options.add_argument("--host-resolver-rules=MAP https://static-de.plista.com 127.0.0.1")

    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 5)
    return driver


def get_max_page(soup):
    pagination = soup.find('div', {'class': 'finando_paging'})
    link_list = pagination.find_all('a')
    return int(link_list[-1].text)


# Index Histories
def get_index_history_content(driver, url, index, start_date, end_date):
    driver.get(url + index + "/" + start_date + "_" + end_date)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    history_table = soup.find_all("div", {"id": "historic-price-list"})
    return history_table


def extract_history_table_to_list(input_table):
    index_history = []
    table_rows = []

    for rows in input_table:
        table_rows = rows.find_all('tr')
        row_items = []
        for items in table_rows[1:]:
            row_items = items.find_all('td')
            tds = [td.text for td in row_items]
            index_history.append(tds)
    return index_history


def save_index_history_to_db(input_table, name):
    print('---- Writing %d items to table' % (len(input_table)))
    for i in range(len(input_table)):
        db.write_data('index_histories', dict(index=name,
                                              datum=input_table[i][0],
                                              schluss=input_table[i][1],
                                              eroeffnung=input_table[i][2],
                                              tageshoch=input_table[i][3],
                                              tagestief=input_table[i][3]))
    return True


# Index Stocks
def get_index_stocks_content(driver, url, index):
    driver.get(url + index)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    stock_list = soup.find_all('div', {'id': 'index-list-container'})
    max_page = get_max_page(soup)

    if max_page == 1:
        return [stock_list]
    else:
        complete_stock_list = [stock_list]
        for i in range(1,max_page):
            time.sleep(5)
            driver.get(url + index + '?p=' + str(i+1))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            stock_list = soup.find_all('div', {'id': 'index-list-container'})
            complete_stock_list.append(stock_list)
    return complete_stock_list


def extract_index_stocks_to_list(input_table):
    index_stock_list = []
    table_rows = []
    for rows in input_table:
        table_rows = rows.find_all('tr')
        row_items = []
        for items in table_rows[1:]:
            row_items = items.find_all('td')
            links = items.find_all('a')
            tds = []
            for td in row_items[:1]:
                tds.append(td.text.strip().split('\n')[0])
                tds.append(td.text.strip().split('\n')[1])
            for a in links[:1]:
                tds.append(a['href'].split('/')[-1])
            index_stock_list.append(tds)
    return index_stock_list


def update_index_stocks_db(input_table, name):
    print('---- Writing %d items to table' % (len(input_table)))
    db.clear_index_contents('index_stocks', name)
    for i in range(len(input_table)):
        db.write_data('index_stocks', dict(index=name,
                                           stock_name=input_table[i][0],
                                           ISIN=input_table[i][1],
                                           stock_link=input_table[i][2],
                                           last_update=date.date_to_string(date.get_todays_date())))
    return True


# Stock Histories
def get_stock_history_content(driver, url, start_date, end_date):
    driver.get(url[:-6] + "/fse/" + start_date + "_" + end_date)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    history_table = soup.find_all("div", {"id": "historic-price-list"})
    return history_table


def save_stock_history_to_db(input_table, index_name, stock_name, isin):
    print('---- Writing %d items to table' % (len(input_table)))
    for i in range(len(input_table)):
        db.write_data('stock_histories', dict(stock=stock_name,
                                              isin=isin,
                                              index=index_name,
                                              datum=input_table[i][0],
                                              schluss=input_table[i][1],
                                              eroeffnung=input_table[i][2],
                                              tageshoch=input_table[i][3],
                                              tagestief=input_table[i][3]))
    return True