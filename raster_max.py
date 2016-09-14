################################################################################
# Script:  raster_max.py
# Author:  Scott Hatcher
# Date:    2016-09-13
# Purpose: This script takes as input any raster format that can be read by GDAL, 
#              and reports the index/indices of the max pixel value for all bands
#              in that raster.
################################################################################

from osgeo import gdal
import numpy as np
import sys

# Let's GDAL throw Python exceptions
gdal.UseExceptions()

def Usage():
    print("""
    Usage:
    $ python raster_max.py input-raster-path
    e.g. python raster_max.py /home/user/test.tif
    """)
    sys.exit(1)

def main( filepath ):
    try:
        src_ds = gdal.Open( filepath )
    except RuntimeError, e:
        print 'Unable to open ' + filepath
        print e
        sys.exit(1)
    
    print "[Raster band count]: ", src_ds.RasterCount
    try:
        for band in range( src_ds.RasterCount ):
            band += 1
            print "[Working on band]: ", band
            src_band = src_ds.GetRasterBand(band)
            if src_band is None:
                continue
    
            src_array = src_band.ReadAsArray().astype(np.float) # Assumed 32-bit float, which may slow it down in some cases
            (y_inds, x_inds) = np.nonzero(src_array == np.max(src_array))
    
            print "[Indices of max value for band " + str(band) + " (format: '[(x1,y1),(x2,y2),...]']:\n" + repr(zip(x_inds, y_inds))
    except RuntimeError, e:
        print 'Failed processing on raster'
        print e
        sys.exit(1)

if __name__ == '__main__':

    if len( sys.argv ) > 2:
        print """
        [ ERROR ] the script can only accept a single input raster
        """
        Usage()

    main( str(sys.argv[1]) )
