# coding=utf-8
from client import start
import requests
import json


def addTask(addtask,tag):
    ip = addtask['participant_ip']
    port = addtask['participant_port']
    addtask['tag'] = tag
    task_json = json.dumps(addtask)
    r = requests.post('http://%s:%s/addtask'%(ip,port),task_json)
    return r.text

def beginTask(addtask,tag,id):
    ip = addtask['participant_ip']
    port = addtask['participant_port']
    key = addtask['align']
    tag_json = json.dumps({'tag':tag})
    start.start(id=id, ip=ip, port=port, key=key)
    return 0


def test(id, ip, port):
    r = requests.get('http://%s:%s/test?id=%s' % (ip, port, id))
    return r.text


def align_1(public_key):
    sample_json = json.dumps(public_key)
    r = requests.post('http://127.0.0.1:8081/align1', sample_json)
    return json.loads(r.text)


def align_2(b_key, id, key, ip, port):
    sample_json = json.dumps({'sample':b_key.to_list(), 'id': id, 'key': key})
    r = requests.post('http://%s:%s/align2' % (ip, port), sample_json)
    return json.loads(r.text)


def woe_1(y_encrypt, y_r_encrypt, id, public_key, ip, port):
    sample_json = json.dumps({'y': y_encrypt.to_list(), '1-y': y_r_encrypt.to_list(), 'id': id, 'pk': public_key})
    r = requests.post('http://%s:%s/woe1' % (ip, port), sample_json)
    return json.loads(r.text)


def learn_1(ub, key_b, ip, port):
    mid_u_string = json.dumps([key_b,ub])
    r = requests.post('http://%s:%s/learn1' % (ip, port), mid_u_string)
    return json.loads(r.text)


def learn_2(gradB_pa, gradA_r, ip, port):
    mid_u_string = json.dumps([gradB_pa,gradA_r])
    r = requests.post('http://%s:%s/learn2' % (ip, port), mid_u_string)
    return json.loads(r.text)


def save(id, ip, port):
    r = requests.post('http://%s:%s/train3' % (ip, port), json.dumps({'id': id}))
    return r


def predict(ub_list,ip,port):
    mid_u_string = json.dumps(ub_list)
    r = requests.post('http://%s:%s/predict' % (ip, port), mid_u_string)
    return json.loads(r.text)


