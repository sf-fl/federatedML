from client.ml import lr


def tarin(x,y,ip,port):
    x['bias'] = 1
    theta, iters = lr.logistic_regression(x, y,ip,port)
    return theta, iters
