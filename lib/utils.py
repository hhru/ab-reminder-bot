import datetime


def get_nearest_day_of_week(index):
    date = datetime.date.today()
    while date.weekday() != index:
        date += datetime.timedelta(1)

    return date.strftime('%Y-%m-%d')


def get_usable_date(params_date=None, defaults=None):
    if params_date is not None:
        return params_date

    if defaults is not None and 'date' in defaults and defaults['date'] is not None:
        return defaults['date']

    raise AttributeError('You must provide date either as parameter or bot settings default value')
