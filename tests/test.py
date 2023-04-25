import pandas as pd
import os

def absolute_path_for_raw_data(raw_data_file):
    abspath = os.path.abspath("../raw_data")
    global csv
    csv = abspath + "\\" + raw_data_file

raw_data_file = "chesterfield_25-08-2021_09-00-00.csv"

absolute_path_for_raw_data(raw_data_file)
print(csv) # Prints the newly formed absolute path with the raw_data_file name given.

#-------------------------------------------------------------------------------------
def extract_sanitise_csv(csv,sanitise_these_columns):
    try:
        global df # as Global to be able to print it outside the function
        df = pd.read_csv(csv, header=None, names=columns)
        df = df.drop(columns=sanitise_these_columns)
    except FileNotFoundError as fnfe:
        print(f'File not found: {fnfe}')

    return df


columns = ['date_time', 'Location', 'full_name', 'order', 'amount', 'payment_type', 'card_number']  # Headers for the orders csv files

sanitise_these_columns = ['full_name', 'card_number']

extract_sanitise_csv(csv,sanitise_these_columns)

#--------------------------------------------------------------------------------------

def count_number_of_different_values(csv,column):
    try:
        global count  # as Global to be able to print it outside the function
        count = df[column].value_counts(ascending=True)
    except FileNotFoundError as fnfe:
         print(f'File not found: {fnfe}')
    return count

column = "order" 

count_number_of_different_values(csv,column)
# print(count)

def get_unique_products_in_orders():
    # df = pd.read_csv(csv, header=None, names=columns)  # Not needed if you're coming from another function that already read this
    orders = df['order'].str.split(',', expand = True)
        
    for item in orders:
        global result
        result = orders[item].unique()

    return result 

get_unique_products_in_orders()
print(result)
