import numpy as np
import matplotlib.image as mpimg
from photidy.compress import _make_photo_bw_, _new_photo_dims_

def _gen_break_points_(n0, num_seg, overlap = 0):
    """
    Generates the break point indices to split a 1-d array of size n0 into 
    equispaced (and overlapping) segments of equal length.
    """
      
    # gauge approximate difference
    dif = np.ceil(n0 / num_seg).astype(int)
    
    # starting break points for each axis segment
    a0 = np.round(np.linspace(0, n0 - dif - overlap, 
                              num_seg)).astype(int)
    
    # return complete set of start-end break points for each axis segment
    return list(zip(a0[:-1], a0[:-1] + dif + overlap)) + \
        [(n0 - dif - overlap, n0)]

def conv_compress_photo(p, max_pix=50, conv_overlap=0):
    """
    """
    
    # load the image and convert to black-and-white
    img = mpimg.imread(p)
    if len(img.shape) == 3:
        img = _make_photo_bw_(img)   

    # set compressed image dimensions
    shp = img.shape
    dim0, dim1 = _new_photo_dims_(shp, max_pix) 
    
    # get break points for convolution segments
    x = _gen_break_points_(shp[0], dim0, conv_overlap)
    y = _gen_break_points_(shp[1], dim1, conv_overlap)
    
    # combine break points and segment image
    xy = [img[ix[0]:ix[1], iy[0]:iy[1]] for ix in x for iy in y]
    xy = np.array(xy).reshape(len(x), len(y), 
                              xy[0].shape[0], xy[1].shape[1])
    
    # take the mean of each segment
    return xy.mean(axis=(2,3))
    