import os

import requests


def get_data_dir():
    pass


def create_data_dir(path):
    pass


def download(url, dest_path):
    pass


def get_data(data_home, url, dest_subdir, dest_filename, download_if_missing):
    pass


def clear_data_dir(path):
    """This function deletes the file.

        Args:
            path (str): File path.
        """
    if os.path.isfile(path):
        os.remove(path)