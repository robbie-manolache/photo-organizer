import os
import pandas as pd
from photidy.my_photos import my_photo_gallery
from photidy.compress_img import pca_compress_photo, \
    conv_compress_photo

def _compress_batch_(df, method="conv", max_pix=100, 
                     verbose=False):
    """
    TO DO: set up **kwargs 
    """
    # initiate loop variables
    index, values = [], []
    n, i = df.shape[0], 0

    # execute loop
    for idx, r in df.iterrows():
        
        # apply compression
        index.append(idx)
        if method == "conv":
            v = conv_compress_photo(os.path.join(r[1], r[0]),
                                    max_pix=max_pix)
        elif method == "pca":
            v = pca_compress_photo(os.path.join(r[1], r[0]),
                                   max_pix=max_pix)
        else:
            print("Method not recognised!")
            return
        values.append(v)
        
        # print progress
        if verbose:
            i += 1
            pct = round(100*i/n)
            p = round(pct/2)
            s = "="*p + "."*(50-p)
            print("\r|%s| %d%% |"%(s, pct), end="")
        else:
            pass

    # insert loop values into df
    df.loc[:, "compr_img"] = pd.Series(values, index=index)
    return df

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
