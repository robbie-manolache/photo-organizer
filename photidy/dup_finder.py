import os
import pandas as pd
from photidy.my_photos import my_photo_gallery
from photidy.compress_photo import compress_photo

def _compress_batch_(df):
    """
    """
    # initiate loop variables
    index, values = [], []
    n, i = df.shape[0], 0

    # execute loop
    for idx, r in df.iterrows():
        # apply compression
        index.append(idx)
        values.append(compress_photo(os.path.join(r[1], r[0])))
        # print progress
        i += 1
        pct = round(100*i/n)
        p = round(pct/2)
        s = "="*p + "."*(50-p)
        print("\r|%s| %d%% |"%(s, pct), end="")

    # insert loop values into df
    df.loc[:, "pca_feat"] = pd.Series(values, index=index)
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
