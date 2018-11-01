from utils import date_op as date
from utils import constants as CST
import sqlalchemy

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


def create_index_content_url_list(url_type):
    url_list = []
    index_list = get_index_names()
    for index in index_list:
        url_list.append(url_type + index)
    return url_list


def check_if_exists(search, table, column):
    with dataset.connect(CST.DATABASE) as database:
        results = database.query("SELECT %s FROM %s WHERE %s = '%s'" % (column, table, column, search))
        try:
            result = [item for item in results][0]
        except IndexError:
            return False
        return result[column] == search


def write_stock_list_to_db(stock_list, index_name):
    for stock in stock_list:
        if not check_if_exists(stock[1], 'Aktien', 'ISIN'):
            write_stock_to_stock_table(stock)
        write_stock_to_stock_contents_table(stock[1], index_name, date.get_todays_date())
    return True


def write_stock_to_stock_table(stock):
    with dataset.connect(CST.DATABASE) as database:
        database['Aktien'].insert(dict(ISIN=stock[1], Name=stock[0], URI=stock[2]))


def write_stock_to_stock_contents_table(isin, index_name, current_date):
    with dataset.connect(CST.DATABASE) as database:
        try:
            database['Indexinhalte'].insert(dict(IndexURI=index_name, AktienISIN=isin, Abrufdatum=current_date))
        except sqlalchemy.exc.IntegrityError:
            pass


def write_stock_history_to_db(index_history, index_URI):
    with dataset.connect(CST.DATABASE) as database:
        for item in index_history:
            date_ = date.string_to_date(item[0])
            start = float(item[1].replace('.', '').replace(',', '.'))
            try:
                end = float(item[2].replace('.', '').replace(',', '.'))
            except ValueError:
                print(item[2])
            try:
                database['Indexhistorien'].insert(dict(IndexURI=index_URI, Datum=date_,
                                                       Eroeffnungswert=start, Schlusswert=end))
            except sqlalchemy.exc.IntegrityError:
                pass


def get_latest_date_from_history(index_uri):
    with dataset.connect(CST.DATABASE) as database:
        results = database.query("SELECT max(Datum) as maxdate FROM %s WHERE IndexURI = '%s'" %(CST.TABLE_INDEX_HISTORIES, index_uri))
        try:
            result = [item for item in results][0]
        except IndexError:
            return False
        return result['maxdate']


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
