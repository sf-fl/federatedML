import copy

def feating(x_raw,y_raw):
    args = x_raw.describe()
    x = copy.deepcopy(x_raw)
    for i in range(x_raw.shape[1]):
        xi = x_raw.iloc[:,i]
        max = xi.max()
        min = xi.min()
        x.iloc[:,i] = x.iloc[:,i].apply(lambda xx: int((xx - min) / (max - min) * 100 // 1))
    y = y_raw.apply(lambda yy : yy*2-1)
    return x,y