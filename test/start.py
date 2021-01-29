from web_temp import web
from server.proxy import server_proxy
import os
import sys

from multiprocessing import Process,Lock
import time
def work1(lock):
    lock.acquire()
    web.app.run(port=5000,debug=False)
    lock.release()

def work2(lock):
    lock.acquire()
    server_proxy.app.run(port=8081,debug=False)
    lock.release()

if __name__ == '__main__':
    os.chdir(sys.path[0])
    lock=Lock()
    p1 = Process(target=work1,args=(lock,))

    p1.start()




if __name__ == '__main__':
    os.chdir(sys.path[0])
    # web.app.run(port=5000,debug=False)
    lock = Lock()
    p2 = Process(target=work2, args=(lock,))
    p2.start()
    # server_proxy.app.run(port=8081,debug=False)