from client.proxy import client_proxy
from client.iAo import model_save
from client.federation import alignment
from client.federation import feature_engineering
from client.federation import train
from client.federation import predict
from client.federation import initial
import os
import sys



def start(id,key):

    # 连接测试
    print(client_proxy.test())

    # 对齐模块
    x_raw,y_raw = alignment.align(id,key)

    # 特征工程&预处理
    x,y = feature_engineering.feating(x_raw,y_raw)

    # 训练
    result = train.tarin(x,y)

    # 保存
    model_save.save_model(result)

    # 预测
    pred = predict.predict(result[0],x,y)



if __name__ == '__main__':
    os.chdir(os.path.dirname(sys.path[0]))
    start()
