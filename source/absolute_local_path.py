import os

def absolute_path_for_raw_data(raw_data_file):
    abspath = os.path.abspath("./raw_data")
    csv_file = abspath + "\\" + raw_data_file
    return csv_file
