import pandas as pd
import io

#-----------------------------------------------------------------
# [1] Read and sanitise raw csv

# ****DROPS [FULL_NAME], [ORDER] AND [CARD_NUMBER] ONLY****

def sanitise_csv_order_table(raw_csv, invocation_id):
    print(f'sanitise_csv_order_table function started.. , invocation_id = {invocation_id}')
    try:
        columns =  ['date_time', 'location', 'full_name', 'order', 'transaction_total', 'payment_type', 'card_number']  # Headers for the orders csv files
        df = pd.read_csv(io.BytesIO(raw_csv), header=None, names=columns)
        sanitised_df = df.drop(columns=['full_name', 'order', 'card_number'])
        print(f'sanitise_csv_order_table function completed. , invocation_id = {invocation_id}')

    except FileNotFoundError as fnfe:
        print(f'sanitise_csv_order_table function, File not found: {fnfe}, , invocation_id = {invocation_id}')

    return sanitised_df

#-----------------------------------------------------------------------------------------------
# [2] Changes date/time format to postgreSQL format (yyyy/mm/dd)

def sort_time_to_postgre_format(df, invocation_id):
    print(f'sort_time_to_postgre_format function started.. , invocation_id = {invocation_id}')
    try:
        df['date_time'] = pd.to_datetime(df['date_time'], dayfirst=True)
        print(f'sort_time_to_postgre_format function completed. , invocation_id = {invocation_id}')
        
    except Exception as error:
        print(f'sort_time_to_postgre_format function error changing date/time format: {error}, invocation_id = {invocation_id}')
    
    return df

#-----------------------------------------------------------------------------------------------

# [3] Checks to see if dataframe value (location) is first within the target table (locations), if not then inserts value and returns value ID, replaces the value within the original dataframe:

def update_locations(sanitised_df, cursor, invocation_id):
    print(f'update_locations function started.., invocation_id = {invocation_id}')
    try:
    # Get the distinct location names from the sanitized dataframe
        location_names = sanitised_df['location'].unique()

        # Check each location name against the locations table in the database
        for name in location_names:
            cursor.execute("SELECT location_id FROM locations WHERE location_name = %s", (name,))
            result = cursor.fetchone()

            # If the location name is not in the table, insert it and update the associated column within the dataframe with the returned location_id
            if result is None:
                cursor.execute("INSERT INTO locations (location_name) VALUES (%s)", (name,))
                cursor.connection.commit()
                cursor.execute("SELECT location_id FROM locations WHERE location_name = (%s)", (name,))
                location_id = cursor.fetchone()[0]
            else:
                location_id = result[0]
                
            sanitised_df.loc[sanitised_df['location'] == name, 'location'] = location_id
        
        print(f'update_locations function completed. invocation_id = {invocation_id}')

        return sanitised_df

    except Exception as error:
        print(f'update_locations function error updating locations: {error}, invocation_id = {invocation_id}')

#-------------------------------------------------------------------------------------------------------------------

# [4] Checks to see if dataframe value (payment_type_name) is first within the target table (payment_types), if not then inserts value and returns value ID, replaces the value within the original dataframe:

def update_payment_types(sanitised_df, cursor, invocation_id):
    print(f'update_payment_types function started.., invocation_id = {invocation_id}')
    try:
        # Get the distinct payment names from the sanitized dataframe
        payment_types = sanitised_df['payment_type'].unique()

        # Check each payment name against the payment_type table in the database
        for name in payment_types:
            cursor.execute("SELECT * FROM payment_types WHERE payment_name = %s", (name,))
            result = cursor.fetchone()

            # If the payment name is not in the table, insert it
            if result is None:
                cursor.execute("INSERT INTO payment_types (payment_name) VALUES (%s)", (name,))
                cursor.connection.commit()
                cursor.execute("SELECT payment_type_id FROM payment_types WHERE payment_name = (%s)", (name,))
                payment_type_id = cursor.fetchone()[0]
            else:
                payment_type_id = result[0]

            # Update the payment_type column in the dataframe with the payment_type_id
            sanitised_df.loc[sanitised_df['payment_type'] == name, 'payment_type'] = payment_type_id

        print(f'update_payment_types function completed., invocation_id = {invocation_id}')
        
        return sanitised_df
    
    except Exception as error:
        print(f'update_payment_types function error updating payment_types: {error}, invocation_id = {invocation_id}')



#-------------------------------------------------------------------------------------------------------------------

# [5] After original dataframe is normalised with replaced values from "update_locations" & "update_payment_types", inserts all values per row into "orders" table in the database:

def update_orders_table(sanitised_df, cursor, invocation_id):
    print(f'update_orders_table function started.., invocation_id = {invocation_id}')
    try:
        # Iterate over each row in the DataFrame
        for index, row in sanitised_df.iterrows():
            date_time = row['date_time']
            location = row['location']
            transaction_total = row['transaction_total']
            payment_type = row['payment_type']
            
            # Check if the order already exists in the table
            cursor.execute("INSERT INTO orders (date_time, location_id, transaction_total, payment_type_id) VALUES (%s, %s, %s, %s)", (date_time, location, transaction_total, payment_type))
            cursor.connection.commit()
            
        print(f'update_orders_table function completed., invocation_id = {invocation_id}')
        
    except Exception as error:
        print(f'update_orders_table function error orders: {error}, invocation_id = {invocation_id}')

#-------------------------------------------------------------------------------

# [6] Read and sanitise raw csv - This time to transform and populate "products" & "orders_products" tables in database:

# ****DROPS [FULL_NAME] AND [CARD_NUMBER] ONLY

def sanitise_csv_for_products(raw_csv, invocation_id):
    print(f'sanitise_csv_for_products function started.., invocation_id = {invocation_id}')
    try:
        columns =  ['date_time', 'location', 'full_name', 'order', 'transaction_total', 'payment_type', 'card_number']  # Headers for the orders csv files
        df = pd.read_csv(io.BytesIO(raw_csv), header=None, names=columns)
        sanitised_df = df.drop(columns=['full_name', 'card_number'])
        print(f'sanitise_csv_for_products function completed., invocation_id = {invocation_id}')

    except FileNotFoundError as fnfe:
        print(f'sanitise_csv_for_products function, File not found: {fnfe}, invocation_id = {invocation_id}')

    return sanitised_df

#--------------------------------------------------------------------------------------

# [7] Iterates through the "order" column within dataframe and seperates multiple products into individuals with their prices, inserts only product names into "products" table:

def update_product_table(sanitised_df, cursor, invocation_id):
    print(f'update_product_table function started.., invocation_id = {invocation_id}')
    try:
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
                    cursor.execute("INSERT INTO products (product_name) VALUES (%s)", (product_name,))
                    cursor.connection.commit()
                    # cursor.execute("SELECT product_id FROM products WHERE product_name = (%s)", (product_name,))
                    # result = cursor.fetchone()

        print(f'update_product_table function completed., invocation_id = {invocation_id}')
        
    except Exception as error:
        print(f'update_product_table function error updating products: {error}, invocation_id = {invocation_id}')
    
#------------------------------------------------------------------------------------------

# [8] Finally, inserts both "order_id" & "product_id" as well as "price" into "orders_products" database table, foreign key constraints will link them up accordingly: 

def update_order_product_table(sanitised_df, cursor, invocation_id):
    print(f'update_order_product_table function started.., invocation_id = {invocation_id}')
    try:
        # Get the current max order_id in the "orders_products" table
        cursor.execute("SELECT MAX(order_id) FROM orders_products")
        max_order_id = cursor.fetchone()[0]
        if max_order_id is None:
            max_order_id = 0
        # Get the product names and their associated ids from the "products" table
        cursor.execute("SELECT product_name, product_id FROM products")
        product_id_dict = dict(cursor.fetchall())
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
                cursor.execute("INSERT INTO orders_products (order_id, product_id, product_price) VALUES (%s, %s, %s)", (order_id, product_id, product_price))
                cursor.connection.commit()
        
        print(f'update_order_product_table function completed., invocation_id = {invocation_id}')
    
    except Exception as error:
        print(f'update_order_product_table function error updating orders_products: {error}, invocation_id = {invocation_id}')
 
