import numpy as np
import matplotlib.image as mpimg
from sklearn.decomposition import PCA
from photidy.compress import _make_photo_bw_, _new_photo_dims_

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
    