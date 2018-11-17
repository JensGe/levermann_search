import re
import time

from utils import db_op as db
from utils import date_op as date
from utils import scrap_op as scrap
from utils import constants as CST

from bs4 import BeautifulSoup


# Index Histories
def get_historic_prices(soup):
    history_table = soup.find_all(CST.HTML_DIV, {CST.HTML_ID: CST.HISTORIC_PRICE_LIST})
    index_history = []
    table_rows = []
    for rows in history_table:
        table_rows = rows.find_all(CST.HTML_TR)
        row_items = []
        for items in table_rows[1:]:
            row_items = items.find_all(CST.HTML_TD)
            tds = [td.text.strip() for td in row_items]
            index_history.append(tds)
    return index_history


def convert_index_history_list(index_history):
    return [[list_[0], float(list_[1].replace('.','').replace(',','.')), float(list_[2].replace('.','').replace(',','.'))] for list_ in index_history]


def extract_history_table_to_list(input_table):
    index_history = []
    table_rows = []

    for rows in input_table:
        table_rows = rows.find_all(CST.HTML_TR)
        row_items = []
        for items in table_rows[1:]:
            row_items = items.find_all(CST.HTML_TD)
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
    soup = BeautifulSoup(driver.page_source, CST.PARSER)
    stock_list = soup.find_all(CST.HTML_DIV, {CST.HTML_ID: CST.TEXT_INDEX_LIST_CONTAINER})
    max_page = scrap.get_max_page(soup)

    if max_page == 1:
        return [stock_list]
    else:
        complete_stock_list = [stock_list]
        for i in range(1,max_page):
            time.sleep(5)
            driver.get(url + index + '?p=' + str(i+1))
            soup = BeautifulSoup(driver.page_source, CST.PARSER)
            stock_list = soup.find_all(CST.HTML_DIV, {CST.HTML_ID: CST.TEXT_INDEX_LIST_CONTAINER})
            complete_stock_list.append(stock_list)
    return complete_stock_list


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
    driver.get(url[:-6] + CST.EXCHANGE_APPENDIX + '/' + start_date + "_" + end_date)
    soup = BeautifulSoup(driver.page_source, CST.PARSER)
    history_table = soup.find_all(CST.HTML_DIV, {CST.HTML_ID: CST.HISTORIC_PRICE_LIST})
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


# V2
# Stock / Company Infos

def convert_market_cap(market_cap_string):
    market_cap_value, market_cap_multiplier = market_cap_string.split(' ')
    market_cap_value = convert_ger_to_en_numeric(market_cap_value)
    if market_cap_multiplier == 'Mrd':
        market_cap_value *= 1000
    elif market_cap_multiplier == 'Tsd':
        market_cap_value /= 1000
    return market_cap_value


def convert_ger_to_en_numeric(string):
    return float(string.replace('.', '').replace(',', '.'))


def get_market_cap(soup):
    market_cap_loc = soup.find(text=re.compile(CST.TEXT_MARKET_CAP))
    market_cap = market_cap_loc.find_next(CST.HTML_TD).contents[0].strip()
    return convert_market_cap(market_cap)


def get_listed_indizes(soup):
    indizes = soup.find_all(CST.HTML_H2, text=re.compile(CST.TEXT_LISTED_INDIZES))
    parent = []
    for par in indizes:
        parent.append(par.parent)
    link_items = []
    for items in parent:
        links = items.find_all(CST.HTML_A)
        for link in links:
            link_items.append(link.text.strip())
    return link_items


def get_sectors(soup):
    sectors = soup.find_all(CST.HTML_H2, text=re.compile(CST.TEXT_COMPANY_INFO))
    parent = []
    for item in sectors:
        parent.append(item.parent)
    link_items = []
    for items in parent:
        links = items.find_all(CST.HTML_A)
        for link in links:
            link_items.append(link.text.strip())
    return link_items


def get_result_after_tax(soup):
    result_td = soup.find(CST.HTML_TD, text=re.compile(CST.TEXT_RESULT_AFTER_TAX))
    result_tr = result_td.parent
    result_after_tax = result_tr.find_all(CST.HTML_TD)[-1].text.strip()
    return convert_ger_to_en_numeric(result_after_tax)


def get_operative_result(soup):
    result_td = soup.find(CST.HTML_TD, text=re.compile(CST.TEXT_OPERATIVE_RESULT))
    result_tr = result_td.parent
    operative_result = result_tr.find_all(CST.HTML_TD)[-1].text.strip()
    return convert_ger_to_en_numeric(operative_result)


def get_sales_revenue(soup):
    result_td = soup.find(CST.HTML_TD, text=re.compile(CST.TEXT_SALES_REVENUE))
    result_tr = result_td.parent
    sales_revenue = result_tr.find_all(CST.HTML_TD)[-1].text.strip()
    return convert_ger_to_en_numeric(sales_revenue)


def get_total_assets(soup):
    result_td = soup.find(CST.HTML_TD, text=re.compile(CST.TEXT_TOTAL_ASSETS))
    result_tr = result_td.parent
    total_assets = result_tr.find_all(CST.HTML_TD)[-1].text.strip()
    return convert_ger_to_en_numeric(total_assets)


def get_current_value_of_attribute(soup, attribute):
    result_td = soup.find(CST.HTML_TD, text=re.compile(attribute))
    result_tr = result_td.parent
    result = result_tr.find_all(CST.HTML_TD)[-1].text.strip()
    return result


def get_latest_date_of_list(date_list):
    current_date = date.get_todays_date()
    date_list_past = [date_ for date_ in date_list if date_ < current_date]
    max_date = max(date_list_past)
    return max_date


def get_last_quarterly_figures_date(soup):
    """
    Calculates the newest, but in the past lying date, where a company event has
    been held. Returns a date-object
    :param soup:
    :return: date
    """
    result_td = soup.find(CST.HTML_H2, text=re.compile(CST.TEXT_LAST_DATES))
    parent_div = result_td.parent
    dates = parent_div.find_all(CST.HTML_TD, {CST.HTML_CLASS: CST.TEXT_TEXT_RIGHT})
    date_list = [date.string_to_date(date_.text.strip()) for date_ in dates]
    latest_date = get_latest_date_of_list(date_list)
    return latest_date


def get_result_per_share_last_three_years(soup):
    result_td = soup.find(CST.HTML_TD, text=re.compile(CST.TEXT_EPS_UNDILUTED))
    result_tr = result_td.parent
    result_minus_3 = result_tr.find_all(CST.HTML_TD)[-3].text.strip()
    result_minus_2 = result_tr.find_all(CST.HTML_TD)[-2].text.strip()
    result_minus_1 = result_tr.find_all(CST.HTML_TD)[-1].text.strip()
    return convert_ger_to_en_numeric(result_minus_3), \
           convert_ger_to_en_numeric(result_minus_2), \
           convert_ger_to_en_numeric(result_minus_1)


def get_result_per_share_current_and_next_year(soup):
    result_td = soup.find(CST.HTML_TD, text=re.compile(CST.TEXT_EPS))
    result_tr = result_td.parent
    result_current = result_tr.find_all(CST.HTML_TD)[3].text.strip()
    result_plus1 = result_tr.find_all(CST.HTML_TD)[4].text.strip()
    return convert_ger_to_en_numeric(result_current), \
           convert_ger_to_en_numeric(result_plus1)


def get_analyst_ratings(soup):
    result_td = soup.find(CST.HTML_TD, {CST.HTML_CLASS: CST.TEXT_HISTORIC_RATING})
    values = result_td.find_all(CST.HTML_SPAN)
    list = [value.text.strip() for value in values if value.has_attr(CST.HTML_ID)]
    no_buy, no_hold, no_sell = list[0], list[1], list[2]
    return no_buy, no_hold, no_sell


def get_closing_price_from_date(soup, date_str):
    result_td = soup.find(CST.HTML_TD, text=re.compile(date_str))
    result_tr = result_td.parent
    closing_price = result_tr.find_all(CST.HTML_TD)[2].text.strip()
    return convert_ger_to_en_numeric(closing_price)


def get_closing_price_from_date_before(soup, date_str):
    result_td = soup.find(CST.HTML_TD, text=re.compile(date_str))
    parent_tr = result_td.parent
    results = parent_tr.next_sibling.next_sibling.find_all(CST.HTML_TD)
    return results[2].text.strip()


def get_stock_list_of_single_index(soup):
    stock_table = soup.find_all(CST.HTML_DIV, {CST.HTML_ID: CST.TEXT_INDEX_LIST_CONTAINER})
    stock_list = extract_index_stocks_to_list(stock_table)
    return stock_list


def extract_index_stocks_to_list(input_table):
    index_stock_list = []
    table_rows = []
    for rows in input_table:
        table_rows = rows.find_all(CST.HTML_TR)
        row_items = []
        for items in table_rows[1:]:
            row_items = items.find_all(CST.HTML_TD)
            links = items.find_all(CST.HTML_A)
            tds = []
            for td in row_items[:1]:
                tds.append(td.text.strip().split('\n')[0])
                tds.append(td.text.strip().split('\n')[3].strip())
            for a in links[:1]:
                tds.append(a[CST.HTML_HREF].split('/')[-1])
            index_stock_list.append(tds)
    return index_stock_list
