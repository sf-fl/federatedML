from client.ml import lr
import pandas as pd

def predict(theta,x,y,id,ip,port):
    if theta is None:
        pass
    if 'bias' not in x.columns:
        x['bias'] = 1
    result = lr.predict(theta,x,y,ip,port)
    result.to_csv('result.csv')
    return result