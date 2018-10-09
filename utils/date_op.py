from _datetime import datetime
import dateutil.relativedelta


def date_to_string(date):
    return datetime.strftime(date, '%d.%m.%Y')


def string_to_date(string):
    return datetime.strptime(string, '%d.%m.%Y')


def get_todays_date():
    return datetime.now()


def subtract_six_months(date):
    return date - dateutil.relativedelta.relativedelta(months=6)


def subtract_one_year(date):
    return date - dateutil.relativedelta.relativedelta(months=12)


def add_one_day(date):
    return date + dateutil.relativedelta.relativedelta(days=1)




