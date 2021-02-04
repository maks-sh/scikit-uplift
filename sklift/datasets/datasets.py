import os
import shutil

import pandas as pd
import requests


def get_data_dir():
    """This function returns a directory, which stores the datasets.

    Returns:
        Full path to a directory, which stores the datasets.

    """
    return os.path.join(os.path.expanduser("~"), "scikit-uplift-data")


def create_data_dir(path):
    """This function creates a directory, which stores the datasets.

    Args:
        path (str): The path to the folder where datasets are stored.

    """
    if not os.path.isdir(path):
        os.makedirs(path)


def download(url, dest_path):
    '''Download the file from url and save it localy
    
    Args:
        url: URL address, must be a string.
        dest_path: Destination of the file.

    Returns:
        TypeError if URL is not a string.
    '''
    if isinstance(url, str):
        req = requests.get(url, stream=True)
        req.raise_for_status()

        with open(dest_path, "wb") as fd:
            for chunk in req.iter_content(chunk_size=2**20):
                fd.write(chunk)
    else:
        raise TypeError("URL must be a string")


def get_data(data_home, url, dest_subdir, dest_filename, download_if_missing):
    """Return the path to the dataset.
    
    Args:
        data_home (str, unicode): The path to the folder where datasets are stored.
        url (str or unicode): The URL to the dataset.
        dest_subdir (str or unicode): The name of the folder in which the dataset is stored.
        dest_filename (str): The name of the dataset.
        download_if_missing (bool): Flag if dataset is missing.

    Returns:
        The path to the dataset.
        
    """
    if data_home is None:
        if dest_subdir is None:
            data_dir = get_data_dir()
        else:
            data_dir = os.path.join(get_data_dir(), dest_subdir)
    else:
        if dest_subdir is None:
            data_dir = os.path.abspath(data_home)
        else:
            data_dir = os.path.join(os.path.abspath(data_home), dest_subdir)

    create_data_dir(data_dir)

    dest_path = os.path.join(data_dir, dest_filename)

    if not os.path.isfile(dest_path):
        if download_if_missing:
            download(url, dest_path)
        else:
            raise IOError("Dataset missing")
    return dest_path


def clear_data_dir(path=None):
    """This function deletes the file.

        Args:
            path (str): File path. By default, this is the default path for datasets.
        """
    if path is None:
        path = get_data_dir()
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)


def fetch_criteo(data_home=None, download_if_missing=True, interaction_feature='treatment', target='visit', as_frame=True):
    """
    TODO: Add description
    Args:
        data_home (str):
        download_if_missing (bool, default=True):
        interaction_feature (str, default='treatment'): {'treatment', 'exposure'}
        target (str, default='visit'): {'visit', 'conversion'}
        as_frame (bool, default=True):
    Returns:
        (data, target): tuple
    """
    url = "https://criteo-bucket.s3.eu-central-1.amazonaws.com/criteo.csv.gz"
    csv_path = get_data(data_home=data_home, url=url, dest_subdir=None,
                        dest_filename='criteo.csv.gz',
                        download_if_missing=download_if_missing)
    criteo_df = pd.read_csv(csv_path, compression='gzip')

    if interaction_feature == 'exposure':
        X_data = criteo_df.drop(columns=['treatment', 'conversion', 'visit'])
    else:
        X_data = criteo_df.drop(columns=['conversion', 'visit', 'exposure'])

    if target == 'conversion':
        y_data = criteo_df[['conversion']]
    else:
        y_data = criteo_df[['visit']]

    if as_frame:
        return X_data, y_data
    else:
        return X_data.to_numpy(), y_data.to_numpy()
    # TODO: Memory optimization
