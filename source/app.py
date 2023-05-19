#from absolute_local_path import absolute_path_for_raw_data [LOCAL TESTING ONLY]
from transformation import sanitise_csv_order_table, sort_time_to_postgre_format, update_locations, update_payment_types, update_orders_table, sanitise_csv_for_products, update_product_table, update_order_product_table
from database import setup_db_connection, create_redshift_database_schema
import boto3
import json
import logging

#logger = logging.getLogger(__name__)

def lambda_handler(event, context):
    invocation_id = context.aws_request_id
    print(f"lambda_handler started: invocation_id = {invocation_id}")
    s3 = boto3.client('s3')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    print(f'lambda_handler bucket = {bucket}, key = {key}, invocation_id = {invocation_id}')
    ssm_client = boto3.client('ssm')
    parameter_details = ssm_client.get_parameter(Name='brewed-awakening-redshift-settings')
    redshift_details = json.loads(parameter_details['Parameter']['Value'])
    print(f"lambda_handler redshift_details = {redshift_details['host']}, invocation_id = {invocation_id}")
    
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print(f'lambda_handler s3 response = {response}, invocation_id = {invocation_id}')
        content = response['Body'].read()
# jkasnjsnasnlfsjan
#-----------------------------------------------------------------------------------------
# Below variable is linked to a function that would LOCALLY read a csv from the computer:

        #raw_data_file = "chesterfield_25-08-2021_09-00-00.csv"
#raw_data_file = "leeds_01-01-2020_09-00-00.csv"

        #raw_csv = absolute_path_for_raw_data(raw_data_file)
        
#-------------------------------------------------------------------------------------------

# Variable used to connect to a (Redshift) database
        conn = setup_db_connection(host=redshift_details['host'], 
                        user=redshift_details['user'], 
                        password=redshift_details['password'],
                        db=redshift_details['database-name'],
                        port=redshift_details['port'],
                        invocation_id=invocation_id)
        
        print(f'lambda_handler connection started.. invocation_id = {invocation_id}')
        
        cursor = conn.cursor()
        
        #[!] This function runs all database table create functions from "database.py" and if the tables already exist then will not overwrite: 
        
        create_redshift_database_schema(cursor, invocation_id)

#-------ETL PIPELINE BELOW--------------------------------------------------------------------------

# [1] Read and sanitise raw csv - ****DROPS [FULL_NAME], [ORDER] AND [CARD_NUMBER] ONLY****

        order_table_df = sanitise_csv_order_table(content, invocation_id)

# [2] Changes date/time format to postgreSQL format (yyyy/mm/dd)

        sorted_datetime_df = sort_time_to_postgre_format(order_table_df, invocation_id)

# [3] Checks to see if dataframe value (location) is first within the target table (locations), if not then inserts value and returns value ID, replaces the value within the original dataframe:      
    
        normalised_location_df = update_locations(sorted_datetime_df, cursor, invocation_id)

# [4] Checks to see if dataframe value (payment_type_name) is first within the target table (payment_types), if not then inserts value and returns value ID, replaces the value within the original dataframe:

        normalised_payment_type_df = update_payment_types(normalised_location_df, cursor, invocation_id)

# [5] After original dataframe is normalised with replaced values from "update_locations" & "update_payment_types", inserts all values per row into "orders" table in the database:

        update_orders_table(normalised_payment_type_df, cursor, invocation_id)

# [6] Read and sanitise raw csv - This time to transform and populate "products" & "orders_products" tables in database:
# ****DROPS [FULL_NAME] AND [CARD_NUMBER] ONLY****

        general_df = sanitise_csv_for_products(content, invocation_id)

# [7] Iterates through the "order" column within dataframe and seperates multiple products into individuals with their prices, inserts only product names into "products" table:

        update_product_table(general_df, cursor, invocation_id)

# [8] Finally, inserts both "order_id" & "product_id" as well as "price" into "orders_products" database table, foreign key constraints will link them up accordingly: 

        update_order_product_table(general_df, cursor, invocation_id)
    
        #[!] Commit changes at the end then close the connection:
        print(f"lambda_handler commiting, invocation_id = {invocation_id}")
        conn.commit()
        print(f"lambda_handler successfully commited, invocation_id = {invocation_id}")
        cursor.close()
        print(f"lambda_handler successfully closed, invocation_id = {invocation_id}")
          
    except Exception as error:
        print('Error has occured in lambda_handler: ' + str(error) + f'invocation_id = {invocation_id}')

#-------------------------------------------------------------------------------------------
        
