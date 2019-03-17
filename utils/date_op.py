from utils import constants as cst
from _datetime import datetime
from _datetime import date

import random
import calendar
import dateutil.relativedelta


# Date vs Strings
def date_to_string(date):
    try:
        return datetime.strftime(date, "%d.%m.%Y")
    except ValueError:
        return datetime.strftime(date, "%d.%m.%y")


def string_to_date(string):
    try:
        return datetime.strptime(string, "%d.%m.%Y").date()
    except ValueError:
        return datetime.strptime(string, "%d.%m.%y").date()


def convert_parse_to_date_db_string(string):
    split_list = string.split(".")
    conv_string = "20%s-%s-%s" % (split_list[2], split_list[1], split_list[0])
    return conv_string


# Date
def get_current_date():
    return datetime.now().date()


def edit_date(date, operator, amount, unit):
    if unit == cst.DT_DAY:
        if operator == cst.DT_PLUS:
            return date + dateutil.relativedelta.relativedelta(days=amount)
        elif operator == cst.DT_MINUS:
            return date - dateutil.relativedelta.relativedelta(days=amount)
    elif unit == cst.DT_MONTH:
        if operator == cst.DT_PLUS:
            return date + dateutil.relativedelta.relativedelta(months=amount)
        elif operator == cst.DT_MINUS:
            return date - dateutil.relativedelta.relativedelta(months=amount)


def subtract_one_year(date):
    return edit_date(date, cst.DT_MINUS, 12, cst.DT_MONTH)


def add_one_day(date):
    return edit_date(date, cst.DT_PLUS, 1, cst.DT_DAY)


def get_last_days_of_last_four_months(input_date):
    current_year = input_date.year
    current_month = input_date.month
    first_day = 1

    first_day_of_current_month = date(current_year, current_month, first_day)
    last_day_last_month = edit_date(
        first_day_of_current_month, cst.DT_MINUS, 1, cst.DT_DAY
    )

    first_day_last_month = edit_date(
        first_day_of_current_month, cst.DT_MINUS, 1, cst.DT_MONTH
    )
    last_day_second_last_month = edit_date(
        first_day_last_month, cst.DT_MINUS, 1, cst.DT_DAY
    )

    first_day_second_last_month = edit_date(
        first_day_of_current_month, cst.DT_MINUS, 2, cst.DT_MONTH
    )
    last_day_third_last_month = edit_date(
        first_day_second_last_month, cst.DT_MINUS, 1, cst.DT_DAY
    )

    first_day_third_last_month = edit_date(
        first_day_of_current_month, cst.DT_MINUS, 3, cst.DT_MONTH
    )
    last_day_forth_last_month = edit_date(
        first_day_third_last_month, cst.DT_MINUS, 1, cst.DT_DAY
    )

    return [
        last_day_forth_last_month,
        last_day_third_last_month,
        last_day_second_last_month,
        last_day_last_month,
    ]


# Wait / Sleep Timings
def long_waiting_time():
    return cst.LONG_WAIT


def short_waiting_time():
    return cst.SHORT_WAIT


def long_random_waiting_time():
    return cst.LONG_WAIT + random.uniform(0, cst.RANDOM_WAIT_RANGE)


def short_random_waiting_time():
    return cst.SHORT_WAIT + random.uniform(0, cst.RANDOM_WAIT_RANGE)


# Queue Calculator
def get_first_friday_of_months(year):
    month_list = []
    for month_ in range(1, 13):
        month_calendar = calendar.monthcalendar(year, month_)
        week1 = month_calendar[0]
        week2 = month_calendar[1]

        if week1[calendar.FRIDAY] != 0:
            week_day_no = date(year=year, month=month_, day=week1[calendar.FRIDAY])
        else:
            week_day_no = date(year=year, month=month_, day=week2[calendar.FRIDAY])

        month_list.append(week_day_no)

    return month_list


def get_first_and_third_friday_of_months(year):
    monthly_date_list = get_first_friday_of_months(year=year)
    biweekly_list = []
    for date_ in monthly_date_list:
        biweekly_list.append(date_)
        biweekly_list.append(edit_date(date_, cst.DT_PLUS, 14, cst.DT_DAY))
    return biweekly_list
