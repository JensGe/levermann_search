from datetime import datetime
from utils import date_op as date

import dataset


def write_data(dictionary):
    with dataset.connect('sqlite:///stockbase.db') as tx:
        tx['index_histories'].insert(dictionary)


def get_max_date_of_index_history(index_name):
    db = dataset.connect('sqlite:///stockbase.db')
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


def get_closing_price_from_date(request_date, index_name):
    db = dataset.connect('sqlite:///stockbase.db')
    q_date = date.date_to_string(request_date)
    result = db.get_table('index_histories').find(datum=q_date, index=index_name)
    for value in result:
        return value['schluss']
