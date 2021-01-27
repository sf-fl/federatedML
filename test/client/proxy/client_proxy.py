# coding=utf-8

import requests
import json


def addTask(addtask,tag):
    ip = addtask['participant_ip']
    port = addtask['participant_port']
    addtask['tag'] = tag
    task_json = json.dumps(addtask)
    r = requests.post('http://%s:%s/addtask'%(ip,port),task_json)
    return r.text


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
    # mid_u_json = json.dumps([key_b,ub])
    mid_u_string = json.dumps([key_b,ub])
    r = requests.post('http://127.0.0.1:8081/learn1',mid_u_string)
    return json.loads(r.text)


def learn_2(gradB_pa,gradA_r):
    # mid_u_json = json.dumps([key_b,ub])
    mid_u_string = json.dumps([gradB_pa,gradA_r])
    r = requests.post('http://127.0.0.1:8081/learn2',mid_u_string)
    return json.loads(r.text)


def predict(ub_list):
    # mid_u_json = json.dumps([key_b,ub])
    mid_u_string = json.dumps(ub_list)
    r = requests.post('http://127.0.0.1:8081/predict',mid_u_string)
    return json.loads(r.text)


def learn_3():
    pass
