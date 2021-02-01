from client.ml import lr


def tarin(x,y,ip,port):

    theta, iters = lr.logistic_regression(x, y,ip,port)
    return theta, iters
