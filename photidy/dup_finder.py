from photidy.my_photos import my_photo_gallery

class photo_dup_finder(my_photo_gallery):
    """
    """

    def __init__(self, photo_dir):
        """
        """
        my_photo_gallery.__init__(self, photo_dir)
        self.base_dir = None
        self.comp_dirs = None
        self.dup_methods = []
        self.delete_method = "careful"