from utils import date_op as date
from utils import constants as CST

import dataset


def get_index_names():
    with dataset.connect(CST.DATABASE) as database:
        index_list = [item['URI'] for item in database['Aktienindizes']]
    return index_list


def get_pages_count(index_name):
    with dataset.connect(CST.DATABASE) as database:
        table = database['Aktienindizes'].find(URI=index_name)
        result = [item['Seiten'] for item in table]
        return int(result[0])


def create_index_content_url_list():
    url_list = []
    index_list = get_index_names()
    for index in index_list:
        for i in range(get_pages_count(index)):
            url_list.append(CST.URL_INDEX_CONTENT + index + '?p=' + str(i+1))
    return url_list




######## OLD
################################################
def select_data(table):
    with dataset.connect(CST.DATABASE) as tx:
        print(tx[table])


def write_data(table_name, dictionary):
    with dataset.connect(CST.DATABASE) as tx:
        tx[table_name].insert(dictionary)

# def write_data(table_name, dictionary):
#     with dataset.connect('sqlite:///data/stockbase.db') as tx:
#         tx[table_name].insert(dictionary)


def clear_index_contents(table_name, index_name):
    """
    Deletes all rows in a table with a given index_name
    :param table_name: table, where the deletion has to be
    :param index_name: filtering one index_name, which will be cleared
    :return:
    """
    with dataset.connect('sqlite:///data/stockbase.db') as tx:
        tx[table_name].delete(index=index_name)
    return True


def get_max_date_of_index_history(index_name):
    db = dataset.connect('sqlite:///data/stockbase.db')
    try:
        dates = db.get_table('index_histories').find(index=index_name)
    except:
        return False

    date_list = []
    for item in dates:
        date_list.append(date.string_to_date(item['datum']))

    if len(date_list) == 0:
        return False
    max_date = sorted(date_list, reverse=True)[0]
    max_date_str = date.date_to_string(max_date)
    return max_date_str


def get_max_date_of_stock_history(stock_name):
    db = dataset.connect('sqlite:///data/stockbase.db')
    try:
        dates = db.get_table('stock_histories').find(stock=stock_name)
    except:
        return False

    date_list = []
    for item in dates:
        date_list.append(date.string_to_date(item['datum']))

    if len(date_list) == 0:
        return False
    max_date = sorted(date_list, reverse=True)[0]
    max_date_str = date.date_to_string(max_date)
    return max_date_str


def get_closing_price_from_date(request_date, index_name):
    db = dataset.connect('sqlite:///data/stockbase.db')
    q_date = date.date_to_string(request_date)
    result = db.get_table('index_histories').find(datum=q_date, index=index_name)
    for value in result:
        return value['schluss']


def get_all_stock_infos(index_name):
    db = dataset.connect('sqlite:///data/stockbase.db')
    try:
        urls = db.get_table('index_stocks').find(index=index_name)
    except:
        return False
    url_list = []
    for url in urls:
        url_list.append([url['stock_name'], url['ISIN'], url['stock_link']])
    return url_list
