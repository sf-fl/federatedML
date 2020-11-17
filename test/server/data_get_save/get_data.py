import pandas as pd

key='phone_num'

def get_data_key():
    data = pd.read_csv('./data_storage/data.csv')
    key_word = data[key]
    return key_word