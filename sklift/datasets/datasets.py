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

        :Attribute Information:
            -customer                           age
            -CardHolder	                        customer id
            -cheque_count_12m_g*	            number of customer receipts collected within last 12 months before campaign. g* is a product group
            -cheque_count_3m_g*	                number of customer receipts collected within last 3 months before campaign. g* is a product group
            -cheque_count_6m_g*	                number of customer receipts collected within last 6 months before campaign. g* is a product group
            -children	                        number of children
            -crazy_purchases_cheque_count_12m	number of customer receipts with items purchased on "crazy" marketing campaign collected within last 12 months before campaign
            -crazy_purchases_cheque_count_1m	number of customer receipts with items purchased on "crazy" marketing campaign collected within last 1 month before campaign
            -crazy_purchases_cheque_count_3m	number of customer receipts with items purchased on "crazy" marketing campaign collected within last 3 months before campaign
            -crazy_purchases_cheque_count_6m	number of customer receipts with items purchased on "crazy" marketing campaign collected within last 6 months before campaign
            -crazy_purchases_goods_count_12m	items amount purchased on "crazy" marketing campaign collected within last 12 months before campaign
            -crazy_purchases_goods_count_6m	    items amount purchased on "crazy" marketing campaign collected within last 6 months before campaign
            -disc_sum_6m_g34	                discount sum for past 6 month on a 34 product group
            -food_share_15d	                    food share in customer purchases for 15 days
            -food_share_1m	                    food share in customer purchases for 1 month
            -gender	                            customer gender
            -group	                            treatment/control group flag
            -k_var_cheque_15d	                average check coefficient of variation for 15 days
            -k_var_cheque_3m	                average check coefficient of variation for 3 months
            -k_var_cheque_category_width_15d	coefficient of variation of the average number of purchased categories (2nd level of the hierarchy) in one receipt for 15 days
            -k_var_cheque_group_width_15d	    coefficient of variation of the average number of purchased groups (1st level of the hierarchy) in one receipt for 15 days
            -k_var_count_per_cheque_15d_g*  	unique product id (SKU) coefficient of variation for 15 days for g* product group
            -k_var_count_per_cheque_1m_g*	    unique product id (SKU) coefficient of variation for 1 month for g* product group
            -k_var_count_per_cheque_3m_g*	    unique product id (SKU) coefficient of variation for 3 months for g* product group
            -k_var_count_per_cheque_6m_g*	    unique product id (SKU) coefficient of variation for 6 months for g* product group
            -k_var_days_between_visits_15d	    coefficient of variation of the average period between visits for 15 days
            -k_var_days_between_visits_1m	    coefficient of variation of the average period between visits for 1 month
            -k_var_days_between_visits_3m	    coefficient of variation of the average period between visits for 3 months
            -k_var_disc_per_cheque_15d	        discount sum coefficient of variation for 15 days
            -k_var_disc_share_12m_g32	        discount amount coefficient of variation for 12 months for g* product group
            -k_var_disc_share_15d_g*	        discount amount coefficient of variation for 15 days for g* product group
            -k_var_disc_share_1m_g*	            discount amount coefficient of variation for 1 month for g* product group
            -k_var_disc_share_3m_g*	            discount amount coefficient of variation for 3 months for g* product group
            -k_var_disc_share_6m_g*	            discount amount coefficient of variation for 6 months for g* product group
            -k_var_discount_depth_15d	        discount amount coefficient of variation for 1 month
            -k_var_discount_depth_1m	        discount amount coefficient of variation for 15 days
            -k_var_sku_per_cheque_15d	        number of unique product ids (SKU) coefficient of variation for 15 days
            -k_var_sku_price_12m_g*	            price coefficient of variation for 15 days, 3, 6, 12 months for g* product group
            -main_format	                    store type (1 - grociery store, 0 - superstore)
            -mean_discount_depth_15d	        mean discount depth for 15 days
            -months_from_register	            number of months from a moment of register
            -perdelta_days_between_visits_15_30d	timdelta in percent between visits during the first half of the month and visits during second half of the month
            -promo_share_15d	                promo goods share in the customer bucket
            -response_att	                    binary target variable = store visit
            -response_sms	                    share of customer responses to previous SMS. Response = store visit
            -response_viber	                    share of responses to previous Viber messages. Response = store visit
            -sale_count_12m_g*	                number of purchased items from the group * for 12 months
            -sale_count_3m_g*	                number of purchased items from the group * for 3 months
            -sale_count_6m_g*	                number of purchased items from the group * for 6 months
            -sale_sum_12m_g*	                sum of sales from the group * for 12 months
            -sale_sum_3m_g*	                    sum of sales from the group * for 3 months
            -sale_sum_6m_g*	                    sum of sales from the group * for 6 months
            -stdev_days_between_visits_15d	    coefficient of variation of the days between visits for 15 days
            -stdev_discount_depth_15d	        discount sum coefficient of variation for 15 days
            -stdev_discount_depth_1m	        discount sum coefficient of variation for 1 month

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
