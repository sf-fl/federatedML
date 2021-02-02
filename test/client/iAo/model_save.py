import pandas as pd

def save_model(result,id):
    model = result[0]
    iter = result[1]
    model.to_csv(r'./client/data_storage/model_%s.csv' % id)
    return 0