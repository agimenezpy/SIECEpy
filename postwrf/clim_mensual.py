import cdms2
import numpy as np
from sys import argv
from six import print_


def clim_mensual(fname, vname="rainc"):
    dset = cdms2.open(fname)

    kw = {
        "level_%s" % vname: 10,
        "squeeze": True
    }
    vdat = dset[vname](**kw)
    months = vdat.shape[0]
    years = months / 12
    mdata = np.zeros((12, vdat.shape[1], vdat.shape[2]), dtype=np.float32)
    for cur in range(0, 12):
        for month in range(cur, months, 12):
            mdata[cur,:,:] += vdat[month,:,:]
        mdata[cur,:,:] /= years
    mdata.tofile("monthly_%s.dat" % vname)


if __name__ == '__main__':
    if len(argv) > 2:
        clim_mensual(argv[1], argv[2])
    else:
        print_("""
        Uso %s nombre_archivo.ctl variable
        """ % argv[0])