import pandas as pd

def save_model(id,result):
    result = pd.DataFrame(result)
    result.to_csv(r'./client/data_storage/model_%s.csv' % id)
    return 0