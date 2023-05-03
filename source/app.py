import psycopg2
import pandas as pd
import os
import json
from dotenv import load_dotenv

#---------------------------------------------------------------

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

# def update_location_table(conn, sanitised_data):
#     # Extract the unique location names from the raw data
#     unique_locations = sanitised_data['location'].unique()

#     # Check if each location exists in the database, and insert it if it doesn't
#     for location_name in unique_locations:
#         # Check if the location already exists in the database
#         with conn.cursor() as cur:
#             cur.execute('SELECT location_id FROM locations WHERE location_name=%s', (location_name,))
#             row = cur.fetchone()

#         # If the location doesn't exist, insert it and get the new ID
#         if row is None:
#             with conn.cursor() as cur:
#                 cur.execute('INSERT INTO locations (location_name) VALUES (%s) RETURNING location_id', (location_name,))
#                 location_id = cur.fetchone()[0]
#         else:
#             location_id = row[0]

#     # Commit the changes
#     conn.commit()

#print(update_location_table(conn, df))

#-------------------------------------------------------------------------------------

def update_locations(sanitized_df, conn):
    # Create a cursor to interact with the database
    cur = conn.cursor()

    # Get the distinct location names from the sanitized dataframe
    location_names = sanitized_df['location'].unique()

    # Check each location name against the locations table in the database
    for name in location_names:
        cur.execute("SELECT * FROM locations WHERE location_name = %s", (name,))
        result = cur.fetchone()

        # If the location name is not in the table, insert it
        if result is None:
            cur.execute("INSERT INTO locations (location_name) VALUES (%s) RETURNING location_id", (name,))

    # Commit the changes to the database and close the cursor
    conn.commit()
    cur.close()

#update_locations(df, conn)

#-------------------------------------------------------------------------------------

def update_payment_types(sanitized_df, conn):
    # Create a cursor to interact with the database
    cur = conn.cursor()

    # Get the distinct payment names from the sanitized dataframe
    payment_types = sanitized_df['payment_type'].unique()

    # Check each payment name against the payment_type table in the database
    for name in payment_types:
        cur.execute("SELECT * FROM payment_types WHERE payment_name = %s", (name,))
        result = cur.fetchone()

        # If the payment name is not in the table, insert it
        if result is None:
            cur.execute("INSERT INTO payment_types (payment_name) VALUES (%s) RETURNING payment_type_id", (name,))

    # Commit the changes to the database and close the cursor
    conn.commit()
    cur.close()

#update_payment_types(df, conn)

#---------------------------------------------------------------------

# def split_products_from_order(sanitized_df):
#     product_list = []
#     for i, order in enumerate(df['order']):
#         order_split = order.split(', ')
#         product_dict = {}
#         for item in order_split:
#             item_split = item.split(' - ')
#             product = item_split[0].strip() + item_split[1].strip()
#             price = item_split[-1]
#             product_dict[product] = price
#         product_list.append(product_dict)
#     #return product_list
    
#     print(product_list)
    
# split_products_from_order(df)

#-------------------------------------------------------------------------------------


# def seperate_products_list(product_list):
#     for products in product_list:
#         print(products)
#         #for product_name, product_price in products.items():
            
            
# seperate_products_list(split_products_from_order(df))

#---------------------------------------------------------

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

#update_product_table(df, conn)

#---------------------------------------------------------

def split_prices_per_product(sanitised_df):

    for index, row in sanitised_df.iterrows():
            order_string = row['order']
            # Split the order string into individual orders
            orders = order_string.split(', ')
            # Iterate over each order
            for order in orders:
                    product_price = order.split(' - ')[-1].strip()
        
            print(product_price)


split_prices_per_product(df)  

# Go through CSV[orders] again
# create a new order
# split string again and match product name to ID in products table
# Return ID
# Use associated price from  


# Possible implementation for updating Orders_products table

def update_order_product_table(sanitised_df, conn):
    # Create a cursor object
    cur = conn.cursor()
    
    # Get the product names and their associated ids from the "products" table
    cur.execute("SELECT product_name, product_id FROM products")
    product_id_dict = dict(cur.fetchall())
    
    # Iterate through each order in the dataframe and insert its products into the "orders_products" table
    for i, order in sanitised_df.iterrows():
        # Split the order string into a list of individual product strings
        products = order['order'].split(', ')
        
        # Assign an order_id to this order
        order_id = i + 1
        
        # Iterate through each product in this order and insert it into the "orders_products" table
        for product in products:
            # Split the product string into its name, flavour (if present), and price components
            product_components = product.split(' - ')
            product_name = product_components[0].strip()
            if len(product_components) == 3:
                product_name += ' - ' + product_components[1].strip()
            product_price = float(product_components[-1].strip())
            
            # Get the product_id for this product from the "products" table
            product_id = product_id_dict[product_name]
            
            # Insert the order_id, product_id, and product_price into the "orders_products" table
            cur.execute("INSERT INTO orders_products (order_id, product_id, product_price) VALUES (%s, %s, %s)", (order_id, product_id, product_price))
    
    # Commit the changes and close the cursor
    conn.commit()
    cur.close()


     