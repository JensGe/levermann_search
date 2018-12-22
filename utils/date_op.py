from utils import constants as CST
from _datetime import datetime
from _datetime import date

import random
import dateutil.relativedelta


# Date and Strings
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


def get_year_and_week_string(date_time):
    year_and_week = '%d-%d' % (datetime.date(date_time).isocalendar()[0], datetime.date(date_time).isocalendar()[1])
    return year_and_week


# Date
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


def subtract_one_year(date):
    return edit_date(date, CST.DT_MINUS, 12, CST.DT_MONTH)


def add_one_day(date):
    return edit_date(date, CST.DT_PLUS, 1, CST.DT_DAY)


def get_last_days_of_last_four_months():
    current_year = get_current_date().year
    current_month = get_current_date().month
    first_day = 1

    first_day_of_current_month = date(current_year, current_month, first_day)
    last_day_last_month = edit_date(first_day_of_current_month, CST.DT_MINUS, 1, CST.DT_DAY)

    first_day_last_month = edit_date(first_day_of_current_month, CST.DT_MINUS, 1, CST.DT_MONTH)
    last_day_second_last_month = edit_date(first_day_last_month, CST.DT_MINUS, 1, CST.DT_DAY)

    first_day_second_last_month = edit_date(first_day_of_current_month, CST.DT_MINUS, 2, CST.DT_MONTH)
    last_day_third_last_month = edit_date(first_day_second_last_month, CST.DT_MINUS, 1, CST.DT_DAY)

    first_day_third_last_month = edit_date(first_day_of_current_month, CST.DT_MINUS, 3, CST.DT_MONTH)
    last_day_forth_last_month = edit_date(first_day_third_last_month, CST.DT_MINUS, 1, CST.DT_DAY)

    return [last_day_forth_last_month, last_day_third_last_month, last_day_second_last_month, last_day_last_month]


# Times
def long_waiting_time():
    return CST.LONG_WAIT


def short_waiting_time():
    return CST.SHORT_WAIT


def long_random_waiting_time():
    return CST.LONG_WAIT + random.uniform(0, CST.RANDOM_WAIT_RANGE)


def short_random_waiting_time():
    return CST.SHORT_WAIT + random.uniform(0, CST.RANDOM_WAIT_RANGE)
