#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from flask import Flask
from flask import request
from flask import redirect
from flask import jsonify
from server.federation import alignment
from server.federation import train
from client.federation import iAo

import os


app = Flask(__name__)


@app.route('/' , methods=['POST'])
def index():
    if request.method == 'POST':
        a = request.get_data()
        dict1 = json.loads(a)
        dict1['返回'] = '成功'
        return json.dumps(dict1)
    else:
        return '<h1>只接受post请求！</h1>'


@app.route('/test' , methods=['GET'])
def test():
    try:
        return '连接成功！'
    except Exception as e:
        print(e)
        return '连接失败！错误情况：%s' % e


@app.route('/addtask' , methods=['POST'])
def addtask():
    try:
        a = request.get_data()
        addtask = json.loads(a)
        tag = addtask['tag']
        ip = request.remote_addr
        port = 8081
        addtask['ip'] = addtask['participant_ip']
        addtask['port'] = addtask['participant_port']
        addtask['participant_ip'] = ip
        addtask['participant_port'] = port
        result = iAo.receive_task(addtask,tag)
        return json.dumps(result)
    except Exception as e:
        print(e)
        return '出现错误！错误情况：%s' % e



@app.route('/align1' , methods=['POST'])
def align1():
    try:
        a = request.get_data()
        dict1 = json.loads(a)
        result = alignment.align1(dict1).to_dict()
        return json.dumps(result)
    except Exception as e:
        print(e)
        return '出现错误！错误情况：%s' % e


@app.route('/align2' , methods=['POST'])
def align2():
    try:
        a = request.get_data()
        dict1 = json.loads(a)
        b_key = dict1['sample']
        id = dict1['id']
        key = dict1['key']
        result = alignment.align2(b_key,id,key).to_list()
        return json.dumps(result)
    except Exception as e:
        return '连接失败！错误情况：%s' % e


@app.route('/learn1' , methods=['POST'])
def learn1():
    try:
        a = request.get_data()
        dict1 = json.loads(a)
        result = train.train1(dict1)
        return json.dumps(result)
    except Exception as e:
        return '连接失败！错误情况：%s' % e


@app.route('/learn2' , methods=['POST'])
def learn2():
    try:
        a = request.get_data()
        dict1 = json.loads(a)
        result = train.train2(dict1)
        return json.dumps(result)
    except Exception as e:
        return '连接失败！错误情况：%s' % e


@app.route('/learn3' , methods=['POST'])
def learn3():
    try:
        a = request.get_data()
        dict1 = json.loads(a)
        result = train.train3(dict1)
        return json.dumps(result)
    except Exception as e:
        return '连接失败！错误情况：%s' % e


@app.route('/predict' , methods=['POST'])
def predict():
    try:
        a = request.get_data()
        dict1 = json.loads(a)
        result = train.predict(dict1)
        return json.dumps(result)
    except Exception as e:
        return '连接失败！错误情况：%s' % e


if __name__ =='__main__':
    import sys
    os.chdir(os.path.dirname(os.path.dirname(sys.path[0])))
    app.run(host='0.0.0.0',port='8081',debug=True)