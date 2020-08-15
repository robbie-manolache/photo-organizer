
import os
import pandas as pd

def _gen_photo_df_(photo_dir):
    """
    """
    photo_dict = {"file_name": [], "dir_path": []}
    for root, _, files in os.walk(photo_dir):
        for f in files:
            photo_dict["file_name"].append(f)
            photo_dict["dir_path"].append(root)
    photo_df = pd.DataFrame(photo_dict)
    # may have to handle edge cases for files without extensions
    photo_df.loc[:, "file_type"] = photo_df["file_name"].apply(
                                    lambda x: x.split(".")[-1].lower())
    return(photo_df)
    
class my_photos:
    """
    """

    def __init__(self, photo_dir):
        """
        """ 
        self.photo_df = _gen_photo_df_(photo_dir)
        