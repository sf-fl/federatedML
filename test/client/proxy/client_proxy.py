#coding=utf-8

import requests
import json


def test():

    r = requests.get('http://127.0.0.1:8081/test')
    return r.text

data={ "opr": "add", "data": { "userName": "98997", "disc": "hudihiudhu", "expDate":"2", "ip": [ "10.10.11.1", "10.10.11.2", "10.10.11.3" ] } }
data = json.dumps(data)