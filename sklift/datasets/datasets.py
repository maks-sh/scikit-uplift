import os
import shutil

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


def fetch_hillstorm(target='visit',
                    data_home=None,
                    dest_subdir=None,
                    download_if_missing=True):
   
    """Load the hillstorm dataset.
    
        Parameters
    ----------
    target : str, dafault=visit. 
        Can also be conversion, and spend
    data_home : str, default=None
        Specify another download and cache folder for the datasets.
    dest_subdir : str, default=None
    download_if_missing : bool, default=True
        If False, raise a IOError if the data is not locally available
        instead of trying to download the data from the source site.
        
        Returns
    ----------
        Dictionary-like object, with the following attributes.
        data : {ndarray, dataframe} of shape (64000, 12)
            The data matrix to learn. 
        target : {ndarray, series} of shape (64000,)
            The regression target for each sample. 
        treatment : {ndarray, series} of shape (64000,)
        
        """

    url = 'https://hillstorm1.s3.us-east-2.amazonaws.com/hillstorm_no_indices.csv.gz'
    csv_path = get_data(data_home=data_home,
                        url=url,
                        dest_subdir=dest_subdir,
                        dest_filename='hillstorm_no_indices.csv.gz',
                        download_if_missing=download_if_missing)
    hillstorm = pd.read_csv(csv_path)
    hillstorm_dict = {}
    hillstorm_dict['treatment'] = hillstorm.segment
    hillstorm_dict['target'] = hillstorm[target]
    hillstorm_data = hillstorm.drop(columns=['segment', target])
    hillstorm_dict['data'] = hillstorm_data
    return hillstorm_dict