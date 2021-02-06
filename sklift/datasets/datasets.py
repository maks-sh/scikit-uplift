import shutil
import os
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


def fetch_lenta(return_X_y_t=False, data_home=None, dest_subdir=None, download_if_missing=True):
    '''Fetch the Lenta dataset.

        Args:
            return_X_y_t (bool): If True, returns (data, target, treatment) instead of a Bunch object. 
                See below for more information about the data and target object.
            data_home (str, unicode): The path to the folder where datasets are stored.
            dest_subdir (str, unicode): The name of the folder in which the dataset is stored.
            download_if_missing (bool): Download the data if not present. Raises an IOError if False and data is missing.

        Returns:
            * dataset ('~sklearn.utils.Bunch'): Dictionary-like object, with the following attributes.
                * data (DataFrame object): Dataset without target and treatment.
                * target (Series object): Column target by values.
                * treatment (Series object): Column treatment by values.
                * DESCR (str): Description of the Lenta dataset.

            * (data,target,treatment): tuple if 'return_X_y_t' is True.
    '''
    url='https:/winterschool123.s3.eu-north-1.amazonaws.com/lentadataset.csv.gz'
    filename='lentadataset.csv.gz'
    csv_path=get_data(data_home=data_home, url=url, dest_subdir=dest_subdir,
             dest_filename=filename,
            download_if_missing=download_if_missing)
    data = pd.read_csv(csv_path)
    target=data['response_att']
    treatment=data['group']
    data=data.drop(['response_att', 'group'], axis=1)

    module_path = os.path.dirname(__file__)
    with open(os.path.join(module_path, 'descr', 'lenta.rst')) as rst_file:
        fdescr = rst_file.read()
    
    if return_X_y_t == True:
        return data, target, treatment
    
    return Bunch(data=data, target=target, treatment=treatment, DESCR=fdescr)


def fetch_x5(data_home=None, dest_subdir=None, download_if_missing=True):
    """Fetch the X5 dataset.

        Args:
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

    module_path = os.path.dirname(__file__)
    with open(os.path.join(module_path, 'descr', 'x5.rst')) as rst_file:
        fdescr = rst_file.read()

    return Bunch(data=Bunch(clients=clients, train=train, purchases=purchases), 
                 target=target, treatment=treatment, DESCR=fdescr)


def fetch_criteo(data_home=None, dest_subdir=None, download_if_missing=True, percent10=True,
                 treatment_feature='treatment', target_column='visit', return_X_y_t=False,  as_frame=False):
    """Load data from the Criteo dataset
    
    Args:
        data_home (string): Specify a download and cache folder for the datasets.
        dest_subdir (string, unicode): The name of the folder in which the dataset is stored.
        download_if_missing (bool, default=True): If False, raise an IOError if the data is not locally available
                                                  instead of trying to download the data from the source site.
        percent10 (bool, default=True): Whether to load only 10 percent of the data.
        treatment_feature (string,'treatment' or 'exposure' default='treatment'): Selects which column from dataset
                                                                                  will be treatment
        target_column (string, 'visit' or 'conversion', default='visit'): Selects which column from dataset
                                                                          will be target
        return_X_y_t (bool, default=False): If True, returns (data, target, treatment) instead of a Bunch object.
                See below for more information about the data and target object.
        as_frame (bool, default=False):
    Returns:
        ''~sklearn.utils.Bunch'': dataset
            Dictionary-like object, with the following attributes.
                data (ndarray, DataFrame object): Dataset without target and treatment.
                target (ndarray, series): Column target by values
                treatment (ndarray, series): Column treatment by values
                DESCR (string): Description of the Criteo dataset.
                feature_names (list): The names of the future columns
                target_name (string): The name of the target column.
                treatment_name (string): The name of the treatment column
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
        raise ValueError(f"Treatment_feature value must be from {['treatment', 'exposure']}. "
                         f"Got value {treatment_feature}.")
    feature_names = list(data.columns)

    if target_column == 'conversion':
        target = pd.read_csv(csv_path,  usecols=['conversion'], dtype={'conversion': 'Int8'})
        if as_frame:
            target = target['conversion']
    elif target_column == 'visit':
        target = pd.read_csv(csv_path,  usecols=['visit'], dtype={'visit': 'Int8'})
        if as_frame:
            target = target['visit']
    else:
        raise ValueError(f"Target_column value must be from {['visit', 'conversion']}. "
                         f"Got value {target_column}.")

    if return_X_y_t:
        if as_frame:
            return data, target, treatment
        else:
            return data.to_numpy(), target.to_numpy(), treatment.to_numpy()
    else:
        target_name = target_column
        treatment_name = treatment_feature
        module_path = os.path.dirname(__file__)
        with open(os.path.join(module_path, 'descr', 'criteo.rst')) as rst_file:
            fdescr = rst_file.read()
        if as_frame:
            return Bunch(data=data, target=target, treatment=treatment, DESCR=fdescr, feature_names=feature_names,
                         target_name=target_name, treatment_name=treatment_name)
        else:
            return Bunch(data=data.to_numpy(), target=target.to_numpy(), treatment=treatment.to_numpy(), DESCR=fdescr,
                         feature_names=feature_names, target_name=target_name, treatment_name=treatment_name)


def fetch_hillstrom(target='visit',
                    data_home=None,
                    dest_subdir=None,
                    download_if_missing=True,
                    return_X_y=False):
    """Load the hillstrom dataset.
    
        Args:
          target : str, desfault=visit. 
              Can also be conversion, and spend
          data_home : str, default=None
              Specify another download and cache folder for the datasets.
          dest_subdir : str, default=None
          download_if_missing : bool, default=True
              If False, raise a IOError if the data is not locally available
              instead of trying to download the data from the source site.
        
        Returns:
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
    hillstrom = pd.read_csv(csv_path)
    hillstrom_data = hillstrom.drop(columns=['segment', target])
    
    module_path = os.path.dirname('__file__')
    with open(os.path.join(module_path, 'descr', 'hillstrom.rst')) as rst_file:
        fdescr = rst_file.read()
    
    if return_X_y:
        return treatment, data, target
    
    return Bunch(treatment=hillstrom['segment'],
                 target=hillstrom[target],
                 data=hillstrom_data, DESCR=fdescr)
