import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

#---------------------------------------------------------------

def absolute_path_for_raw_data(raw_data_file):
    abspath = os.path.abspath("./raw_data")
    csv_file = abspath + "\\" + raw_data_file
    return csv_file

#raw_data_file = "chesterfield_25-08-2021_09-00-00.csv"
raw_data_file = "leeds_01-01-2020_09-00-00.csv"

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

# ****DROPS [FULL_NAME], [ORDER] AND [CARD_NUMBER] ONLY

def sanitise_csv_order_table(raw_csv):
    try:
        columns =  ['date_time', 'location', 'full_name', 'order', 'transaction_total', 'payment_type', 'card_number']  # Headers for the orders csv files
        df = pd.read_csv(raw_csv, header=None, names=columns)
        sanitised_df = df.drop(columns=['full_name', 'order', 'card_number'])

    except FileNotFoundError as fnfe:
        print(f'File not found: {fnfe}')

    return sanitised_df

order_table_df = sanitise_csv_order_table(raw_csv)

#print(df)

#-----------------------------------------------------------------------------------------------

def sort_time_to_postgre_format(df):
    df['date_time'] = pd.to_datetime(df['date_time'], dayfirst=True)
    
    return df

sorted_datetime_df = sort_time_to_postgre_format(order_table_df)

#-----------------------------------------------------------------------------------------------        

def update_locations(sanitised_df, conn):
    # Create a cursor to interact with the database
    cur = conn.cursor()

    # Get the distinct location names from the sanitized dataframe
    location_names = sanitised_df['location'].unique()

    # Check each location name against the locations table in the database
    for name in location_names:
        cur.execute("SELECT location_id FROM locations WHERE location_name = %s", (name,))
        result = cur.fetchone()

        # If the location name is not in the table, insert it and update the associated column within the dataframe with the returned location_id
        if result is None:
            cur.execute("INSERT INTO locations (location_name) VALUES (%s) RETURNING location_id", (name,))
            location_id = cur.fetchone()[0]
            sanitised_df.loc[sanitised_df['location'] == name, 'location'] = location_id

    # Commit the changes to the database and close the cursor
    conn.commit()
    cur.close()
    return sanitised_df
    
normalised_location_df = update_locations(sorted_datetime_df, conn)

#-------------------------------------------------------------------------------------

def update_payment_types(sanitised_df, conn):
    # Create a cursor to interact with the database
    cur = conn.cursor()

    # Get the distinct payment names from the sanitized dataframe
    payment_types = sanitised_df['payment_type'].unique()

    # Check each payment name against the payment_type table in the database
    for name in payment_types:
        cur.execute("SELECT * FROM payment_types WHERE payment_name = %s", (name,))
        result = cur.fetchone()

        # If the payment name is not in the table, insert it
        if result is None:
            cur.execute("INSERT INTO payment_types (payment_name) VALUES (%s) RETURNING payment_type_id", (name,))
            payment_type_id = cur.fetchone()[0]
        else:
            payment_type_id = result[0]

        # Update the payment_type column in the dataframe with the payment_type_id
        sanitised_df.loc[sanitised_df['payment_type'] == name, 'payment_type'] = payment_type_id

    # Commit the changes to the database and close the cursor
    conn.commit()
    cur.close()
    return sanitised_df
    

normalised_payment_type_df = update_payment_types(normalised_location_df, conn)
#print(normalised_payment_type_df)

#------------------------------------------------------------------------------

def update_orders_table(sanitised_df, conn):
    # Create a cursor object to interact with the database
    cursor = conn.cursor()
    
    # Iterate over each row in the DataFrame
    for index, row in sanitised_df.iterrows():
        date_time = row['date_time']
        location = row['location']
        transaction_total = row['transaction_total']
        payment_type = row['payment_type']
        
        # Check if the order already exists in the table
        cursor.execute("INSERT INTO orders (date_time, location_id, transaction_total, payment_type_id) VALUES (%s, %s, %s, %s)", (date_time, location, transaction_total, payment_type))

    # Commit the changes to the database
    conn.commit()
    
    # Close the cursor
    cursor.close()
    
update_orders_table(normalised_payment_type_df, conn)

#-------------------------------------------------------------------------------

#Read and sanitise raw csv

# ****DROPS [FULL_NAME] AND [CARD_NUMBER] ONLY

def read_sanitise_csv(raw_csv):
    try:
        columns =  ['date_time', 'location', 'full_name', 'order', 'transaction_total', 'payment_type', 'card_number']  # Headers for the orders csv files
        df = pd.read_csv(raw_csv, header=None, names=columns)
        sanitised_df = df.drop(columns=['full_name', 'card_number'])

    except FileNotFoundError as fnfe:
        print(f'File not found: {fnfe}')

    return sanitised_df

general_df = read_sanitise_csv(raw_csv)

#----------------------------------------------------------------------------------

def update_product_table(sanitised_df, conn):
    # Create a cursor object to interact with the database
    cursor = conn.cursor()
    # Iterate over each row in the DataFrame
    for index, row in sanitised_df.iterrows():
        order_string = row['order']
        # Split the order string into individual orders
        orders = order_string.split(', ')
        # Iterate over each order
        for order in orders:
            if order.count('-') == 1:
                product_name = order.split(' - ')[0].strip()
            
            else:
                product_name = f"{order.split(' - ')[0].strip()} - {order.split(' - ')[1].strip()}"
            
            # Check if the product already exists in the table
            cursor.execute("SELECT product_id FROM products WHERE product_name = %s", (product_name,))
            result = cursor.fetchone()
            if result is None:
                # If the product does not exist, insert it into the table
                cursor.execute("INSERT INTO products (product_name) VALUES (%s) RETURNING product_id", (product_name,))
    conn.commit()
    # Close the cursor
    cursor.close()

update_product_table(general_df, conn)

#------------------------------------------------------------------------------------------

def update_order_product_table(sanitised_df, conn):
    # Create a cursor object
    cur = conn.cursor()
    # Get the current max order_id in the "orders_products" table
    cur.execute("SELECT MAX(order_id) FROM orders_products")
    max_order_id = cur.fetchone()[0]
    if max_order_id is None:
        max_order_id = 0
    # Get the product names and their associated ids from the "products" table
    cur.execute("SELECT product_name, product_id FROM products")
    product_id_dict = dict(cur.fetchall())
    # Iterate through each order in the dataframe and insert its products into the "orders_products" table
    for i, order in sanitised_df.iterrows():
        # Split the order string into a list of individual product strings
        products = order['order'].split(', ')
        # Assign an order_id to this order
        order_id = max_order_id + i + 1
        # Iterate through each product in this order and insert it into the "orders_products" table
        for j, product in enumerate(products):
            # Split the product string into its name, flavour (if present), and price components
            product_components = product.split(' - ')
            product_name = product_components[0]
            if len(product_components) == 3:
                product_name += ' - ' + product_components[1]
            product_price = float(product_components[-1])
            # Get the product_id for this product from the "products" table
            product_id = product_id_dict[product_name]
            # Insert the order_id, product_id, and product_price into the "orders_products" table
            cur.execute("INSERT INTO orders_products (order_id, product_id, product_price) VALUES (%s, %s, %s)", (order_id, product_id, product_price))
    # Commit the changes and close the cursor
    conn.commit()
    cur.close()

update_order_product_table(general_df, conn)

#-------------------------------------------------------------------------------------------


