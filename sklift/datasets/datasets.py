import os
import shutil

import pandas as pd
import requests
from sklearn.utils import Bunch


def get_data_dir():
    """Return the path of the scikit-uplift data dir.

    This folder is used by some large dataset loaders to avoid downloading the data several times.

    By default the data dir is set to a folder named ‘scikit_learn_data’ in the user home folder.

    Returns:
        string: The path to scikit-uplift data dir.

    """
    return os.path.join(os.path.expanduser("~"), "scikit-uplift-data")


def _create_data_dir(path):
    """Creates a directory, which stores the datasets.

    Args:
        path (str): The path to scikit-uplift data dir.

    """
    if not os.path.isdir(path):
        os.makedirs(path)


def _download(url, dest_path):
    """Download the file from url and save it locally.

    Args:
        url (str): URL address, must be a string.
        dest_path (str): Destination of the file.

    """
    if isinstance(url, str):
        req = requests.get(url, stream=True)
        req.raise_for_status()

        with open(dest_path, "wb") as fd:
            for chunk in req.iter_content(chunk_size=2 ** 20):
                fd.write(chunk)
    else:
        raise TypeError("URL must be a string")


def _get_data(data_home, url, dest_subdir, dest_filename, download_if_missing):
    """Return the path to the dataset.
    
    Args:
        data_home (str): The path to scikit-uplift data dir.
        url (str): The URL to the dataset.
        dest_subdir (str): The name of the folder in which the dataset is stored.
        dest_filename (str): The name of the dataset.
        download_if_missing (bool): If False, raise a IOError if the data is not locally available instead of
            trying to download the data from the source site.

    Returns:
        string: The path to the dataset.

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

    _create_data_dir(data_dir)

    dest_path = os.path.join(data_dir, dest_filename)

    if not os.path.isfile(dest_path):
        if download_if_missing:
            _download(url, dest_path)
        else:
            raise IOError("Dataset missing")
    return dest_path


def clear_data_dir(path=None):
    """Delete all the content of the data home cache.

        Args:
            path (str): The path to scikit-uplift data dir

    """
    if path is None:
        path = get_data_dir()
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)


def fetch_lenta(data_home=None, dest_subdir=None, download_if_missing=True, return_X_y_t=False):
    """Load and return the Lenta dataset (classification).

    An uplift modeling dataset containing data about Lenta's customers grociery shopping and
    related marketing campaigns.

    Major columns:

    - ``group`` (str): treatment/control group flag
    - ``response_att`` (binary): target
    - ``gender`` (str): customer gender
    - ``age`` (float): customer age
    - ``main_format`` (int): store type (1 - grociery store, 0 - superstore)

    Read more in the :ref:`docs <Lenta>`.

    Args:
        data_home (str): The path to the folder where datasets are stored.
        dest_subdir (str): The name of the folder in which the dataset is stored.
        download_if_missing (bool): Download the data if not present. Raises an IOError if False and data is missing.
        return_X_y_t (bool): If True, returns (data, target, treatment) instead of a Bunch object.

    Returns:
        Bunch or tuple: dataset.

        Bunch:
            By default dictionary-like object, with the following attributes:

                * ``data`` (DataFrame object): Dataset without target and treatment.
                * ``target`` (Series object): Column target by values.
                * ``treatment`` (Series object): Column treatment by values.
                * ``DESCR`` (str): Description of the Lenta dataset.
                * ``feature_names`` (list): Names of the features.
                * ``target_name`` (str): Name of the target.
                * ``treatment_name`` (str): Name of the treatment.

        Tuple:
            tuple (data, target, treatment) if `return_X_y` is True

    """

    url = 'https://winterschool123.s3.eu-north-1.amazonaws.com/lentadataset.csv.gz'
    filename = url.split('/')[-1]
    csv_path = _get_data(data_home=data_home, url=url, dest_subdir=dest_subdir,
                         dest_filename=filename,
                         download_if_missing=download_if_missing)

    target_col = 'response_att'
    treatment_col = 'group'

    data = pd.read_csv(csv_path)
    treatment, target = data[treatment_col], data[target_col]

    data = data.drop([target_col, treatment_col], axis=1)
    feature_names = list(data.columns)

    if return_X_y_t:
        return data, target, treatment

    module_path = os.path.dirname(__file__)
    with open(os.path.join(module_path, 'descr', 'lenta.rst')) as rst_file:
        fdescr = rst_file.read()

    return Bunch(data=data, target=target, treatment=treatment, DESCR=fdescr,
                 feature_names=feature_names, target_name=target_col, treatment_name=treatment_col)


def fetch_x5(data_home=None, dest_subdir=None, download_if_missing=True):
    """Load and return the X5 RetailHero dataset (classification).

    The dataset contains raw retail customer purchases, raw information about products and general info about customers.

    Major columns:

    - ``treatment_flg`` (binary): treatment/control group flag
    - ``target`` (binary): target
    - ``customer_id`` (str): customer id - primary key for joining

    Read more in the :ref:`docs <X5>`.

    Args:
        data_home (str, unicode): The path to the folder where datasets are stored.
        dest_subdir (str, unicode): The name of the folder in which the dataset is stored.
        download_if_missing (bool): Download the data if not present. Raises an IOError if False and data is missing

    Returns:
        Bunch: dataset.

         Dictionary-like object, with the following attributes.

            * ``data`` (Bunch object): dictionary-like object without target and treatment:

                * ``clients`` (ndarray or DataFrame object): General info about clients.
                * ``train`` (ndarray or DataFrame object): A subset of clients for training.
                * ``purchases`` (ndarray or DataFrame object): clients’ purchase history prior to communication.
            * ``target`` (Series object): Column target by values.
            * ``treatment`` (Series object): Column treatment by values.
            * ``DESCR`` (str): Description of the Lenta dataset.
            * ``feature_names`` (Bunch object): Names of the features.
            * ``target_name`` (str): Name of the target.
            * ``treatment_name`` (str): Name of the treatment.

    References:
        https://ods.ai/competitions/x5-retailhero-uplift-modeling/data

    """
    url_train = 'https://timds.s3.eu-central-1.amazonaws.com/uplift_train.csv.gz'
    file_train = url_train.split('/')[-1]
    csv_train_path = _get_data(data_home=data_home, url=url_train, dest_subdir=dest_subdir,
                               dest_filename=file_train,
                               download_if_missing=download_if_missing)
    train = pd.read_csv(csv_train_path)
    train_features = list(train.columns)

    target_col = 'target'
    treatment_col = 'treatment_flg'

    treatment, target = train[treatment_col], train[target_col]

    train = train.drop([target_col, treatment_col], axis=1)

    url_clients = 'https://timds.s3.eu-central-1.amazonaws.com/clients.csv.gz'
    file_clients = url_clients.split('/')[-1]
    csv_clients_path = _get_data(data_home=data_home, url=url_clients, dest_subdir=dest_subdir,
                                 dest_filename=file_clients,
                                 download_if_missing=download_if_missing)
    clients = pd.read_csv(csv_clients_path)
    clients_features = list(clients.column)

    url_purchases = 'https://timds.s3.eu-central-1.amazonaws.com/purchases.csv.gz'
    file_purchases = url_purchases.split('/')[-1]
    csv_purchases_path = _get_data(data_home=data_home, url=url_purchases, dest_subdir=dest_subdir,
                                   dest_filename=file_purchases,
                                   download_if_missing=download_if_missing)
    purchases = pd.read_csv(csv_purchases_path)
    purchases_features = list(purchases.columns)

    data = Bunch(clients=clients, train=train, purchases=purchases)
    feature_names = Bunch(train_features=train_features, clients_features=clients_features,
                          purchases_features=purchases_features)

    module_path = os.path.dirname(__file__)
    with open(os.path.join(module_path, 'descr', 'x5.rst')) as rst_file:
        fdescr = rst_file.read()

    return Bunch(data=data, target=target, treatment=treatment, DESCR=fdescr,
                 feature_names=feature_names, target_name='target', treatment_name='treatment_flg')


def fetch_criteo(target_col='visit', treatment_col='treatment', data_home=None, dest_subdir=None,
                 download_if_missing=True, percent10=False, return_X_y_t=False):
    """Load and return the Criteo Uplift Prediction Dataset (classification).

    This dataset is constructed by assembling data resulting from several incrementality tests, a particular randomized
    trial procedure where a random part of the population is prevented from being targeted by advertising.

    Major columns:

    * ``treatment`` (binary): treatment
    * ``exposure`` (binary): treatment
    * ``visit`` (binary): target
    * ``conversion`` (binary): target
    * ``f0, ... , f11`` (float): feature values

    Read more in the :ref:`docs <Criteo>`.

    Args:
        target_col (string, 'visit', 'conversion' or 'all', default='visit'): Selects which column from dataset
            will be target. If 'all', return a DataFrame with all targets cols.
        treatment_col (string,'treatment', 'exposure' or 'all', default='treatment'): Selects which column from dataset
            will be treatment. If 'all', return a DataFrame with all treatment cols.
        data_home (string): Specify a download and cache folder for the datasets.
        dest_subdir (string): The name of the folder in which the dataset is stored.
        download_if_missing (bool, default=True): If False, raise an IOError if the data is not locally available
            instead of trying to download the data from the source site.
        percent10 (bool, default=False): Whether to load only 10 percent of the data.
        return_X_y_t (bool, default=False): If True, returns (data, target, treatment) instead of a Bunch object.

    Returns:
        Bunch or tuple: dataset.

        Bunch:
            By default dictionary-like object, with the following attributes:

                * ``data`` (DataFrame object): Dataset without target and treatment.
                * ``target`` (Series or DataFrame object): Column target by values.
                * ``treatment`` (Series or DataFrame object): Column treatment by values.
                * ``DESCR`` (str): Description of the Lenta dataset.
                * ``feature_names`` (list): Names of the features.
                * ``target_name`` (str list): Name of the target.
                * ``treatment_name`` (str or list): Name of the treatment.

        Tuple:
            tuple (data, target, treatment) if `return_X_y` is True

    References:
        “A Large Scale Benchmark for Uplift Modeling”
        Eustache Diemert, Artem Betlei, Christophe Renaudin; (Criteo AI Lab), Massih-Reza Amini (LIG, Grenoble INP)
    """
    treatment_cols = ['exposure', 'treatment']
    if treatment_col == 'all':
        treatment_col = treatment_cols
    elif treatment_col not in treatment_cols:
        raise ValueError(f"treatment_col value must be in {treatment_cols + ['all']}. "
                         f"Got value {treatment_col}.")

    target_cols = ['visit', 'conversion']
    if target_col == 'all':
        target_col = target_cols
    elif target_col not in target_cols:
        raise ValueError(f"target_col value must be from {target_cols + ['all']}. "
                         f"Got value {target_col}.")

    if percent10:
        url = 'https://criteo-bucket.s3.eu-central-1.amazonaws.com/criteo10.csv.gz'
    else:
        url = "https://criteo-bucket.s3.eu-central-1.amazonaws.com/criteo.csv.gz"

    filename = url.split('/')[-1]
    csv_path = _get_data(data_home=data_home, url=url, dest_subdir=dest_subdir,
                         dest_filename=filename,
                         download_if_missing=download_if_missing)

    dtypes = {
        'exposure': 'Int8',
        'treatment': 'Int8',
        'conversion': 'Int8',
        'visit': 'Int8'
    }
    data = pd.read_csv(csv_path, dtype=dtypes)
    treatment, target = data[treatment_col], data[target_col]

    data = data.drop(target_cols + treatment_cols, axis=1)

    if return_X_y_t:
        return data, target, treatment

    feature_names = list(data.columns)

    module_path = os.path.dirname(__file__)
    with open(os.path.join(module_path, 'descr', 'criteo.rst')) as rst_file:
        fdescr = rst_file.read()

    return Bunch(data=data, target=target, treatment=treatment, DESCR=fdescr, feature_names=feature_names,
                 target_name=target_col, treatment_name=treatment_col)


def fetch_hillstrom(target_col='visit', data_home=None, dest_subdir=None, download_if_missing=True,
                    return_X_y_t=False):
    """Load and return Kevin Hillstrom Dataset MineThatData (classification or regression).

    This dataset contains 64,000 customers who last purchased within twelve months.
    The customers were involved in an e-mail test.

    Major columns:

    * ``visit`` (binary): target. 1/0 indicator, 1 = Customer visited website in the following two weeks.
    * ``conversion`` (binary): target. 1/0 indicator, 1 = Customer purchased merchandise in the following two weeks.
    * ``spend`` (float): target. Actual dollars spent in the following two weeks.
    * ``segment`` (str): treatment. The e-mail campaign the customer received

    Read more in the :ref:`docs <Hillstrom>`.

    Args:
        target_col (string, 'visit' or 'conversion', 'spend' or 'all', default='visit'): Selects which column from dataset
            will be target
        data_home (str): The path to the folder where datasets are stored.
        dest_subdir (str): The name of the folder in which the dataset is stored.
        download_if_missing (bool): Download the data if not present. Raises an IOError if False and data is missing.
        return_X_y_t (bool, default=False): If True, returns (data, target, treatment) instead of a Bunch object.
        
    Returns:
        Bunch or tuple: dataset.

        Bunch:
            By default dictionary-like object, with the following attributes:

                * ``data`` (DataFrame object): Dataset without target and treatment.
                * ``target`` (Series or DataFrame object): Column target by values.
                * ``treatment`` (Series object): Column treatment by values.
                * ``DESCR`` (str): Description of the Lenta dataset.
                * ``feature_names`` (list): Names of the features.
                * ``target_name`` (str or list): Name of the target.
                * ``treatment_name`` (str): Name of the treatment.

        Tuple:
            tuple (data, target, treatment) if `return_X_y` is True

    References:
        https://blog.minethatdata.com/2008/03/minethatdata-e-mail-analytics-and-data.html

    """
    target_cols = ['visit', 'conversion', 'spend']
    if target_col == 'all':
        target_col = target_cols
    elif target_col not in target_cols:
        raise ValueError(f"target_col value must be from {target_cols + ['all']}. "
                         f"Got value {target_col + ['all']}.")

    url = 'https://hillstorm1.s3.us-east-2.amazonaws.com/hillstorm_no_indices.csv.gz'
    filename = url.split('/')[-1]
    csv_path = _get_data(data_home=data_home, url=url, dest_subdir=dest_subdir,
                         dest_filename=filename,
                         download_if_missing=download_if_missing)

    treatment_col = 'segment'

    data = pd.read_csv(csv_path)
    treatment, target = data[treatment_col], data[target_col]

    data = data.drop(target_cols + [treatment_col], axis=1)

    if return_X_y_t:
        return data, target, treatment

    feature_names = list(data.columns)

    module_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(module_path, 'descr', 'hillstrom.rst')) as rst_file:
        fdescr = rst_file.read()

    return Bunch(data=data, target=target, treatment=treatment, DESCR=fdescr,
                 feature_names=feature_names, target_name=target_col, treatment_name=treatment_col)
