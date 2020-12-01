import pandas as pd

def feating(x_raw):
    x_oh = pd.get_dummies(x_raw)

    return x_oh