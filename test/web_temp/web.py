from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  #Flask的跨域问题
from client.federation import iAo
from web_temp import temp_file
import os
import sys
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


@app.route('/tasklist',methods=['GET'])
def tasklist():
    params = request.args.to_dict()
    returndict = {}
    returndict['state'] = "success"
    returndict['result'] = temp_file.gettasklist(int(params['page']), 'execute')
    return returndict


@app.route('/applylist',methods=['GET'])
def applylist():
    params = request.args.to_dict()
    returndict = {}
    returndict['state'] = "success"
    returndict['result'] = temp_file.gettasklist(int(params['page']), 'apply')
    return returndict


@app.route('/trainform',methods=['POST'])
def trainform():
    id = int(list(request.values.to_dict().keys())[0])
    returndict = temp_file.get_append_task(id)[0]
    return returndict


@app.route('/traininfo',methods=['POST'])
def traininfo():
    id = int(list(request.values.to_dict().keys())[0])
    returndict = temp_file.get_train_info(id)[0]
    return returndict


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
            file_path = os.path.join(r"./web_temp/data", "train_data.csv")
            file_obj.save(file_path)
            with open(file_path,'r',encoding='utf-8') as f1:
                feature = f1.readline().strip().split(',')
        else:
            file_path = '文件格式错误'
    return {'file_path':file_path,'feature':feature}


@app.route('/add_traintask',methods=["POST"])
def add_traintask():
    request_info = request.values.to_dict()
    try:
        checklist = ['taskname','alian_feature','ip','port','learningAlgorithm','expireDate','modelname','trainratio','partnername']
        for s in checklist:
            no_null(s,request_info[s])
        with open("./web_temp/data/train_data.csv", 'r', encoding='utf-8-sig') as f1:
            feature = f1.readline().strip().split(',')
            if request_info['alian_feature'] not in feature:
                raise Exception('对齐字段无法找到，请重新填写')
        iAo.save_task(request_info,'train')
        return 'success'
    except Exception as e:
        # writelog todo
        return e


@app.route('/append_traintask', methods=['post'])
def append_traintask():
    pass


@app.route('/add_predicttask',methods=["POST"])
def add_predicttask():
    request_info = request.values.to_dict()
    try:
        checklist = ['taskname','alian_feature','ip','port','learningAlgorithm','expireDate','modelname','trainratio','partnername']
        for s in checklist:
            no_null(s,request_info[s])
        with open("./web_temp/data/train_data.csv", 'r', encoding='utf-8-sig') as f1:
            feature = f1.readline().strip().split(',')
            if request_info['alian_feature'] not in feature:
                raise Exception('对齐字段无法找到，请重新填写')
        iAo.save_task(request_info, 'predict')
        return 'success'
    except Exception as e:
        # writelog todo
        return e


@app.route('/append_predicttask', methods=['post'])
def append_predicttask():
    pass


@app.route('/login',methods=["POST"])
def login():
    request_info = request.form.to_dict()
    flag = iAo.login(request_info['account'],request_info['password'])
    session = 'xxxxxxxxxx'
    accountId = 'xxx'
    result = {'state': flag, 'data': {}}
    result['data']['accountId'] = accountId
    result['data']['session'] = session
    return result


if __name__ == "__main__":
    os.chdir(os.path.dirname(sys.path[0]))
    app.run(debug=False)
