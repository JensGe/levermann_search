import re


from utils import date_op as date
from utils import constants as CST

from loguru import logger


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
    return [[list_[0], float(list_[1].replace('.', '').replace(',', '.')),
             float(list_[2].replace('.', '').replace(',', '.'))] for list_ in index_history]


def is_data_available(soup):
    try:
        info = soup.find(CST.HTML_DIV, {CST.HTML_CLASS: 'state_content'})
        return info.text.strip() != CST.NO_DATA_AVAILABLE_LONG
    except AttributeError:
        logger.error('Parsing Data available Check: AttributeError')
        return True


def convert_market_cap(market_cap_string):
    try:
        market_cap_value, market_cap_multiplier = market_cap_string.split(' ')
        market_cap_value = convert_ger_to_en_numeric(market_cap_value)
        if market_cap_multiplier == 'Mrd':
            market_cap_value *= 1000
        elif market_cap_multiplier == 'Tsd':
            market_cap_value /= 1000
        return market_cap_value
    except ValueError:
        if market_cap_string is None:
            logger.error('Convert Market Cap Error: market_cap_string empty')
        else:
            logger.error('Convert Market Cap Error: %s' % market_cap_string)
        pass


def convert_ger_to_en_numeric(string):
    try:
        en_numeric = float(string.replace('.', '').replace(',', '.'))
        return en_numeric
    except ValueError:
        logger.error('Convert ger2en Numeric Error for %s' % string)
        return 0


def get_market_cap(soup):
    try:
        market_cap_loc = soup.find(text=re.compile(CST.TEXT_MARKET_CAP))
        market_cap = market_cap_loc.find_next(CST.HTML_TD).contents[0].strip()
        return convert_market_cap(market_cap)
    except AttributeError:
        logger.error('Get Market Cap: AttributeError')
        pass


def get_market_place(soup):
    try:
        market_place_loc = soup.find(text=re.compile(CST.TEXT_MARKET_PLACE))
        return market_place_loc.find_next(CST.HTML_DIV).contents[0].strip()
    except AttributeError:
        logger.error('Get Market Place: AttributeError')
        pass


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


def get_current_value_of_attribute(soup, attribute):
    for elem in soup.find_all(CST.HTML_TD, text=re.compile(attribute)):
        if elem.text.strip() == attribute:
            return convert_ger_to_en_numeric(elem.parent.find_all(CST.HTML_TD)[-1].text.strip())


def get_current_value_of_attribute_old(soup, attribute):
    result_td = soup.find(CST.HTML_TD, text=re.compile(attribute))
    result_tr = result_td.parent
    result = result_tr.find_all(CST.HTML_TD)[-1].text.strip()
    return result


def get_latest_date_of_list(date_list):
    current_date = date.get_current_date()
    quarter_year_ago = date.edit_date(current_date, CST.DT_MINUS, 3, CST.DT_MONTH)
    date_list_past = [date_ for date_ in date_list if quarter_year_ago < date_ < current_date]
    try:
        return max(date_list_past)
    except ValueError:
        logger.error('Get Latest Date of List: AttributeError')
        return None


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
    return int(no_buy), int(no_hold), int(no_sell)


def get_closing_price_from_date(soup, date_str):
    result_td = soup.find(CST.HTML_TD, text=re.compile(date_str))
    result_tr = result_td.parent
    closing_price = result_tr.find_all(CST.HTML_TD)[2].text.strip()
    return convert_ger_to_en_numeric(closing_price)


def get_closing_price_from_date_before(soup, date_str):
    result_td = soup.find(CST.HTML_TD, text=re.compile(date_str))
    parent_tr = result_td.parent
    results = parent_tr.next_sibling.next_sibling.find_all(CST.HTML_TD)
    return convert_ger_to_en_numeric(results[2].text.strip())


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
                # tds.append(td.text.strip().split('\n')[3].strip())
            for a in links[:1]:
                tds.append(a[CST.HTML_HREF].split('/')[-1])
            index_stock_list.append(tds)
    return index_stock_list
