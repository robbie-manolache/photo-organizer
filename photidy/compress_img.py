import numpy as np
import matplotlib.image as mpimg
from sklearn.decomposition import PCA

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
        
def pca_compress_photo(p, max_pix=50, keep_pca=False,
                       always_portrait=True):
    """
    Compresses photo using the PCA method.
    """

    # load the image and convert to black-and-white
    img = mpimg.imread(p)
    if len(img.shape) == 3:
        img = _make_photo_bw_(img)   

    # set PCA transform dimensions
    shp = img.shape
    dim0, dim1 = _new_photo_dims_(shp, max_pix)
    pca0 = PCA(dim0, random_state=42)
    pca1 = PCA(dim1, random_state=42)

    # transpose landscape images
    if shp[1] > shp[0]:
        img = img.transpose()
        pca0, pca1 = pca1, pca0

    # apply PCA to both dimesions
    img = pca0.fit_transform(img)
    img = pca1.fit_transform(img.transpose())
    
    # re-transpose landscape photos if portrait not desired
    if always_portrait:
        pass
    elif shp[1] > shp[0]:
        img = img.transpose()
        pca0, pca1 = pca1, pca0

    # return compressed object
    if keep_pca:
        return img, pca0.components_, pca1.components_
    else:
        return img
    
def recon_from_pca(img, pca0, pca1):
    """
    Reconstitutes a compressed photo from its PCA components
    """
    return np.matmul(np.matmul(img, pca1).transpose(), pca0)        

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
   