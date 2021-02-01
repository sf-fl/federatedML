import pandas as pd

def save_model(result):
    result = pd.DataFrame(result)
    result.to_csv(r'./server/data_storage/model_%s.csv' % id)
    return 0