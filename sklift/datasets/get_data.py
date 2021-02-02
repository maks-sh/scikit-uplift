import os

import requests


def get_data_dir():
    pass


def create_data_dir(path):
    pass


def download(url, dest_path):
    pass


def get_data(data_home, url, dest_subdir, dest_filename, download_if_missing):
    """Return the path to the dataset.
    
    Args:
        data_home (str, unicode): The path to the folder where datasets are stored.
        url (str or unicode): The URL to the dataset.
        dest_subdir (str or unicode): The path to the folder where dataset are stored.
        dest_filename (str): The name of the dataset.
        download_if_missing (bool): Flag if dataset is missing.

    Returns:
        The path to the dataset.
        
    """
    if data_home is None:
        data_dir = os.path.join(get_data_dir(),dest_subdir)
    else:
        data_dir = os.path.join(os.path.abspath(data_home),dest_subdir)

    create_data_dir(data_dir)

    dest_path = os.path.join(data_dir,dest_filename)

    if not os.path.isfile(dest_path):
        if download_if_missing:
            download(url, dest_path)
        else:
            raise IOError("Dataset missing")
    return dest_path

def clear_data_dir(path):
    pass