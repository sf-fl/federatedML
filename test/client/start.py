from client.proxy import client_proxy
from client.iAo import model_save
from client.federation import alignment
from client.federation import feature_engineering
from client.federation import train
from client.federation import predict
from client.federation import tools
from client.federation import initial
from client.iAo import FetchAndQuery as FAQ
import os
import sys

def write_step(id, step):
    with open(r'./client/data_storage/train_step_%s.log' % id, 'w', encoding='UTF-8') as f1:
        f1.write(str(step))


def start(id,ip,port,key):
    tools.write_detail(id,'','w')
    write_step(id,1)
    taskinfo = {'task_id': id, }

    # 连接测试
    res = client_proxy.test(id, ip, port)
    print(res)
    tools.write_detail(id, res+'\n', 'a+')
    write_step(id,2)

    # 对齐模块
    x_raw,y_raw = alignment.align(id, key, ip, port)
    tools.write_detail(id, '对齐完成共%d条样本\n' % x_raw.shape[0],'a+')
    write_step(id,3)

    # 特征工程&预处理
    x,y = feature_engineering.feating(x_raw, y_raw, ip, port)
    write_step(id,4)

    # 训练
    result = train.tarin(x, y, ip, port, id)
    taskinfo['task_progress'] = '训练完成'
    FAQ.changeTask(taskinfo)
    write_step(id,5)

    # 保存
    model_save.save_model(result, id, ip, port)
    write_step(id,6)

    # 验证
    pred = predict.predict(result[0], x, y, id, ip, port)
    auc, ks = predict.calculate(y, pred.loc[:, 'p'])
    print(auc, ks)
    taskinfo['auc'] = auc
    taskinfo['ks'] = ks
    FAQ.changeTask(taskinfo)
    write_step(id,7)


if __name__ == '__main__':
    os.chdir(os.path.dirname(sys.path[0]))
    start()
