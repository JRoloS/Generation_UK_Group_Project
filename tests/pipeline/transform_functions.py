import pandas as pd
import json

#Read and sanitise raw csv
def read_sanitise_csv(raw_csv):
    try:
        columns =  ['date_time', 'location', 'full_name', 'order', 'transaction_total', 'payment_type', 'card_number']  # Headers for the orders csv files
        df = pd.read_csv(raw_csv, header=None, names=columns)
        sanitised_df = df.drop(columns=['full_name', 'card_number'])

    except FileNotFoundError as fnfe:
        print(f'File not found: {fnfe}')

    return sanitised_df
        

#Normalise location
def normalise_location(df, db_connection):

    unique_locations = df['location'].unique()

    current_db_locations = get_locations(db_connection) # read locations from DB

    for location in unique_locations:
        if location not in current_db_locations:
            # INSERT LOCATION INTO DB
            # Return ID
        












    # for location in df['location'].unique():
    #     if location not in location_dict:
            
    #         new_location = df.iloc[0].iat[1]
            
    #         if  max(location_dict.values()) == "0":
    #             next_num = 0
            
    #         else:     
    #             next_num = max(location_dict.values()) + 1
            
    #         location_dict[new_location] = next_num
            
    #     df['location'] = df['location'].replace(location_dict)
        


#Normalise orders_products



#Normalise products



#Normalise payment_types


#Normalise orders
#def normalise_orders(raw_csv):
# Select locations and switch locations with ID


# Test -----------------------------------

# df = read_sanitise_csv('chesterfield_25-08-2021_09-00-00.csv')
# location_df = normalise_location(df)
# print(location_df.head())