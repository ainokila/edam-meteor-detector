import sys
import numpy as np
import io
try:
    from astropy.io import fits
except ImportError:
    import pyfits as fits

def fits_to_jpg(fitsfilename, vmin=0, vmax=1.5e6):

    # Try to read data from first HDU in fits file
    data = fits.open(fitsfilename)[0].data
    # If nothing is there try the second one
    if data is None:
        data = fits.open(fitsfilename)[1].data

    # Clip data to brightness limits
    data[data > vmax] = vmax
    data[data < vmin] = vmin
    # Scale data to range [0, 1] 
    data = (data - vmin)/(vmax - vmin)
    # Convert to 8-bit integer  
    data = (255*data).astype(np.uint8)
    # Invert y axis
    data = data[::-1, :]

    return data

def image_to_byte_array(image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr