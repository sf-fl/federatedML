from client.ml import lr


def tarin(x,y,ip,port,id):
    x['bias'] = 1
    theta, iters = lr.logistic_regression(x, y,ip,port,id)
    return theta, iters
