from client.iAo import initialAndCreate
from client.iAo import FetchAndQuery

def initialize_fl():
    initialAndCreate.CreateTable()
    initialAndCreate.Register(username='admin', passwd='password', identity='administrator')
