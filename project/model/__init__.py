# -*- coding: utf-8 -*-
PERIODS = ("EFM", "FMA", "MAM",
           "AMJ", "MJJ", "JJA", "JAS",
           "ASO", "SON", "OND", "NDE",
           "DEF")

MEMBERS = ("M1", "M2", "M3", "M4")

REGIONS = {
    "PARAGUAY": "Paraguay",
    "PY": "Paraguay",
    "SA": "Sudamérica"
}

SCENARIOS = {
    "M1": "Miembro 1",
    "M2": "Miembro 2",
    "M3": "Miembro 3",
    "M4": "Miembro 4"
}

VARIABLES = {
    "p": "Precipitación",
    "t": "Temperatura"
}

MATCHES = {
    "WRF3.4": "WRF3.4/(?P<region>\w+)-.*-(?P<variable>\w)\.gif",
    "CWRF3.4": "CWRF3.4/(?P<region>\w+)/(?P<scenario>\w+)/(?P<year>\d{4})-"
               "(?P<month>\d{2})\+90_(?P<variable>\w)\.png",
    "CAM": "CAM/(?P<scenario>\w+)/(?P<period>\w{3}).*(?P<variable>\w?)_"
           "(?P<year>\d+)\.png"
}

CLIMATE_MODELS = {
    "tiempo": "WRF3.4",
    "clima": "CWRF3.4",
    "atmos": "CAM"
}
