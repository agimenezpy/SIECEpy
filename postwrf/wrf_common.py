import Ngl, Nio
import numpy as np
from datetime import datetime, timedelta
import calendar
import locale
import cdms2
import pyresample

CLIMATOLOGY = "/STORAGE/climatology/monthly_%s.ctl"

REGIONS = {
    "SA": (
        (-90, -56),
        (-32, 20)
    ),
    "PY": (
        (-67, -33),
        (-49, -16)
    )
}

DEFAULT_FILE_FORMAT = "%04d-%02d+%02d_%s"

VARIABLES = {
    "T2": "t",
    "RAINC": "p"
}

DATE_FORMAT = "%Y-%m-%d_%H:%M:%S"


def add_shapefile_outlines(wks, plot, filename):
    #---Read data off shapefile
    f = Nio.open_file(filename, "r")
    lon = np.ravel(f.variables["x"][:])
    lat = np.ravel(f.variables["y"][:])

    plres = Ngl.Resources()      # resources for polylines
    plres.gsLineColor = "navyblue"
    plres.gsLineThicknessF = 2.0           # default is 1.0
    plres.gsSegments = f.variables["segments"][:,0]

    return Ngl.add_polyline(wks, plot, lon, lat, plres)


def set_map_options(res, lats, lons):
    # Map options
    res.mpDataBaseVersion = "MediumRes"                # better map outlines
    res.mpOutlineBoundarySets = "GeophysicalAndUSStates"   # more outlines

    res.mpLimitMode = "LatLon"
    res.mpMinLatF = np.min(lats)-1
    res.mpMaxLatF = np.max(lats)+1
    res.mpMinLonF = np.min(lons)-1
    res.mpMaxLonF = np.max(lons)+1
    res.mpGridAndLimbOn = False


def get_date(sdate):
    return datetime.strptime(sdate, DATE_FORMAT)


def get_trimester(sdate=None):
    if sdate is None:
        a_date = datetime.now()
    else:
        a_date = datetime.strptime(sdate, DATE_FORMAT)
    month = a_date.month

    trim = ""
    for m in range(month, month + 3):
        trim += calendar.month_abbr[(m % 12)].upper()[0]
    return trim


def get_trimester_names(month=-1):
    locale.setlocale(locale.LC_ALL, 'es_PY.UTF-8')
    if 0 < month < 13:
        month -= 1
    else:
        month = datetime.now().month - 1

    trim = ", ".join([
        calendar.month_name[(month % 12) + 1].title(),
        calendar.month_name[((month + 1) % 12) + 1].title(),
        calendar.month_name[((month + 2) % 12) + 1].title(),
    ])
    return trim


def get_list_times(data_set):
    if "XTIME" in data_set.variables:
        result = []
        cur_date = get_date(data_set.START_DATE)
        for value in data_set.variables['XTIME']:
            result.append(
                cur_date + timedelta(minutes=int(value))
            )
        return result
    else:
        return []


def get_rain_data(dset, month, days):
    last = days - 1
    if days > 89:
        last = days + 1
    tot = dset.variables["RAINNC"][:last, :, :] + \
          dset.variables["RAINC"][:last, :, :]
    vdat = tot[-1, :, :] - tot[0, :, :]

    dset1 = cdms2.open(CLIMATOLOGY % "rainc")
    dset2 = cdms2.open(CLIMATOLOGY % "rainnc")

    shape = dset1['rainc'].shape
    month_count = days/30
    tot = np.zeros((month_count, shape[1], shape[2]), np.float)
    for i in range(0, month_count):
        tot[i] = dset1['rainc'][(month + i) % 12, :, :]*30 + dset2['rainnc'][(month + i) % 12, :, :]*30
    #vrainc /= month_count
    #vrainnc /= month_count

    #base = vrainc + vrainnc
    base = np.mean(tot, axis=0)# - tot[0, :, :]

    return vdat, np.ma.masked_less(base, 0)


def get_temp_data(dset, month, days):
    last = days - 1
    if days > 89:
        last = days + 1
    vdat = np.average(dset.variables["T2"][:last, :, :] - 273.15, axis=0)

    dset1 = cdms2.open(CLIMATOLOGY % "t2ave")

    shape = dset1['t2ave'].shape
    vt2 = np.zeros((shape[1], shape[2]), np.float)
    month_count = days / 30
    for i in range(0, month_count):
        vt2 += dset1['t2ave'][(month + i) % 12, :, :] - 273.5
    vt2 /= month_count

    return vdat, np.ma.masked_less(vt2, -11)


def get_coordinates(vname):
    dset1 = cdms2.open(CLIMATOLOGY % vname)

    return dset1[vname].getLongitude()[:], dset1[vname].getLatitude()[:]


def regrid(s_coord, d_coord, data):
    lon2d, lat2d = np.meshgrid(s_coord[0], s_coord[1])

    orig_def = pyresample.geometry.SwathDefinition(lons=lon2d, lats=lat2d)

    targ_def = pyresample.geometry.SwathDefinition(lons=d_coord[0],
                                                   lats=d_coord[1])
    return pyresample.kd_tree.resample_nearest(orig_def, data, targ_def,
                                               radius_of_influence=500000,
                                               fill_value=None)