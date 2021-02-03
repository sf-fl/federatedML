import pandas as pd
from client.proxy import client_proxy

def save_model(result,id,ip,port):
    client_proxy.save(id, ip, port)
    model = result[0]
    iter = result[1]
    model.to_csv(r'./client/data_storage/model_%s.csv' % id)
    return 0