# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from os import walk, path, listdir
from re import match
from . import (REGIONS, SCENARIOS, VARIABLES, MATCHES, PERIODS, MEMBERS)
from project.utils.dates import get_trimester_names
import logging
from itertools import groupby

LOG = logging.getLogger(__name__)


def file_list(directory):
    matches = []
    for root, dirnames, filenames in walk(directory):
        matches.extend([path.join(root, filename) for filename in filenames])
    return matches


class ClimateModel(object):

    def __init__(self, model, directory):
        prec = []
        temp = []

        if model in listdir(directory):
            filenames = file_list(path.join(directory, model))

            for filename in filenames:
                groups = match(".*" + MATCHES[model], filename)
                if groups is not None:
                    meta = groups.groupdict()
                    if meta['variable'] == '' and '_t' in filename:
                        meta['variable'] = 't'
                    elif meta['variable'] == '':
                        meta['variable'] = 'p'
                    result = dict(
                        variable=VARIABLES[meta['variable']],
                        content=filename.replace(directory, "")
                    )
                    if 'region' in meta:
                        result['region'] = meta['region']
                        result['region_name'] = REGIONS[meta[
                            'region']].decode("utf-8")
                    else:
                        result['region'] = "global"

                    if 'scenario' in meta:
                        result['scenario'] = SCENARIOS[meta['scenario']]
                        result['title'] = SCENARIOS[meta['scenario']]
                        result['order'] = 10 * MEMBERS.index(meta['scenario'])

                    if 'period' in meta:
                        result['period'] = meta['period']
                        result['period_ord'] = PERIODS.index(meta['period'])
                        result['period_name'] = get_trimester_names(result['period_ord'] + 1)
                        result['order'] += result['period_ord']

                    if 'year' in meta:
                        result['year'] = int(meta['year'])

                    if 'month' in meta:
                        result['month'] = int(meta['month'])

                    if meta['variable'] == 't':
                        temp.append(result)
                    else:
                        prec.append(result)

        self.data = dict(prec=[], temp=[])
        self.extra = {}

        for region, values in groupby(prec, group_key):
            data = list(values)
            max_date = concat_date(max(data, key=concat_date))
            self.data["prec"] += filter(lambda it: max_date == concat_date(it),
                                        data)

        for region, values in groupby(temp, group_key):
            data = list(values)
            max_date = concat_date(max(data, key=concat_date))
            self.data["temp"] += filter(lambda it: max_date == concat_date(it),
                                        data)


def concat_date(recd):
    return recd.get("year", 1000)*100 + recd.get("period_ord", 0) \
           + recd.get("month", 0)


def group_key(recd):
    return recd["region"]

