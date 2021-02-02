import os
import shutil

import requests


def get_data_dir():
    pass


def create_data_dir(path):
    pass


def download(url, dest_path):
    pass


def get_data(data_home, url, dest_subdir, dest_filename, download_if_missing):
    pass


def clear_data_dir(path=None):
    """This function deletes the file.

        Args:
            path (str): File path. By default, this is the default path for datasets.
        """
    if path is None:
        path = get_data_dir()
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)
