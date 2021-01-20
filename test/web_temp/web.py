from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  #Flask的跨域问题
import os
import json
import pandas as pd

app = Flask(__name__)
app.config['data'] = r"./data"
CORS(app)                   #Flask的跨域问题

def no_null(s,svalue):
    #  非空校验
    if svalue == '':
        raise Exception(s+'不能为空')

@app.route('/')


@app.route('/upload',methods=["POST"]) # 方法要与前端一致
def upload():
    file_obj = None
    try:
        file_obj = request.files['file']  # Flask中获取文件
    except Exception as e:
        if file_obj is None:  # 表示没有发送文件
            return '未上传文件,error:'+str(e)
        return '其他错误,error:'+str(e)
    else:
        # 判断文件格式
        if file_obj.filename[-4:] == '.csv':
            # 保存文件
            file_path = os.path.join(app.config['data'], "train_data.csv")
            file_obj.save(file_path)
            with open(file_path,'r',encoding='utf-8') as f1:
                feature = f1.readline().strip().split(',')
        else:
            file_path = '文件格式错误'
    return {'file_path':file_path,'feature':feature}


@app.route('/add_traintask',methods=["POST"])
def add_user():
    request_info = request.values.to_dict()
    try:
        checklist = ['taskname','alian_feature','ip','port','learningAlgorithm','expireDate','modelname','trainratio','partnername']
        for s in checklist:
            no_null(s,request_info[s])

        return 'success'
    except Exception as e:
        # writelog todo
        return e


@app.route('/login',methods=["POST"])
def login():
    request_info = request.form.to_dict()
    flag = 'fail'
    if request_info['account'] == 'admin' and request_info['password'] == 'password':
        flag = 'success'
    session = 'xxxxxxxxxx'
    accountId = 'xxx'
    result = {}
    result['state'] = flag
    result['data'] = {}
    result['data']['accountId'] = accountId
    result['data']['session'] = session
    return result

if __name__ == "__main__":
    app.run(debug=True)
