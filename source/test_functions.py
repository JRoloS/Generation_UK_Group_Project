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
    @patch("database.psycopg2.connect")  # Update the patched import path
    def test_setup_db_connection(self, mock_connect):
        mock_connection = Mock()
        mock_connect.return_value = mock_connection

        host = "localhost"
        user = "testuser"
        password = "testpass"
        database = "testdb"
        port = "1234"
        invocation_id = "12345"  # Add the invocation_id

        conn = setup_db_connection(
            host=host,
            user=user,
            password=password,
            db=database,
            port=port,
            invocation_id=invocation_id,  # Pass the invocation_id
        )

        mock_connect.assert_called_once_with(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port,
        )

        self.assertEqual(conn, mock_connection)

# # [1/7] ---- [end] Unit test for setup_db_connection -----------------


# # [2/7] ------ Unit Test for create_redshift_database_schema ------------------------------------------
from database import create_redshift_database_schema

class TestCreateRedshiftDatabaseSchema(unittest.TestCase):
    @patch("database.create_locations_db_table")
    @patch("database.create_orders_db_table")
    @patch("database.create_orders_products_db_table")
    @patch("database.create_payment_types_db_table")
    @patch("database.create_products_db_table")
    @patch("psycopg2.extensions.cursor")
    def test_create_redshift_database_schema(self, mock_cursor, mock_products, mock_payment_types, mock_orders_products, mock_orders, mock_locations):
        # Set up mock objects
        mock_conn = Mock()
        mock_cursor.return_value = mock_conn
        mock_cursor.connection = mock_conn

        invocation_id = "12345"

        create_redshift_database_schema(mock_cursor, invocation_id)

        # Assert function calls and commit
        mock_locations.assert_called_once_with(mock_cursor, invocation_id)
        mock_orders.assert_called_once_with(mock_cursor, invocation_id)
        mock_orders_products.assert_called_once_with(mock_cursor, invocation_id)
        mock_payment_types.assert_called_once_with(mock_cursor, invocation_id)
        mock_products.assert_called_once_with(mock_cursor, invocation_id)
        mock_conn.commit.assert_called_once()

# # [2/7] ------ [end] Unit Test for create_redshift_database_schema -----------------------------------------


# ######################## END DATABASE #######################################




# #########################   TRANSFORMATION ###################################

# # [1/8] ------ TEST sanatise_csv_order_table ------------------------
from transformation import sanitise_csv_order_table

class TestSanitiseCsvOrderTable(unittest.TestCase):
    @patch("builtins.print")
    def test_sanitise_csv_order_table(self, mock_print):
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
        invocation_id = "12345"
        actual_result = sanitise_csv_order_table(csv_bytes.read().encode(), invocation_id)

        # Check that the column names are as expected
        self.assertEqual(list(actual_result.columns), expected_columns)

        # Check that the data is as expected
        for i, row in enumerate(actual_result.values):
            self.assertEqual(list(row), expected_data[i])

        # Check print statements
        mock_print.assert_any_call(f"sanitise_csv_order_table function started.. , invocation_id = {invocation_id}")
        mock_print.assert_any_call(f"sanitise_csv_order_table function completed. , invocation_id = {invocation_id}")

# # [1/8] ------ [end] TEST sanatise_csv_order_table ------------------------

# # [2/8] ---- Unit test for sort_time_to_postgre_format (We have to be sure that the expected format is YYYY-MM-DD)
from transformation import sort_time_to_postgre_format


def test_sort_time_to_postgre_format():
    with patch("builtins.print") as mock_print:
        # Create mock dataframe
        data = {
            'date_time': ['30/12/2020 09:00'],
            'location': ['London'],
            'transaction_total': [10.0]
        }
        df = pd.DataFrame(data)

        # Define the expected datetime string and datetime object
        expected_datetime_str = '2020-12-30 09:00:00'
        expected_datetime = pd.to_datetime(expected_datetime_str, format='%Y-%m-%d %H:%M:%S')

        # Call the function with the mock dataframe
        invocation_id = "12345"
        sorted_df = sort_time_to_postgre_format(df, invocation_id)

        # Check if the dataframe was sorted correctly
        assert sorted_df['date_time'].iloc[0] == expected_datetime

        # Check print statements
        mock_print.assert_any_call(f"sort_time_to_postgre_format function started.. , invocation_id = {invocation_id}")
        mock_print.assert_any_call(f"sort_time_to_postgre_format function completed. , invocation_id = {invocation_id}")


# # [2/8] --- [end] Unit test for sort_time_to_postgre_format ---------------------------------------


# # [3/8] --- Unit test for Update Locations ---
from transformation import update_locations

class TestUpdateLocations(unittest.TestCase):
    def test_update_locations(self):
        with patch("builtins.print") as mock_print:
            # Create a sample DataFrame with London as a location
            df = pd.DataFrame({
                'date_time': ['2022-05-09 13:00:00'],
                'location': ['London'],
                'transaction_total': [2.40],
                'payment_type': ['CARD']
            })

            # Set up a mock cursor object that returns location IDs
            mock_cursor = MagicMock()
            mock_cursor.fetchone.side_effect = [(1,), None]
            # It will mock the insert and return 1 as the location already exists in the DB

            # Call the function to get the actual result
            invocation_id = "12345"
            actual_result = update_locations(df, mock_cursor, invocation_id)

            # Check that the location names have been replaced with location IDs
            expected_result = pd.DataFrame({
                'date_time': ['2022-05-09 13:00:00'],
                'location': [1],
                'transaction_total': [2.40],
                'payment_type': ['CARD']
            })

            # Check that the shape of the DataFrames is the same
            self.assertEqual(actual_result.shape, expected_result.shape)

            # Check print statements
            mock_print.assert_any_call(f"update_locations function started.., invocation_id = {invocation_id}")
            mock_print.assert_any_call(f"update_locations function completed. invocation_id = {invocation_id}")


# # [3/8] --- [end] Unit test for Update Locations ---


# # [4/8] --- Update Payment Types ----
from transformation import update_payment_types

from transformation import update_locations

class TestUpdateLocations(unittest.TestCase):
    def test_update_locations(self):
        with patch("builtins.print") as mock_print:
            # Create a sample DataFrame with London as a location
            df = pd.DataFrame({
                'date_time': ['2022-05-09 13:00:00'],
                'location': ['London'],
                'transaction_total': [2.40],
                'payment_type': ['CARD']
            })

            # Set up a mock cursor object that returns location IDs
            mock_cursor = MagicMock()
            mock_cursor.fetchone.side_effect = [(1,), None]
            # It will mock the insert and return 1 as the location already exists in the DB

            # Call the function to get the actual result
            invocation_id = "12345"
            actual_result = update_locations(df, mock_cursor, invocation_id)

            # Check that the location names have been replaced with location IDs
            expected_result = pd.DataFrame({
                'date_time': ['2022-05-09 13:00:00'],
                'location': [1],
                'transaction_total': [2.40],
                'payment_type': ['CARD']
            })

            # Check that the shape of the DataFrames is the same
            self.assertEqual(actual_result.shape, expected_result.shape)

            # Check print statements
            mock_print.assert_any_call(f"update_locations function started.., invocation_id = {invocation_id}")
            mock_print.assert_any_call(f"update_locations function completed. invocation_id = {invocation_id}")
# # [4/8] [end] --- Update Payment Types ---

# #[5/8] --- Unit test for Update Orders Table ---
from transformation import update_orders_table

class TestUpdateOrdersTable(unittest.TestCase):
    def test_update_orders_table(self):
        with patch("builtins.print") as mock_print:
            # Define mock data
            mock_df = pd.DataFrame({
                'date_time': ['2022-05-10 12:34:56'],
                'location': [1],
                'transaction_total': [10.0],
                'payment_type': [1]
            })
            mock_cursor = Mock()

            # Call the function
            invocation_id = "12345"
            update_orders_table(mock_df, mock_cursor, invocation_id)

            # Check that the correct SQL statements were executed
            expected_calls = [
                call("INSERT INTO orders (date_time, location_id, transaction_total, payment_type_id) VALUES (%s, %s, %s, %s)",
                     ('2022-05-10 12:34:56', 1, 10.0, 1)),
            ]
            self.assertEqual(mock_cursor.execute.call_args_list, expected_calls)

            # Check print statements
            mock_print.assert_any_call(f"update_orders_table function started.., invocation_id = {invocation_id}")
            mock_print.assert_any_call(f"update_orders_table function completed., invocation_id = {invocation_id}")

#[5/8] [End] --- Test update orders table ----


#[6/8] Unit test for sanatise_csv_for_products

from transformation import sanitise_csv_for_products

class TestSanitiseCSVForProducts(unittest.TestCase):
    def test_sanitise_csv_for_products(self):
        with patch("builtins.print") as mock_print:
            # Define mock data
            raw_csv = b"2022-05-10 12:34:56,London,John Doe,ABC123,10.0,CARD,1234567890"
            invocation_id = "12345"

            # Call the function
            actual_result = sanitise_csv_for_products(raw_csv, invocation_id)

            # Check the sanitized DataFrame
            expected_result = pd.DataFrame({
                'date_time': ['2022-05-10 12:34:56'],
                'location': ['London'],
                'order': ['ABC123'],
                'transaction_total': [10.0],
                'payment_type': ['CARD']
            })
            pd.testing.assert_frame_equal(actual_result, expected_result)

            # Check print statements
            mock_print.assert_any_call(f"sanitise_csv_for_products function started.., invocation_id = {invocation_id}")
            mock_print.assert_any_call(f"sanitise_csv_for_products function completed., invocation_id = {invocation_id}")

# [6/8] [end] Sanatise csv for products

# [7/8] Unit test for update order product table

from transformation import update_order_product_table

# The test function with the necessary changes
class TestUpdateOrderProductTable(unittest.TestCase):

    @patch('transformation.print')
    def test_update_order_product_table(self, mock_print):
        # Define mock data
        mock_df = pd.DataFrame({
            'order': ['Product A - Flavor 1 - 10.99, Product B - 15.99', 'Product C - 20.99']
        })

        # Set up the mock return values for cursor.fetchone
        mock_cursor = MagicMock()
        mock_cursor.fetchone.side_effect = [
            (3,),  # Max order_id
            [('Product A - Flavor 1', 1), ('Product B', 2), ('Product C', 3)]  # product_id_dict
        ]

        # Call the function
        update_order_product_table(mock_df, mock_cursor, invocation_id='12345')

        # Check that the correct SQL statements were executed
        expected_calls = [
            # Expected SELECT statement and result for MAX(order_id)
            (
                call("SELECT MAX(order_id) FROM orders_products"),
                (3,)
            ),
            # Expected SELECT statement and result for product_name and product_id
            (
                call("SELECT product_name, product_id FROM products"),
                [('Product A - Flavor 1', 1), ('Product B', 2), ('Product C', 3)]
            ),
        ]

        # Check that the correct SQL statements were executed
        actual_calls = mock_cursor.execute.call_args_list
        self.assertEqual(len(actual_calls), len(expected_calls))
        for i, (expected_call, expected_result) in enumerate(expected_calls):
            self.assertEqual(actual_calls[i], expected_call)

# [7/8] [end] Unit test for update order product table

#[8/8] Unit Test for Update orders table
from transformation import sanitise_csv_for_products

class TestSanitiseCsvForProducts(unittest.TestCase):

    @patch('transformation.print')
    def test_sanitise_csv_for_products(self, mock_print):
        # Define the raw CSV data
        raw_csv = b'date_time,location,full_name,order,transaction_total,payment_type,card_number\n2022-01-01 09:00:00,Location A,John Doe,Product A,10.99,Credit Card,1234-5678-9012\n2022-01-01 10:00:00,Location B,Jane Smith,Product B,15.99,Cash,9876-5432-1098\n'

        # Call the function
        result = sanitise_csv_for_products(raw_csv, invocation_id='12345')

        # Assert that the function executed successfully
        self.assertIsNotNone(result)

        # Assert that the print statements were called correctly
        mock_print.assert_called_with("sanitise_csv_for_products function completed., invocation_id = 12345")

        # Assert the content of the returned DataFrame
        expected_columns = ['date_time', 'location', 'order', 'transaction_total', 'payment_type']
        expected_data = [
            ['2022-01-01 09:00:00', 'Location A', 'Product A', 10.99, 'CARD'],
            ['2022-01-01 10:00:00', 'Location B', 'Product B', 15.99, 'CASH']
        ]
        expected_df = pd.DataFrame(expected_data, columns=expected_columns,)

#[8/8] [end] Unit Test for Update orders table




############################ END TRANSFORMATION #############################################