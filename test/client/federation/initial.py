from client.iAo import initialAndCreate
from client.iAo import FetchAndQuery

def initialize_fl():
    initialAndCreate.CreateTable()
    initialAndCreate.Register(username='admin', passwd='password', identity='administrator')


if __name__ == '__main__':
    import os
    import sys
    os.chdir(os.path.dirname(os.path.dirname(sys.path[0])))
    initialize_fl()