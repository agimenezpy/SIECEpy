import locale
import calendar
from datetime import datetime, date
from werkzeug.contrib import cache
import logging

LOG = logging.getLogger(__name__)

locale.setlocale(locale.LC_ALL, 'es_PY.UTF-8')

results = cache.SimpleCache()


def get_trimester(cur_date=None):
    if cur_date is None:
        now = datetime.now()
    else:
        now = cur_date
    month = now.month

    trim = ""
    for m in range(month, month + 3):
        trim += calendar.month_abbr[(m % 12)].upper()[0]
    return trim


def get_trimester_names(month=-1):
    if 0 < month < 13:
        month -= 1
    else:
        month = datetime.now().month - 1

    if results.has(month):
        return results.get(month)
    else:
        LOG.info("Cache MISS trimester %d" % month)
        trim = ", ".join([
            calendar.month_name[(month % 12) + 1].title(),
            calendar.month_name[((month + 1) % 12) + 1].title(),
            calendar.month_name[((month + 2) % 12) + 1].title(),
        ])
        results.add(month, trim)
        return trim


def test_get_trimester():
    for i in range(0, 12):
        print(i, get_trimester(date(2017, i+1, 1)))