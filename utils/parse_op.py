import re

from utils import date_op as date
from utils import constants as cst

from loguru import logger


# Historic Prices of Stocks and Indices
def get_historic_prices_from_history(soup):
    history_table = soup.find_all(cst.HTML_DIV, {cst.HTML_ID: cst.HISTORIC_PRICE_LIST})
    index_history = []
    for rows in history_table:
        for items in rows.find_all(cst.HTML_TR)[1:]:
            tds = [td.text.strip() for td in items.find_all(cst.HTML_TD)]
            index_history.append(tds)
    return index_history


def get_historic_stock_prices_from_overview(soup):
    try:
        history_table = soup.find(
            cst.HTML_H2, text=re.compile(cst.TEXT_HISTORIC_PRICES)
        ).next_sibling.next_sibling
    except AttributeError:
        logger.error(
            "AttributeError when Parsing Overview for Stock History, must be empty"
        )
        return None
    return_history = []
    for row in history_table.find_all(cst.HTML_TR)[:-1]:
        tr_items = []
        for items in row.find_all(cst.HTML_TD)[:2]:
            tr_items.append(items.text.strip())
        return_history.append(tr_items)
    return return_history


def convert_index_history_list(index_history):
    return [
        [
            list_[0],
            float(list_[1].replace(".", "").replace(",", ".")),
            float(list_[2].replace(".", "").replace(",", ".")),
        ]
        for list_ in index_history
    ]


def is_data_available(soup):
    try:
        info = soup.find(cst.HTML_DIV, {cst.HTML_CLASS: "state_content"})
        return info.text.strip() != cst.NO_DATA_AVAILABLE_LONG
    except AttributeError:
        logger.error("Parsing Data available Check: AttributeError")
        return True


def get_stock_list_of_single_index(soup):
    stock_table = soup.find_all(
        cst.HTML_DIV, {cst.HTML_ID: cst.TEXT_INDEX_LIST_CONTAINER}
    )
    stock_list = extract_index_stocks_to_list(stock_table)
    return stock_list


def extract_index_stocks_to_list(input_table):
    index_stock_list = []
    for rows in input_table:
        for items in rows.find_all(cst.HTML_TR)[1:]:
            links = items.find_all(cst.HTML_A)
            tds = []
            for td in items.find_all(cst.HTML_TD)[:1]:
                tds.append(td.text.strip().split("\n")[0])
            for a in links[:1]:
                tds.append(a[cst.HTML_HREF].split("/")[-1])
            index_stock_list.append(tds)
    return index_stock_list


# Stocks - Overview
def convert_market_cap(market_cap_string):
    try:
        market_cap_value, market_cap_multiplier = market_cap_string.split(" ")
        market_cap_value = convert_ger_to_en_numeric(market_cap_value)
        if market_cap_multiplier == "Mrd":
            market_cap_value *= 1000
        elif market_cap_multiplier == "Tsd":
            market_cap_value /= 1000
        return market_cap_value
    except ValueError:
        if market_cap_string is None:
            logger.error("Convert Market Cap Error: market_cap_string empty")
        else:
            logger.error("Convert Market Cap Error: %s" % market_cap_string)
        pass


def convert_ger_to_en_numeric(string):
    try:
        en_numeric = float(string.replace(".", "").replace(",", "."))
        return en_numeric
    except ValueError:
        logger.error("Convert ger2en Numeric Error for %s" % string)
        return 0


def get_market_cap(soup):
    try:
        market_cap_loc = soup.find(text=re.compile(cst.TEXT_MARKET_CAP))
        market_cap = market_cap_loc.find_next(cst.HTML_TD).contents[0].strip()
        return convert_market_cap(market_cap)
    except AttributeError:
        logger.error("Get Market Cap: AttributeError")
        pass


def get_market_place(soup):
    try:
        market_place_loc = soup.find(text=re.compile(cst.TEXT_MARKET_PLACE))
        return market_place_loc.find_next(cst.HTML_DIV).contents[0].strip()
    except AttributeError:
        logger.error("Get Market Place: AttributeError")
        pass


def get_listed_indizes(soup):
    indizes = soup.find_all(cst.HTML_H2, text=re.compile(cst.TEXT_LISTED_INDIZES))
    parent = []
    for par in indizes:
        parent.append(par.parent)
    link_items = []
    for items in parent:
        links = items.find_all(cst.HTML_A)
        for link in links:
            link_items.append(link.text.strip())
    return link_items


def get_sectors(soup):
    sectors = soup.find_all(cst.HTML_H2, text=re.compile(cst.TEXT_COMPANY_INFO))
    parent = []
    for item in sectors:
        parent.append(item.parent)
    link_items = []
    for items in parent:
        links = items.find_all(cst.HTML_A)
        for link in links:
            link_items.append(link.text.strip())
    return link_items


# Stock - Dates
def get_latest_date_of_list(date_list, current_date=date.get_current_date()):
    quarter_year_ago = date.edit_date(current_date, cst.DT_MINUS, 3, cst.DT_MONTH)
    date_list_past = [
        date_ for date_ in date_list if quarter_year_ago < date_ < current_date
    ]
    try:
        return max(date_list_past)
    except ValueError:
        logger.error(
            "Get Latest Date of List: AttributeError. "
            "Last Date probably not in last quarter"
        )
        return None


def get_last_quarterly_figures_date(soup, current_date=date.get_current_date()):
    """
    Calculates the newest, but in the past lying date, where a company event has
    been held. Returns a date-object
    :param soup:
    :return: date
    """
    result_td = soup.find(cst.HTML_H2, text=re.compile(cst.TEXT_BYGONE_DATES))
    parent_div = result_td.parent
    dates = parent_div.find_all(cst.HTML_TD, {cst.HTML_CLASS: cst.TEXT_TEXT_RIGHT})
    date_list = [date.string_to_date(date_.text.strip()) for date_ in dates]
    latest_date = get_latest_date_of_list(date_list, current_date=current_date)
    return latest_date


def get_future_dates(soup):
    result_header = soup.find(cst.HTML_H1, text=re.compile(cst.TEXT_FUTURE_DATES))
    parent_div = result_header.parent
    result_trs = parent_div.find_all(cst.HTML_TR)
    return_list = []
    for tr in result_trs[1:]:
        temp_list = [td.text.strip() for td in tr if td != "\n"]
        reordered_temp_list = [
            temp_list[0],
            date.convert_parse_to_date_db_string(temp_list[2]),
            temp_list[1],
            "Future",
        ]
        return_list.append(reordered_temp_list)

    return return_list


def get_bygone_dates(soup):
    result_header = soup.find(cst.HTML_H2, text=re.compile(cst.TEXT_BYGONE_DATES))
    stock = result_header.text.strip()
    parent_div = result_header.parent
    result_trs = parent_div.find_all(cst.HTML_TR)
    return_list = []
    for tr in result_trs[1:]:
        temp_list = [td.text.strip() for td in tr if td != "\n"]
        reordered_temp_list = [
            stock.replace(cst.TEXT_BYGONE_DATES, "").strip(),
            date.convert_parse_to_date_db_string(temp_list[2]),
            temp_list[0] if temp_list[1] == "" else temp_list[1],
            "Past",
        ]
        return_list.append(reordered_temp_list)

    return return_list


# Stock - Balance
def get_current_value_of_attribute(soup, attribute):
    for elem in soup.find_all(cst.HTML_TD, text=re.compile(attribute)):
        if elem.text.strip() == attribute:
            return convert_ger_to_en_numeric(
                elem.parent.find_all(cst.HTML_TD)[-1].text.strip()
            )


def get_result_per_share_last_three_years(soup):
    result_td = soup.find(cst.HTML_TD, text=re.compile(cst.TEXT_EPS_UNDILUTED))
    result_tr = result_td.parent

    result_minus_3 = result_tr.find_all(cst.HTML_TD)[-3].text.strip()
    result_minus_2 = result_tr.find_all(cst.HTML_TD)[-2].text.strip()
    result_minus_1 = result_tr.find_all(cst.HTML_TD)[-1].text.strip()
    return (
        convert_ger_to_en_numeric(result_minus_3),
        convert_ger_to_en_numeric(result_minus_2),
        convert_ger_to_en_numeric(result_minus_1),
    )


def get_result_per_share_current_and_next_year(soup):
    result_td = soup.find(cst.HTML_TD, text=re.compile(cst.TEXT_EPS))
    result_tr = result_td.parent
    result_current = result_tr.find_all(cst.HTML_TD)[3].text.strip()
    result_plus1 = result_tr.find_all(cst.HTML_TD)[4].text.strip()
    return (
        convert_ger_to_en_numeric(result_current),
        convert_ger_to_en_numeric(result_plus1),
    )


# Stock - Targets
def get_analyst_ratings(soup):
    result_td = soup.find(cst.HTML_TD, {cst.HTML_CLASS: cst.TEXT_HISTORIC_RATING})
    values = result_td.find_all(cst.HTML_SPAN)
    analyst_list = [
        value.text.strip() for value in values if value.has_attr(cst.HTML_ID)
    ]
    no_buy, no_hold, no_sell = analyst_list[0], analyst_list[1], analyst_list[2]
    return int(no_buy), int(no_hold), int(no_sell)


def get_closing_price_from_date(soup, date_str):
    result_td = soup.find(cst.HTML_TD, text=re.compile(date_str))
    result_tr = result_td.parent
    closing_price = result_tr.find_all(cst.HTML_TD)[2].text.strip()
    return convert_ger_to_en_numeric(closing_price)


def get_closing_price_from_date_before(soup, date_str):
    result_td = soup.find(cst.HTML_TD, text=re.compile(date_str))
    parent_tr = result_td.parent
    results = parent_tr.next_sibling.next_sibling.find_all(cst.HTML_TD)
    return convert_ger_to_en_numeric(results[2].text.strip())
