import sys
import os
from os import path as pth
from sys import argv

import re
import Ngl
import Nio
import numpy as np
from six import print_
from wrf_common import (
    VARIABLES, DEFAULT_FILE_FORMAT, get_date, get_list_times,
    get_rain_data, get_temp_data, get_coordinates, regrid)


def cwrf_contour(fname, vname, days=None):

    if not pth.exists(fname):
        print_("You do not have the necessary '%s' file to run this script." % fname)
        sys.exit(1)

    dset = Nio.open_file(fname + ".nc")
    lat = dset.variables["XLAT"][0, :, :]
    lon = dset.variables["XLONG"][0, :, :]
    region, subm = re.split(os.sep, pth.dirname(fname))[-2:]

    cur_date = get_date(dset.START_DATE)
    dates = get_list_times(dset)
    if days is None:
        days = len(dates) / 10 * 10
    elif days in ('30', '60', '90'):
        days = int(days)
    else:
        print_("%s invalid, between 30, 60 and 90" % days)
        sys.exit(1)

    if vname == "RAINC":
        vdat, base = get_rain_data(dset, cur_date.month - 1, days)
        blon, blat = get_coordinates("rainc")
        title = "Precipitacion Total"
        unit = "mm"
        levels = (30, 1200, 150)
        blevels = [-300., -180.,  -90.,  -30.,   30.,   90.,  180.,  300.]
        palete = 'WhBlGrYeRe'
        bpalete = 'precip_diff_12lev'
    elif vname == "T2":
        vdat, base = get_temp_data(dset, cur_date.month - 1, days)
        blon, blat = get_coordinates("t2ave")
        title = "Temperatura Media a 2 m"
        unit = "~S~o~N~C"
        levels = (-5, 35, 5)
        blevels = [-3, -2, -1, -0.3, 0.3, 1, 2, 3]
        palete = 'MPL_coolwarm'
        bpalete = 'temp_diff_18lev'
    else:
        print_("%s not supported" % vname)
        sys.exit(1)

    rbase = regrid((blon, blat), (lon, lat), base)

    wks_type = "png"
    wks_res = Ngl.Resources()
    wks_res.wkHeight = 600
    wks_res.wkWidth = 650
    wks = Ngl.open_wks(wks_type,
                       DEFAULT_FILE_FORMAT % (cur_date.year, cur_date.month,
                                              days, VARIABLES[vname]), wks_res)

    panelres = Ngl.Resources()
    panelres.nglMaximize = True
    panelres.nglPanelBottom = 0.03

    res = Ngl.Resources()
    res.nglDraw = False
    res.nglFrame = False
    # Mapa
    set_map(res, (np.min(lon), np.min(lat)), (np.max(lon), np.max(lat)))
    #set_map(res, (REGIONS["SA"][0][0], REGIONS["SA"][0][1]),
    #             (REGIONS["SA"][1][0], REGIONS["SA"][1][1]))
    set_labelbar(res, unit)

    res.tiMainFontHeightF = 0.025
    res.tiMainString = "Totales"
    res.sfXArray = lon
    res.sfYArray = lat

    set_contour(res, levels, cnFillPalette=palete)
    plot1 = Ngl.contour_map(wks, vdat, res)
    #res.tmYLOn = False
    #res.tmYROn = True
    #res.tmYRLabelsOn = True
    res.tiMainString = "Anomalias"
    #res.sfXArray = blon
    #res.sfYArray = blat
    set_contour(res, blevels, cnFillPalette=bpalete)
    plot2 = Ngl.contour_map(wks, vdat - rbase, res)

    txres = Ngl.Resources()
    txres.txFontHeightF = 0.03
    Ngl.text_ndc(wks, title, 0.5, 0.97, txres)

    txres.txFontHeightF = 0.02
    last = days - 1
    if days > 89:
        last = days + 1
    Ngl.text_ndc(wks,
                 "Promedio %d dias desde %s hasta %s" %
                 (days, dates[0].strftime("%d%b%Y"),
                  dates[last].strftime("%d%b%Y")),
                 0.5, 0.91, txres)

    txres.txFontHeightF = 0.015
    y1 = 0.120
    y2 = 0.090
    if region == "PARAGUAY":
        y1 = 0.190
        y2 = 0.160
    Ngl.text_ndc(wks, "CWRF-CAM-%s OLE~S~2~N~ (clima.pol.una.py) " % subm,
                 0.8, y1, txres)
    txres.txFontHeightF = 0.013
    Ngl.text_ndc(wks, "Proyecto 14-INV-054 / GUYRA Paraguay / Facultad "
                      "Politecnica", 0.75, y2,
                 txres)

    Ngl.panel(wks, [plot1, plot2], [1, 2], panelres)
    Ngl.end()


def set_map(res, ll, tr):
    res.mpOutlineBoundarySets = "AllBoundaries"
    res.mpProjection = "Mercator"
    res.mpDataSetName = "Earth..4"
    res.mpDataBaseVersion = "MediumRes"
    res.mpLimitMode = "Corners"
    res.mpLeftCornerLatF = ll[1]
    res.mpLeftCornerLonF = ll[0]
    res.mpRightCornerLatF = tr[1]
    res.mpRightCornerLonF = tr[0]
    res.mpGridAndLimbOn = False
    return res


def set_labelbar(res, unit):
    res.lbTitleString = unit
    res.lbOrientation = "Horizontal"
    res.lbLabelFontHeightF = 0.015
    res.lbTitleFontHeightF = 0.02

    res.pmLabelBarOrthogonalPosF = -0.005
    res.pmLabelBarHeightF = 0.1
    res.pmLabelBarWidthF = 0.6
    return res


def set_contour(res, levels, **kwargs):
    # Contour
    res.cnFillOn = True
    res.cnLinesOn = False
    res.cnLineLabelsOn = False
    res.cnInfoLabelOn = False
    res.cnConstFLabelOn = False
    if len(levels) == 3:
        res.cnLevelSelectionMode = "ManualLevels"
        res.cnLevelSpacingF = levels[2]
        res.cnMinLevelValF = levels[0]
        res.cnMaxLevelValF = levels[1]
    elif len(levels) > 3:
        res.cnLevelSelectionMode = "ExplicitLevels"
        res.cnLevels = levels
    for k, v in kwargs.items():
        setattr(res, k, v)
    return res


if __name__ == '__main__':
    if len(argv) > 2:
        cwrf_contour(*argv[1:])
    else:
        print_("""
        Uso %s nombre_archivo.ctl variable
        """ % argv[0])