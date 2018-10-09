import time

from utils import local_scrap_op as scrap
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


def get_class_content(driver, url, class_name):
    driver.get(url)
    table_content = driver.find_element_by_class_name(class_name).text
    return table_content


def get_element_content_by_id(driver, url, id_):
    driver.get(url)
    return driver.find_element_by_id(id_)


def get_index_history_content(driver, url, index, start_date, end_date):
    driver.get(url + index + "/" + start_date + "_" + end_date)
    page = BeautifulSoup(driver.page_source, "html.parser")
    history_table = page.find_all("div", {"id": "historic-price-list"})
    return history_table


def get_index_stocks_content(driver, url, index):
    driver.get(url + index)
    page = BeautifulSoup(driver.page_source, "html.parser")
    stock_list = page.find_all("div", {"id": "index-list-container"})
    return stock_list


def extract_index_history_to_list(input_table):
    index_history = []
    table_rows = []

    for rows in input_table:
        table_rows = rows.find_all('tr')
        row_items = []
        for items in table_rows[1:]:
            row_items = items.find_all('td')
            tds = []
            for td in row_items:
                tds.append(td.text)
            index_history.append(tds)
    return index_history


# def extract_index_stocks_to_list(input_table):
#     output_table = []
#
#     table_rows = []
#     for rows in input_table:
#         table_rows = rows.find_all('tr')
#         row_items = []
#         for items in table_rows[1:]:
#             row_items = items.find_all('td')
#             tds = []
#             for td in row_items:
#                 tds.append(td.text)
#             output_table.append(tds)
#     return output_table


def save_list_table_to_history_db(input_table, name):
    print('----writing %d items to table' % (len(input_table)))
    for i in range(len(input_table)):
        db.write_data(dict(index=name,
                           datum=input_table[i][0],
                           schluss=input_table[i][1],
                           eroeffnung=input_table[i][2],
                           tageshoch=input_table[i][3],
                           tagestief=input_table[i][3]))
    return True


