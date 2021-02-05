import os
import shutil
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


def fetch_criteo(return_X_y_t=False, data_home=None, dest_subdir=None, download_if_missing=True,
                 percent10=True, treatment_feature='treatment', target_column='visit', as_frame=False):
    """Load data from the Criteo dataset
    Args:
        return_X_y_t (bool): If True, returns (data, target, treatment) instead of a Bunch object.
                See below for more information about the data and target object.
        data_home (str): Specify a download and cache folder for the datasets.
        dest_subdir (str, unicode): The name of the folder in which the dataset is stored.
        download_if_missing (bool, default=True): If False, raise an IOError if the data is not locally available
                                                  instead of trying to download the data from the source site.
        percent10 (bool, default=True): Whether to load only 10 percent of the data.
        treatment_feature (str, default='treatment'): {'treatment', 'exposure'} Selects which column from dataset
                                                      will be treatment
        target_column (str, default='visit'): {'visit', 'conversion'} Selects which column from dataset will be target
        as_frame (bool, default=False):
    Returns:
        '~sklearn.utils.Bunch': dataset
            Dictionary-like object, with the following attributes.
                data (DataFrame object): Dataset without target and treatment.
                target (DataFrame object): Column target by values
                treatment (DataFrame object): Column treatment by values
                DESCR (str): Description of the Criteo dataset.
        tuple (data, target, treatment): tuple if return_X_y_t is True
    """
    if percent10:
        url = 'https://criteo-bucket.s3.eu-central-1.amazonaws.com/criteo10.csv.gz'
        csv_path = get_data(data_home=data_home, url=url, dest_subdir=dest_subdir,
                            dest_filename='criteo10.csv.gz',
                            download_if_missing=download_if_missing)
    else:
        url = "https://criteo-bucket.s3.eu-central-1.amazonaws.com/criteo.csv.gz"
        csv_path = get_data(data_home=data_home, url=url, dest_subdir=dest_subdir,
                        dest_filename='criteo.csv.gz',
                        download_if_missing=download_if_missing)

    if treatment_feature == 'exposure':
        data = pd.read_csv(csv_path, usecols=[i for i in range(12)])
        treatment = pd.read_csv(csv_path,  usecols=['exposure'], dtype={'exposure': 'Int8'})
        if as_frame:
            treatment = treatment['exposure']
    elif treatment_feature == 'treatment':
        data = pd.read_csv(csv_path, usecols=[i for i in range(12)])
        treatment = pd.read_csv(csv_path,  usecols=['treatment'], dtype={'treatment': 'Int8'})
        if as_frame:
            treatment = treatment['treatment']
    else:
        raise ValueError("Treatment_feature value must be from %s, got"
                         " %s." % (['treatment', 'exposure'], treatment_feature))

    if target_column == 'conversion':
        target = pd.read_csv(csv_path,  usecols=['conversion'], dtype={'conversion': 'Int8'})
        if as_frame:
            target = target['conversion']
    elif target_column == 'visit':
        target = pd.read_csv(csv_path,  usecols=['visit'], dtype={'visit': 'Int8'})
        if as_frame:
            target = target['visit']
    else:
        raise ValueError("Target_column value must be from %s, got"
                         " %s." % (['visit', 'conversion'], target_column))

    if return_X_y_t:
        if as_frame:
            return data, target, treatment
        else:
            return data.to_numpy(), target.to_numpy(), treatment.to_numpy()
    else:
        module_path = os.path.dirname(__file__)
        with open(os.path.join(module_path, 'descr', 'criteo.rst')) as rst_file:
            fdescr = rst_file.read()
        if as_frame:
            return Bunch(data=data, target=target, treatment=treatment, DESCR=fdescr)
        else:
            return Bunch(data=data.to_numpy(), target=target.to_numpy(), treatment=treatment.to_numpy(), DESCR=fdescr)
