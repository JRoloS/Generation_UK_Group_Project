# UNIT TESTING FOR FUNCTIONS
# Run from terminal with py pytest -v test_functions.py   

# IMPORTS 

import os 
import dotenv
from unittest.mock import patch, Mock, MagicMock
import unittest
import pandas as pd
import psycopg2

# -------------------------------- UNIT TEST FUNCTIONS ----------------------------------------------------------

# ---- Unit Test for RawData Path --------------------
from absolute_local_path import absolute_path_for_raw_data #NOTE: This one will be removed when moving to Lambdas 

def test_absolute_path_for_raw_data():
     raw_data_file = "chesterfield_25-08-2021_09-00-00.csv"
     raw_csv = absolute_path_for_raw_data(raw_data_file)
     expected_csv_path = os.path.abspath("./raw_data") + "\\" + raw_data_file
     assert raw_csv == expected_csv_path
    
test_absolute_path_for_raw_data()
# ---- [end] Unit Test for RawData Path ----------------



# ---- Unit test for setup_db_connection ------------------
from database import setup_db_connection

class TestSetupDbConnection(unittest.TestCase):
    @patch("psycopg2.connect")
    def test_setup_db_connection(self, mock_connect):
        mock_connection = Mock()
        mock_connect.return_value = mock_connection

        host = "localhost"
        user = "testuser"
        password = "testpass"
        database = "testdb"
        port = "1234"

        conn = setup_db_connection(
            host=host, 
            user=user, 
            password=password, 
            db=database, 
            port=port
        )

        mock_connect.assert_called_once_with(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )

        self.assertEqual(conn, mock_connection)
#---- [end] Unit test for setup_db_connection -----------------





# --- TRANSFORMATION UNIT TESTING -----------------------------
#---- Unit test for sanatise_csv_order_table ------------------ 
# from transformation import sanitise_csv_order_table

# def test_sanitise_csv_order_table():
#     #Dummy csv file path
#     raw_csv = "dummy.csv"
    
#     #Dummy DataFrame to return
#     columns = ['date_time', 'location', 'full_name', 'order', 'transaction_total', 'payment_type', 'card_number']
#     data = [
#         ['2022-05-09 13:00:00', 'London', 'John Doe', 'Americano, 1.20, Latte 2.20', 2.40, 'CARD', '1234'],
#         ['2022-05-09 13:30:00', 'Not London', 'Jane Doe', 'Tea 1.15', 1.15, 'CASH', '5678']
#     ]
#     dummy_df = pd.DataFrame(data, columns=columns)
    
#     # mock the pd.read_csv function and return the dummy DataFrame
#     pd.read_csv = Mock(return_value=dummy_df)
    
#     # call the function being tested
#     sanitised_df = sanitise_csv_order_table(raw_csv)
    
#     # check if the returned DataFrame is correct
#     expected_columns = ['date_time', 'location', 'transaction_total', 'payment_type']
#     expected_data = [
#         ['2022-05-09 13:00:00', 'London', 2.40, 'CARD'],
#         ['2022-05-09 13:30:00', 'Not London', 1.15, 'CASH']
#     ]
#     expected_df = pd.DataFrame(expected_data, columns=expected_columns)
    
#     pd.testing.assert_frame_equal(sanitised_df, expected_df)
# #---- [end] Unit test for sanatise_csv_order_table -------------



# def sanitise_csv_order_table(raw_csv):
#     try:
#         columns =  ['date_time', 'location', 'full_name', 'order', 'transaction_total', 'payment_type', 'card_number']  # Headers for the orders csv files
#         df = pd.read_csv(io.BytesIO(raw_csv), header=None, names=columns)
#         sanitised_df = df.drop(columns=['full_name', 'order', 'card_number'])

#     except FileNotFoundError as fnfe:
#         print(f'File not found: {fnfe}')

#     return sanitised_df
















# # --- Unit test for sort_time_to_postgre_format (We have to be sure that the expected format is YYYY-MM-DD)
from transformation import sort_time_to_postgre_format

def test_sort_time_to_postgre_format():
    
    # create mock dataframe
    data = {'date_time': ['30/12/2020 09:00'],
            'location': ['London'],
            'transaction_total': [10.0]}
    df = pd.DataFrame(data)

    # call function with mock dataframe
    sorted_df = sort_time_to_postgre_format(df)

    # check if dataframe was sorted correctly
    expected_datetime_str = '2020-12-30 09:00:00'
    expected_datetime = pd.to_datetime(expected_datetime_str, format='%Y-%m-%d %H:%M:%S')
    assert sorted_df['date_time'].iloc[0] == expected_datetime
# # --- [end] Unit test for sort_time_to_postgre_format ---------------------------------------


