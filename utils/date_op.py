from _datetime import datetime
import dateutil.relativedelta


def date_to_string(date):
    try:
        return datetime.strftime(date, '%d.%m.%Y')
    except ValueError:
        return datetime.strftime(date, '%d.%m.%y')


def string_to_date(string):
    try:
        return datetime.strptime(string, '%d.%m.%Y')
    except ValueError:
        return datetime.strptime(string, '%d.%m.%y')


def get_todays_date():
    return datetime.now().date()


def subtract_six_months(date):
    return date - dateutil.relativedelta.relativedelta(months=6)


def subtract_one_year(date):
    return date - dateutil.relativedelta.relativedelta(months=12)


def add_one_day(date):
    return date + dateutil.relativedelta.relativedelta(days=1)




