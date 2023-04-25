# Imports and Variables used for testing
import pandas as pd # Loads Pandas package 
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
import os                                                                                           # For OS related paths 

# Variable List (with their default value [Used in Testing])
raw_data_file = "chesterfield_25-08-2021_09-00-00.csv"                                              # Csv filename on the raw_data subfolder
csv = ""                                                                                            # filepath to be read by functions, used after joint with raw_data_file NOTE: csv variable could be an url if needed
df = ""                                                                                             # Global for the DataFrame
count = ""                                                                                          # Global for count functions
column = "order"                                                                             # Argument for functions
value = "CARD"                                                                                      # Argument for functions
columns = ['date_time', 'Location', 'full_name', 'order', 'amount', 'payment_type', 'card_number']  # Headers for the orders csv files
sanitise_these_columns = ['date_time', 'Location', 'full_name', 'amount', 'payment_type', 'card_number']                                               # Columns list to be sanitised
path = "results/"                                                                                   # to add folder/subfolder/ if needed
newfile = "newfile.csv"                                                                             # Filename to be created by the Create CSV/JSON function

def absolute_path_for_raw_data(raw_data_file):
    abspath = os.path.abspath("../raw_data")
    global csv
    csv = abspath + "\\" + raw_data_file
    
absolute_path_for_raw_data(raw_data_file)

# 2. Extract Sanitise CSV Function [Remove given Columns]
def extract_sanitise_csv(csv,sanitise_these_columns):
    try:
        global df # as Global to be able to print it outside the function
        df = pd.read_csv(csv, header=None, names=columns)
        df = df.drop(columns=sanitise_these_columns)
    except FileNotFoundError as fnfe:
        print(f'File not found: {fnfe}')

    return df

extract_sanitise_csv(csv,sanitise_these_columns)

def filter_by_column_value(csv,column,value):
    try:
        global contain_values # as Global to be able to print it outside the function
        contain_values = df[df[column].str.contains(value.upper())]
    except FileNotFoundError as fnfe:
        print(f'File not found: {fnfe}')

    return contain_values

filter_by_column_value(csv,column,value)

def count_number_of_times_a_value_is_repeated(csv,column,value):
    try:
        df = pd.read_csv(csv, header=None, names=columns)
        global count # as Global to be able to print it outside the function
        count = df[column].value_counts()[value]
    except FileNotFoundError as fnfe:
         print(f'File not found: {fnfe}')
    return count

count_number_of_times_a_value_is_repeated(csv,column,value)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df)

