from proxy import client_proxy
from federation import alignment

def start():
    # 连接测试
    print(client_proxy.test())
    # 对齐模块
    alignment.align()




if __name__ == '__main__':
    start()