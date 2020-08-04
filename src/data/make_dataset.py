import logging
import os
import traceback

import pandas as pd
from dotenv import find_dotenv, load_dotenv


class DataTransFormation:
    def __init__(self):
        self.idx = None
        self.df = None

    def read_csv_data(self, file_csv):
        df = pd.read_csv(os.path.join(file_csv), index_col=0)
        self.df = DataTransFormation.clean_data(df)
        self.idx = DataTransFormation.null_dates(df)

    @staticmethod
    def clean_data(df=None):
        if df is not None:
            DT = DataTransFormation
            df = DT.time_format(df)
            df = DT.create_order_session(DT.create_order_weekday(df))
            return DT.remove_empty_rows(DT.create_metric_dimension_product(df))

    @staticmethod
    def create_order_weekday(df=None):
        if df is None:
            return
        df['order_purchase_weekday'] = df['order_purchase_timestamp'].dt.day_name()
        df = df.assign(order_purchase_session=pd.cut(df.order_purchase_timestamp.dt.hour, [0, 6, 12, 18, 24],
                                                     labels=['Night', 'Morning', 'Afternoon', 'Evening'], right=False))
        return df

    @staticmethod
    def create_order_session(df=None):
        if df is None:
            return
        winter = [12, 1, 2]
        spring = [3, 4, 5]
        summer = [6, 7, 8]
        autumn = [9, 10, 11]
        d = {**dict.fromkeys(winter, 'winter'), **dict.fromkeys(spring, 'spring'), **dict.fromkeys(summer, 'summer'),
             **dict.fromkeys(autumn, 'autumn')}

        df['season'] = list(map(d.get, df.order_purchase_timestamp.dt.month))
        return df

    @staticmethod
    def create_metric_dimension_product(df=None):
        if df is not None:
            df['product_weight_kg'], df['product_weight_g'] = df['product_weight_g'] // 1000, \
                                                              df['product_weight_g'] % 1000
            df['product_length_m'], df['product_length_cm'] = df['product_length_cm'] // 100, \
                                                              df['product_length_cm'] % 100
            df['product_height_m'], df['product_height_cm'] = df['product_height_cm'] // 100, \
                                                              df['product_height_cm'] % 100
            df['product_width_m'], df['product_width_cm'] = df['product_width_cm'] // 100, \
                                                            df['product_width_cm'] % 100
        return df

    @staticmethod
    def remove_empty_rows(df=None):
        if df is None:
            return
        df = df[df['product_category_name_english'].notna()]
        return df

    @staticmethod
    def time_format(data):
        '''
        Function to convert dataset time columns into pandas datetime and calculations for promise date,
        approval time and total time to deliver
        '''
        data.order_purchase_timestamp = pd.to_datetime(data.order_purchase_timestamp, format='%d/%m/%Y %H:%M')
        data.order_approved_at = pd.to_datetime(data.order_approved_at, errors='coerce', format='%d/%m/%Y %H:%M')
        data.order_estimated_delivery_date = pd.to_datetime(data.order_estimated_delivery_date, errors='coerce',
                                                            format='%d/%m/%Y %H:%M')
        data.order_delivered_customer_date = pd.to_datetime(data.order_delivered_customer_date, errors='coerce',
                                                            format='%d/%m/%Y %H:%M')
        data['promise_date'] = data.order_estimated_delivery_date >= data.order_delivered_customer_date  # True if product delivered before or at estimated delivery date
        data['approval_time'] = data.order_approved_at - data.order_purchase_timestamp  # Time for buyer to approve sale
        data['total_time_to_deliver'] = data.order_delivered_customer_date - data.order_purchase_timestamp  # total time from pruchase to delivery
        return data

    @staticmethod
    def null_dates(data):
        '''
        Function to find indexes of order's with null times, most of these rows are order_delievered_customer_date.
        This is probably due to cancelations
        '''
        na = data[['order_purchase_timestamp', 'order_approved_at', 'order_estimated_delivery_date',
                   'order_delivered_customer_date']][data[
            ['order_purchase_timestamp', 'order_approved_at', 'order_estimated_delivery_date',
             'order_delivered_customer_date']].isna().any(1)].index

        return na


def main(project_dir):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')
    try:
        df = DataTransFormation()
        df.read_csv_data(project_dir)
        logger.info(df.df)
        logger.info(df.idx)
        df.df.to_csv(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                               '..',
                                               os.path.pardir,
                                               'data',
                                               'processed',
                                               'processed_consolidated_ecommerce_olist_1.csv')),
                     index=False, header=True)
    except Exception as e:
        logger.warning(traceback.print_exc())
        logger.info(project_dir)
        logger.error('Unable to read CSV: {}'.format(e))


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                               '..',
                                               os.path.pardir,
                                               'data',
                                               'interim',
                                               'consolidated_ecommerce_olist_1.csv'))

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main(project_dir)
