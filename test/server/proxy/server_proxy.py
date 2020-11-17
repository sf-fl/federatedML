#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from flask import Flask
from flask import request
from flask import redirect
from flask import jsonify


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
        return '连接失败！错误情况：%s' % e


@app.route('/align1' , methods=['POST'])
def align1():
    try:
        return '连接成功！'
    except Exception as e:
        return '连接失败！错误情况：%s' % e


@app.route('/align2' , methods=['POST'])
def align2():
    try:
        return '连接成功！'
    except Exception as e:
        return '连接失败！错误情况：%s' % e


if __name__ =='__main__':
    app.run(port='8081',debug=True)