#coding=utf-8

import requests
import json


def test():

    r = requests.get('http://127.0.0.1:8081/test')
    return r.text


def align_1(public_key):
    sample_json = json.dumps(public_key)
    r = requests.post('http://127.0.0.1:8081/align1',sample_json)
    return json.loads(r.text)


def align_2(b_key):
    sample_json = json.dumps(b_key.to_list())
    r = requests.post('http://127.0.0.1:8081/align2',sample_json)
    return json.loads(r.text)


def learn_1(ub,key_b):
    mid_u_json = json.dumps([key_b,ub])
    r = requests.post('http://127.0.0.1:8081/learn1',mid_u_json)
    return json.loads(r.text)

def learn_2():
    pass


def learn_3():
    pass


data={ "opr": "add", "data": { "userName": "98997", "disc": "hudihiudhu", "expDate":"2", "ip": [ "10.10.11.1", "10.10.11.2", "10.10.11.3" ] } }
data = json.dumps(data)