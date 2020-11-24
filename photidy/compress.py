import numpy as np

def _make_photo_bw_(img):
    """
    """
    img = img.sum(axis = 2)
    img = img/img.max()
    return img

def _new_photo_dims_(shp, max_pix):
    """
    Sets dimensions of compressed photo version.
    """
    if shp[1] > shp[0]:
        dim0 = np.ceil((shp[0]/shp[1])*max_pix)
        dim1 = max_pix
    else:
        dim0 = max_pix
        dim1 = np.ceil((shp[1]/shp[0])*max_pix)
    return int(dim0), int(dim1)