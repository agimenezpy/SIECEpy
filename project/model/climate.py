from os import walk, path, listdir
from re import match
from . import (REGIONS, SCENARIOS, VARIABLES, MATCHES, PERIODS, MEMBERS)
from project.utils.dates import get_trimester_names


def file_list(directory):
    matches = []
    for root, dirnames, filenames in walk(directory):
        matches.extend([path.join(root, filename) for filename in filenames])
    return matches


class ClimateModel(object):

    def __init__(self, model, directory):
        prec = []
        temp = []
        period = -1

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
                        result['region_name'] = REGIONS[meta['region']]
                    if 'scenario' in meta:
                        result['scenario'] = SCENARIOS[meta['scenario']]
                        result['title'] = SCENARIOS[meta['scenario']]
                    if 'period' in meta:
                        ord_period = PERIODS.index(meta['period'])
                        result['period'] = meta['period']
                        result['period_name'] = get_trimester_names(
                            ord_period + 1)
                        result['order'] = 10*MEMBERS.index(meta['scenario']) + \
                                          ord_period
                        if ord_period > period:
                            period = ord_period

                    if meta['variable'] == 't':
                        temp.append(result)
                    else:
                        prec.append(result)

        self.data = dict(prec=prec, temp=temp)
        self.period = PERIODS[period] if period > 0 else None
