#import datetime
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import numpy as np


def criticaint(valuefield: str, namefield: str) -> str:
    if valuefield.strip() == '':
        return f'{namefield} is empty'

    value = int(valuefield)

    if value < 1:
        return f'{namefield} equal zero'
    return ''


def criticastr(valuefield: str, namefield: str) -> str:
    if valuefield.strip() == '' or valuefield == None:
        return f'{namefield} is empty'
    return ''


def date_valid(data: str) -> str:
    try:
        datetime.strptime(data, '%Y-%m-%d')
    except ValueError:
        return 'Invalid Date'
    if datetime.strptime(data, '%Y-%m-%d').date() > datetime.now().date():
        return 'Arrived bigger actual date'


def first_last_day(month: int, year: int) -> tuple:
    # put 0 on left
    monthstr = str(month)
    if month < 10:
        monthstr = str('0' + str(month))

    dtini: str = str(year) + '-' + monthstr + '-01'
    dtfinal: str = date(year, month, 1)
    # add 1 to month
    dtfinal = dtfinal + relativedelta(months=1)
    # take the last day of the month
    dtfinal = dtfinal - timedelta(days=1)

    return dtini, dtfinal


def founddata(npdata: np) -> bool:
    cont = 0
    found = False
    while cont <= 11 and not found:
        if npdata[cont] > 0:
            found = True
    return found
