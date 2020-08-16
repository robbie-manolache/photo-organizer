
import os
import pandas as pd

def _gen_photo_df_(photo_dir):
    """
    """
    photo_dict = {"file_name": [], "dir_path": []}
    # may have to pass photo_dir as a list to iterate through
      # i.e. in case there are multiple locations
    for root, _, files in os.walk(photo_dir):
        for f in files:
            photo_dict["file_name"].append(f)
            photo_dict["dir_path"].append(root)
    photo_df = pd.DataFrame(photo_dict)
    # may have to handle edge cases for files without extensions
    photo_df.loc[:, "file_type"] = photo_df["file_name"].apply(
                                    lambda x: x.split(".")[-1].lower())
    return(photo_df)

def _gen_val_counts_(df_in, col):
    """
    """
    df = df_in.copy()[col].value_counts().to_frame().reset_index()
    df.columns = [col, "n_files"]
    return df

def _filter_df_(df_in, col, vals, mode):
    """
    """
    if mode == "keep":
        s = ""
    elif mode == "drop":
        s = " not"
    q = "%s%s in @vals"%(col, s)
    return df_in.copy().query(q)

class my_photo_gallery:
    """
    """

    def __init__(self, photo_dir):
        """
        """ 
        self.photo_df = _gen_photo_df_(photo_dir)
        self.set_uniq_attr()

    def set_uniq_attr(self):
        """
        """
        self.all_dirs = self.photo_df["dir_path"].unique().tolist()
        self.all_ext = self.photo_df["file_type"].unique().tolist()

    def dir_counts(self):
        """
        """
        return _gen_val_counts_(self.photo_df, "dir_path")

    def ext_counts(self):
        """
        """
        return _gen_val_counts_(self.photo_df, "file_type")

    def filter_by(self, col, vals, mode="keep"):
        """
        """
        df = _filter_df_(self.photo_df, col, vals, mode)
        self.photo_df = df
        self.set_uniq_attr()
        