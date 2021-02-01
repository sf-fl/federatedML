import pandas as pd
import os

key = 'phone_num'

def get_data(id):
    data = pd.read_csv('%s/server/data_storage/data_%s.csv' % (os.getcwd(),id))
    return data