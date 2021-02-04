import os
import pandas as pd
import requests
from sklearn.utils import Bunch

def get_data_dir():
    return os.path.join(os.path.expanduser("~"), "lightfm_data")


def create_data_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def download(url, dest_path):
    req = requests.get(url, stream=True)
    req.raise_for_status()

    with open(dest_path, "wb") as fd:
        for chunk in req.iter_content(chunk_size=2 ** 20):
            fd.write(chunk)


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

def clear_data_dir(path):
    pass 

def fetch_lenta(return_X_y_t=False, data_home=None, dest_subdir=None, download_if_missing=True):
    '''Fetch the Lenta dataset.

        Args:
            return_X_y (bool): If True, returns (data, target) instead of a Bunch object. 
                See below for more information about the data and target object.
            data_home (str, unicode): The path to the folder where datasets are stored.
            dest_subdir (str, unicode): The name of the folder in which the dataset is stored.
            download_if_missing (bool): Download the data if not present. Raises an IOError if False and data is missing.

        Returns:
        '~sklearn.utils.Bunch': dataset
            Dictionary-like object, with the following attributes.

            data (DataFrame object): Dataset without target and treatment.
            target (Series object): Column target by values
            treatment (Series object): Column treatment by values
            DESCR (str): Description of the Lenta dataset.

        (data,target,treatment): tuple if 'return_X_y_t' is True
    '''
    url='https:/winterschool123.s3.eu-north-1.amazonaws.com/lentadataset.csv.gz'
    filename='lentadataset.csv.gz'
    csv_path=get_data(data_home=data_home, url=url, dest_subdir=dest_subdir, dest_filename=filename, download_if_missing=download_if_missing)
    data = pd.read_csv(csv_path)
    target=data['response_att']
    treatment=data['group']
    data=data.drop(['response_att','group'], axis=1)
    module_path = os.path.dirname(__file__)
    with open(os.path.join(module_path, 'descr', 'lenta.rst')) as rst_file:
        fdescr = rst_file.read()
    if return_X_y_t == True:
        return data,target,treatment
    return Bunch(data=data, target=target, treatment=treatment, DESCR=fdescr)
