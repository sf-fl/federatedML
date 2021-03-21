from client.ml import lr,show
import pandas as pd

def predict(theta,x,y,id,ip,port):
    if theta is None:
        pass
    if 'bias' not in x.columns:
        x['bias'] = 1
    result = lr.predict(theta,x,y,ip,port)
    result.to_csv('result.csv')
    return result

def calculate(pred,y):
    auc,ks = show.evaluate(pred,y)
    return auc,ks