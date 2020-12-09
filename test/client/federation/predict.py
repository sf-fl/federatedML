from client.ml import lr


def predict(theta,x,y):
    if theta is None:
        pass
    result = lr.predict(theta,x,y)
    with open('temp','a+') as f1:
        f1.write(result)
    return result