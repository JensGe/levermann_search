from utils import local_scrap_op as scrap
from utils import db_op as db
from utils import date_op as date
from Scrapper import index_history_scrapper as ihs


index_history_url = "https://www.boerse-online.de/index/historisch/"
index_stocks_url = "https://www.boerse-online.de/index/liste/"

div_id = "historic-price-list"


def select_intervall(index_name):
    """ calculate Intervall to be used in scrapping
        therefore uses latest date in DB + 1
        if DB is empty, the intervall will be one year ago to today
    :param index_name: the stockindex's name
    :return: start_date_str, end_date_str: as strings
    """
    today_date = date.get_todays_date()
    start_date = date.subtract_one_year(today_date)

    max_db_date = db.get_max_date_of_index_history(index_name)

    if max_db_date:
        start_date = date.add_one_day(date.string_to_date(max_db_date))

    start_date_str = date.date_to_string(start_date)
    end_date_str = date.date_to_string(today_date)

    print("Searching %s - Index from %s to %s" % (index_name, start_date_str, end_date_str))
    return start_date_str, end_date_str


def refresh_index_history(index_name, start_date_str, end_date_str):
    """
    Updates index history with most current values
    """

    if date.string_to_date(start_date_str) >= date.string_to_date(end_date_str):
        print("---- Enddate less or equal than start date --- Dont Scrap")
        return False
    # start scrapping with calculated intervall
    driver = ihs.init_driver()
    content = ihs.get_index_history_content(driver, index_history_url, index_name, start_date_str, end_date_str)

    list_table = ihs.extract_index_history_to_list(content)
    ihs.save_list_table_to_history_db(list_table, index_name)

    driver.quit()
    return True


def refresh_index_stocks(index_name):
    """
    Updates the stocks in each index
    """
