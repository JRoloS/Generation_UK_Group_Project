# UNIT TESTING FOR FUNCTIONS
# Run from terminal with py pytest -v test_functions.py   

# IMPORTS 

import os 
import dotenv
from unittest.mock import patch, Mock, MagicMock, call
import unittest
import pandas as pd
import psycopg2
import io
import csv

# -------------------------------- UNIT TEST FUNCTIONS ----------------------------------------------------------


############################   ABSOLUTE LOCAL PATH  ###########################

# [1/1] ---- Unit Test for RawData Path --------------------
from absolute_local_path import absolute_path_for_raw_data #NOTE: This one will be removed when moving to Lambdas 

def test_absolute_path_for_raw_data():
     raw_data_file = "chesterfield_25-08-2021_09-00-00.csv"
     raw_csv = absolute_path_for_raw_data(raw_data_file)
     expected_csv_path = os.path.abspath("./raw_data") + "\\" + raw_data_file
     assert raw_csv == expected_csv_path
    
test_absolute_path_for_raw_data()
# [1/1] ---- [end] Unit Test for RawData Path ----------------
############################### END ABSOLUTE LOCAL PATH ########################



############################## DATABASE #######################################

# [1/7] ---- Unit test for setup_db_connection ------------------
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
# [1/7] ---- [end] Unit test for setup_db_connection -----------------


# [2/7] ------ Unit Test for create_redshift_database_schema ------------------------------------------
from database import create_redshift_database_schema

class TestCreateRedshiftDatabaseSchema(unittest.TestCase):
    @patch("database.create_locations_db_table")
    @patch("database.create_orders_db_table")
    @patch("database.create_orders_products_db_table")
    @patch("database.create_payment_types_db_table")
    @patch("database.create_products_db_table")
    @patch("database.add_foreign_key_constraints")
    def test_create_redshift_database_schema(self, mock_fk, mock_products, mock_payment_types, mock_orders_products, mock_orders, mock_locations):
        mock_cursor = Mock()
        create_redshift_database_schema(mock_cursor)

        mock_locations.assert_called_once_with(mock_cursor)
        mock_orders.assert_called_once_with(mock_cursor)
        mock_orders_products.assert_called_once_with(mock_cursor)
        mock_payment_types.assert_called_once_with(mock_cursor)
        mock_products.assert_called_once_with(mock_cursor)
        mock_fk.assert_called_once_with(mock_cursor)
# [2/7] ------ [end] Unit Test for create_redshift_database_schema -----------------------------------------


######################## END DATABASE #######################################




#########################   TRANSFORMATION ###################################

# [1/8] ------ TEST sanatise_csv_order_table ------------------------
from transformation import sanitise_csv_order_table

class TestSanitiseCsvOrderTable(unittest.TestCase):

    def test_sanitise_csv_order_table(self):
        # Define the raw CSV input
        raw_csv = [
         ['2022-05-09 13:00:00', 'London', 'John Doe', 'Americano, 1.20, Latte 2.20', 2.40, 'CARD', '1234'],
         ['2022-05-09 13:30:00', 'Not London', 'Jane Doe', 'Tea 1.15', 1.15, 'CASH', '5678']
        ]

        # Convert the raw_csv list to a bytes-like object
        csv_bytes = io.StringIO()
        writer = csv.writer(csv_bytes)
        writer.writerows(raw_csv)
        csv_bytes.seek(0)

        # Define the expected values
        expected_columns = ['date_time', 'location', 'transaction_total', 'payment_type']
        expected_data = [
            ['2022-05-09 13:00:00', 'London', 2.40, 'CARD'],
            ['2022-05-09 13:30:00', 'Not London', 1.15, 'CASH']
        ]

        # Call the function to get the actual result
        actual_result = sanitise_csv_order_table(csv_bytes.read().encode())

        # Check that the column names are as expected
        self.assertEqual(list(actual_result.columns), expected_columns)

        # Check that the data is as expected
        for i, row in enumerate(actual_result.values):
            self.assertEqual(list(row), expected_data[i])
# [1/8] ------ [end] TEST sanatise_csv_order_table ------------------------

# [2/8] ---- Unit test for sort_time_to_postgre_format (We have to be sure that the expected format is YYYY-MM-DD)
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
# [2/8] --- [end] Unit test for sort_time_to_postgre_format ---------------------------------------


# [3/8] --- Unit test for Update Locations ---
from transformation import update_locations

class TestUpdateLocations(unittest.TestCase):
    def test_update_locations(self):
        # Create a sample DataFrame with some London as a Location
        df = pd.DataFrame({
            'date_time': ['2022-05-09 13:00:00'],
            'location': ['London'],
            'transaction_total': [2.40],
            'payment_type': ['CARD']
        })

        # Set up a mock cursor object that returns location IDs
        mock_cursor = MagicMock()
        mock_cursor.fetchone.side_effect = [(1,), None]
        # It will mock the insert, and will return 1 as the location already exists in the DB

        # Call the function to get the actual result
        actual_result = update_locations(df, mock_cursor)

        # Check that the location names have been replaced with location IDs
        expected_result = pd.DataFrame({
            'date_time': ['2022-05-09 13:00:00'],
            'location': [1],
            'transaction_total': [2.40],
            'payment_type': ['CARD']
        })


         # Check that the shape of the DataFrames is the same
        self.assertEqual(actual_result.shape, expected_result.shape)

# [3/8] --- [end] Unit test for Update Locations ---


# [4/8] --- Update Payment Types ----
from transformation import update_payment_types


class TestUpdatePaymentTypes(unittest.TestCase):
    def test_update_payment_types(self):
        # Create a sample DataFrame with some London as a Location
        df = pd.DataFrame({
            'date_time': ['2022-05-09 13:00:00'],
            'location': ['London'],
            'transaction_total': [2.40],
            'payment_type': ['CARD']
        })

        # Set up a mock cursor object that returns location IDs
        mock_cursor = MagicMock()
        mock_cursor.fetchone.side_effect = [(1,), None]
        # It will mock the insert, and will return 1 as the location already exists in the DB

        # Call the function to get the actual result
        actual_result = update_payment_types(df, mock_cursor)

        # Check that the location names have been replaced with location IDs
        expected_result = pd.DataFrame({
            'date_time': ['2022-05-09 13:00:00'],
            'location': ['London'],
            'transaction_total': [2.40],
            'payment_type': [1]
        })


         # Check that the shape of the DataFrames is the same
        self.assertEqual(actual_result.shape, expected_result.shape)
# [4/8] [end] --- Update Payment Types ---

#[5/8] --- Unit test for Update Orders Table ---
from transformation import update_orders_table

class TestUpdateOrdersTable(unittest.TestCase):
    
    def test_update_orders_table(self):
        # Define mock data
        mock_df = pd.DataFrame({
            'date_time': ['2022-05-10 12:34:56', '2022-05-11 14:20:00', '2022-05-11 15:30:00'],
            'location': [1, 2, 3],
            'transaction_total': [10.0, 20.0, 30.0],
            'payment_type': [1, 2, 3]
        })
        mock_cursor = Mock()

        # Call the function
        update_orders_table(mock_df, mock_cursor)

        # Check that the correct SQL statements were executed
        expected_calls = [
            call("INSERT INTO orders (date_time, location_id, transaction_total, payment_type_id) VALUES (%s, %s, %s, %s)",
                 ('2022-05-10 12:34:56', 1, 10.0, 1)),
            call("INSERT INTO orders (date_time, location_id, transaction_total, payment_type_id) VALUES (%s, %s, %s, %s)",
                 ('2022-05-11 14:20:00', 2, 20.0, 2)),
            call("INSERT INTO orders (date_time, location_id, transaction_total, payment_type_id) VALUES (%s, %s, %s, %s)",
                 ('2022-05-11 15:30:00', 3, 30.0, 3))
        ]
        self.assertEqual(mock_cursor.execute.call_args_list, expected_calls)

#[5/8] [End] --- Test update orders table ---

############################ END TRANSFORMATION #############################################