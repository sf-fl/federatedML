from proxy import client_proxy
from data_get_save import model_save
from federation import alignment
from federation import feature_engineering
from federation import train

def start():
    # 连接测试
    print(client_proxy.test())

    # 对齐模块
    x_raw,y_raw = alignment.align()

    # 特征工程&预处理
    x,y = feature_engineering.feating(x_raw,y_raw)

    # 训练
    result = train.tarin(x,y)

    # 保存
    model_save.save_model(result)


if __name__ == '__main__':
    start()