import pandas as pd
import os



def get_data(id):
    data = pd.read_csv('%s/client/data_storage/data_%s.csv' % (os.getcwd(),id))
    return data