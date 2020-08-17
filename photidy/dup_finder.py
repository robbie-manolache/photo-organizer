from photidy.my_photos import my_photo_gallery

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
