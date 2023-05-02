import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

def absolute_path_for_raw_data(raw_data_file):
    abspath = os.path.abspath("./raw_data")
    csv_file = abspath + "\\" + raw_data_file
    return csv_file

raw_data_file = "chesterfield_25-08-2021_09-00-00.csv"

raw_csv = absolute_path_for_raw_data(raw_data_file)

#--------------------------------------------------------

load_dotenv('docker_setup/.env')
host = os.environ.get("sql_host")
user = os.environ.get("sql_user")
password = os.environ.get("sql_pass")
database = os.environ.get("sql_db")
port = os.environ.get("sql_port")

def setup_db_connection(host=host, 
                        user=user, 
                        password=password,
                        db=database,
                        port=port):
    
    print("Connecting to database....")
    conn = psycopg2.connect(
        host = host,
        database = db,
        user = user,
        password = password,
        port = port
    )
    print("Connection established.")
    return conn

conn = setup_db_connection()

#-------------------------------------------------------------------------------------------

#Read and sanitise raw csv
def read_sanitise_csv(raw_csv):
    try:
        columns =  ['date_time', 'location', 'full_name', 'order', 'transaction_total', 'payment_type', 'card_number']  # Headers for the orders csv files
        df = pd.read_csv(raw_csv, header=None, names=columns)
        sanitised_df = df.drop(columns=['full_name', 'card_number'])

    except FileNotFoundError as fnfe:
        print(f'File not found: {fnfe}')

    return sanitised_df

df = read_sanitise_csv(raw_csv)
 
#-----------------------------------------------------------------------------------------------        

def update_location_table(conn, sanitised_data):
    # Extract the unique location names from the raw data
    unique_locations = sanitised_data['location'].unique()

    # Check if each location exists in the database, and insert it if it doesn't
    for location_name in unique_locations:
        # Check if the location already exists in the database
        with conn.cursor() as cur:
            cur.execute('SELECT location_id FROM locations WHERE location_name=%s', (location_name,))
            row = cur.fetchone()

        # If the location doesn't exist, insert it and get the new ID
        if row is None:
            with conn.cursor() as cur:
                cur.execute('INSERT INTO locations (location_name) VALUES (%s) RETURNING location_id', (location_name,))
                location_id = cur.fetchone()[0]
        else:
            location_id = row[0]

    # Commit the changes
    conn.commit()

#print(update_location_table(conn, df))

#-------------------------------------------------------------------------------------