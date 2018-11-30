from utils import constants as CST
from _datetime import datetime
import dateutil.relativedelta


def date_to_string(date):
    try:
        return datetime.strftime(date, '%d.%m.%Y')
    except ValueError:
        return datetime.strftime(date, '%d.%m.%y')


def string_to_date(string):
    try:
        return datetime.strptime(string, '%d.%m.%Y').date()
    except ValueError:
        return datetime.strptime(string, '%d.%m.%y').date()


def string_to_datetime(string):
    try:
        return datetime.strptime(string, '%d.%m.%Y')
    except ValueError:
        return datetime.strptime(string, '%d.%m.%y')


def get_current_date():
    return datetime.now().date()


def edit_date(date, operator, amount, unit):
    if unit == CST.DT_DAY:
        if operator == CST.DT_PLUS:
            return date + dateutil.relativedelta.relativedelta(days=amount)
        elif operator == CST.DT_MINUS:
            return date - dateutil.relativedelta.relativedelta(days=amount)
    elif unit == CST.DT_MONTH:
        if operator == CST.DT_PLUS:
            return date + dateutil.relativedelta.relativedelta(months=amount)
        elif operator == CST.DT_MINUS:
            return date - dateutil.relativedelta.relativedelta(months=amount)


# old

def subtract_six_months(date):
    return edit_date(date, CST.DT_MINUS, 6, CST.DT_MONTH)


def subtract_one_year(date):
    return edit_date(date, CST.DT_MINUS, 12, CST.DT_MONTH)


def add_one_day(date):
    return edit_date(date, CST.DT_PLUS, 1, CST.DT_DAY)




