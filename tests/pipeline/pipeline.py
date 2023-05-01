# SYSTEMATIC HIERARCHY INTENDED TRANSFORMATION 
# ---->  or how I prefer to call it: The S.H.I.T.

# IMPORTS

import os
import pandas as pd


# (1) Reads a file (the lambda trigger must return the csv variable with the filename)
csv_file = 'chesterfield_25-08-2021_09-00-00.csv'

def read_file_and_add_indexes():
    columns = ['date_time', 'location', 'full_name', 'order', 'transaction_total', 'payment_type', 'card_number']  # Headers for the orders csv files
    df = pd.read_csv(csv_file, header=None, names=columns)
    return df

# Called as:
df = read_file_and_add_indexes()

# (2) Sanatise the full_name and card_number rows 

def sanitise_csv(df):
    try:
        df = df.drop(columns=['full_name', 'card_number'])
    except FileNotFoundError as fnfe:
        print(f'File not found: {fnfe}')

    return df

# Called as:
df = sanitise_csv(df)


# (3) Change date format to PostgreSQL standard

def sort_time_to_postgre_format(df):
    df['date_time'] = pd.to_datetime(df['date_time'], dayfirst=True)
    
    return df

# Called as:
df = sort_time_to_postgre_format(df)



# (4) Replace Location with Dictionary ones, Add location to the Dictionary if it is a new one


print(df)
