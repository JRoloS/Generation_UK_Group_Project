from absolute_local_path import absolute_path_for_raw_data
from transformation import sanitise_csv_order_table, sort_time_to_postgre_format, update_locations, update_payment_types, update_orders_table, sanitise_csv_for_products, update_product_table, update_order_product_table
from database import setup_db_connection

#---------------------------------------------------------------
# Below variable is linked to a function that would locally read a csv from the computer:

raw_data_file = "chesterfield_25-08-2021_09-00-00.csv"
#raw_data_file = "leeds_01-01-2020_09-00-00.csv"

raw_csv = absolute_path_for_raw_data(raw_data_file)


# Variable used to connect to database
conn = setup_db_connection()

#-------ETL PIPELINE BELOW--------------------------------------------------------------------------

# [1] Read and sanitise raw csv - ****DROPS [FULL_NAME], [ORDER] AND [CARD_NUMBER] ONLY****

order_table_df = sanitise_csv_order_table(raw_csv)

# [2] Changes date/time format to postgreSQL format (yyyy/mm/dd)

sorted_datetime_df = sort_time_to_postgre_format(order_table_df)

# [3] Checks to see if dataframe value (location) is first within the target table (locations), if not then inserts value and returns value ID, replaces the value within the original dataframe:      
    
normalised_location_df = update_locations(sorted_datetime_df, conn)

# [4] Checks to see if dataframe value (payment_type_name) is first within the target table (payment_types), if not then inserts value and returns value ID, replaces the value within the original dataframe:

normalised_payment_type_df = update_payment_types(normalised_location_df, conn)

# [5] After original dataframe is normalised with replaced values from "update_locations" & "update_payment_types", inserts all values per row into "orders" table in the database:

update_orders_table(normalised_payment_type_df, conn)

# [6] Read and sanitise raw csv - This time to transform and populate "products" & "orders_products" tables in database:
# ****DROPS [FULL_NAME] AND [CARD_NUMBER] ONLY****

general_df = sanitise_csv_for_products(raw_csv)

# [7] Iterates through the "order" column within dataframe and seperates multiple products into individuals with their prices, inserts only product names into "products" table:

update_product_table(general_df, conn)

# [8] Finally, inserts both "order_id" & "product_id" as well as "price" into "orders_products" database table, foreign key constraints will link them up accordingly: 

update_order_product_table(general_df, conn)

#-------------------------------------------------------------------------------------------


