from client.ml import lr
import pandas as pd

def predict(theta,x,y):
    if theta is None:
        pass
    result = lr.predict(theta,x,y)
    result.to_csv('result.csv')
    return result