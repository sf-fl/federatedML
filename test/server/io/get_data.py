import pandas as pd
import os
key = 'phone_num'

def get_data_key():
    data = pd.read_csv('%s/server/data_storage/data.csv' % os.getcwd())
    key_word = data[key]
    return data,key_word