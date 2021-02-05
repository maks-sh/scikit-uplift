import os
import shutil
from os.path import dirname, join
import pandas as pd
import requests
from sklearn.utils import Bunch


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
            for chunk in req.iter_content(chunk_size=2 ** 20):
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


def fetch_x5(data_home=None, dest_subdir=None, download_if_missing=True):
    """Fetch the X5 dataset.

        Args:
            data_home (str, unicode): The path to the folder where datasets are stored.
            dest_subdir (str, unicode): The name of the folder in which the dataset is stored.
            download_if_missing (bool): Download the data if not present. Raises an IOError if False and data is missing.

        Returns:
            '~sklearn.utils.Bunch': dataset
                Dictionary-like object, with the following attributes.
                data ('~sklearn.utils.Bunch'): Dataset without target and treatment.
                target (Series object): Column target by values
                treatment (Series object): Column treatment by values
                DESCR (str): Description of the X5 dataset.
                train (DataFrame object): Dataset with target and treatment.
    """
    url_clients = 'https://timds.s3.eu-central-1.amazonaws.com/clients.csv.gz'
    file_clients = 'clients.csv.gz'
    csv_clients_path = get_data(data_home=data_home, url=url_clients, dest_subdir=dest_subdir,
                                dest_filename=file_clients,
                                download_if_missing=download_if_missing)
    clients = pd.read_csv(csv_clients_path)

    url_train = 'https://timds.s3.eu-central-1.amazonaws.com/uplift_train.csv.gz'
    file_train = 'uplift_train.csv.gz'
    csv_train_path = get_data(data_home=data_home, url=url_train, dest_subdir=dest_subdir,
                              dest_filename=file_train,
                              download_if_missing=download_if_missing)
    train = pd.read_csv(csv_train_path)

    url_purchases = 'https://timds.s3.eu-central-1.amazonaws.com/purchases.csv.gz'
    file_purchases = 'purchases.csv.gz'
    csv_purchases_path = get_data(data_home=data_home, url=url_purchases, dest_subdir=dest_subdir,
                                dest_filename=file_purchases,
                                download_if_missing=download_if_missing)
    purchases = pd.read_csv(csv_purchases_path)

    target = train['target']
    treatment = train['treatment_flg']

    module_path = dirname(__file__)
    with open(join(module_path, 'descr', 'x5.rst')) as rst_file:
        fdescr = rst_file.read()

    return Bunch(data=Bunch(clients=clients, train=train, purchases=purchases), target=target, treatment=treatment, DESCR=fdescr)
