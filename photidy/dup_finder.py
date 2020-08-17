import numpy as np
import matplotlib.image as mpimg
from sklearn.decomposition import PCA
from photidy.my_photos import my_photo_gallery

def _make_photo_bw_(img):
    """
    """
    img = img.sum(axis = 2)
    img = img/img.max()
    return img

def _new_photo_dims_(shp, max_pix):
    """
    """
    if shp[1] > shp[0]:
        dim0 = max_pix
        dim1 = np.ceil((shp[0]/shp[1])*max_pix)
    else:
        dim1 = max_pix
        dim0 = np.ceil((shp[1]/shp[0])*max_pix)
    return int(dim0), int(dim1)

def _compress_photo_(p, max_pix=50, keep_pca=False):
    """
    """
    img = mpimg.imread(p)
    if len(img.shape) == 3:
        img = _make_photo_bw_(img)   
    # set PCA transform dimensions
    dim0, dim1 = _new_photo_dims_(img.shape, max_pix)
    pca0 = PCA(dim0, random_state=42)
    pca1 = PCA(dim1, random_state=42)
    # apply PCA to both dimesions
    img = pca0.fit_transform(img)
    img = pca1.fit_transform(img.transpose())
    # return compressed object
    if keep_pca:
        return img, pca0.components_, pca1.components_
    else:
        return img

class photo_dup_finder(my_photo_gallery):
    """
    """

    def __init__(self, photo_dir):
        """
        """
        my_photo_gallery.__init__(self, photo_dir)
        self.base_dir = None
        self.base_df = None
        self.comp_dirs = None
        self.comp_df = None
        self.dup_methods = []
        self.delete_method = "careful"

    def set_base_dir(self, dir_path):
        """
        """
        self.base_dir = dir_path
        q = "dir_path == @dir_path"
        self.base_df = self.photo_df.copy().query(q)

    def set_comp_dirs(self, dir_list):
        """
        """
        self.comp_dirs = dir_list
        q = "dir_path in @dir_list"
        self.comp_df = self.photo_df.copy().query(q)
