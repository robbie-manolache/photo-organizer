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
    dim0 = max_pix
    if shp[1] > shp[0]:
        dim1 = np.ceil((shp[0]/shp[1])*max_pix)
    else:
        dim1 = np.ceil((shp[1]/shp[0])*max_pix)
    return int(dim0), int(dim1)

def compress_photo(p, max_pix=50, keep_pca=False):
    """
    Compresses photo using the PCA method.
    TO DO: add convolutional approach!
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

    # transpose portrait images
    if shp[0] > shp[1]:
        img = img.transpose()

    # apply PCA to both dimesions
    img = pca0.fit_transform(img)
    img = pca1.fit_transform(img.transpose())

    # re-transpose portrait images (may not be ideal!)
    if shp[0] > shp[1]:
        img = img.transpose()

    # return compressed object
    if keep_pca:
        return img, pca0.components_, pca1.components_
    else:
        return img