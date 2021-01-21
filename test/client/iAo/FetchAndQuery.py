import pandas as pd
import os
import cx_Oracle
import pymysql
import configparser
import datetime as dt

#%%
# 注册新账号
def Register(username,passwd,identity):
    databasename='sys'
    tablename='account'
    config = configparser.ConfigParser()
    path=os.path.abspath('.')
    config.read((path+'\\test\\config\\dbconfig.conf'))
    uid = config.get(databasename, 'uid')
    pwd = config.get(databasename, 'pwd')
    host = config.get(databasename, 'ip')
    port = config.get(databasename, 'port')
    # service=config.get(databasename,'service')
    # 连接数据库
    tag=0
    try:
        conn = pymysql.connect(host=host, port=int(port), user=uid, password=pwd, database=databasename, charset='utf8')
        print('连接数据库成功！')
    except Exception as e:
        print(e)
    cur=conn.cursor()
    # 读取当前表，判断用户是否已注册，并确定用户ID
    try:
        cur.execute('select * from %s.%s'%(databasename,tablename))
        user_list=[acc[1] for acc in cur.fetchall()]
        if username not in user_list:
            accountid=len(user_list)+1
            print('账户ID为：%d'%accountid)
    except Exception as e:
        print(e)
    # 执行插入和更新
    create_time=dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql='insert into %s.%s (accountid,username,password,identity,create_time) values (%d,\'%s\',\'%s\',\'%s\',\'%s\');'%(databasename,tablename,accountid,username,passwd,identity,create_time)
    try:
        conn.begin()
        cur.execute(sql)
        conn.commit()
        tag=1
        print('新账户信息写入成功！')
    except Exception as e:
        conn.rollback()
        print(e)
    cur.close()
    conn.close()
    return tag   # 注册成功返回1,否则返回0

#%%
# 用户登录
def SignIn(username,passwd):
    databasename = 'sys'
    tablename = 'account'
    config = configparser.ConfigParser()
    path = os.path.abspath('.')
    config.read((path + '\\test\\config\\dbconfig.conf'))
    uid = config.get(databasename, 'uid')
    pwd = config.get(databasename, 'pwd')
    host = config.get(databasename, 'ip')
    port = config.get(databasename, 'port')
    # service=config.get(databasename,'service')
    # 连接数据库
    tag=0
    try:
        conn = pymysql.connect(host=host, port=int(port), user=uid, password=pwd, database=databasename, charset='utf8')
        print('连接数据库成功！')
    except Exception as e:
        print(e)
    cur = conn.cursor()
    # 读取当前表，判断用户密码是否正确
    try:
        cur.execute('''select * from %s.%s where user=\'%s\'''' % (databasename, tablename,username))
        if passwd==cur.fetchone()[2]:
            tag=1
    except Exception as e:
        print(e)
    cur.close()
    conn.close()
    return tag   # 登录成功返回1,否则返回0
SignIn('jc1','jc')
#%%
# 读取任务列表
def TaskList():
    databasename = 'sys'
    tablename = 'task'
    config = configparser.ConfigParser()
    path = os.path.abspath('.')
    config.read((path + '\\test\\config\\dbconfig.conf'))
    uid = config.get(databasename, 'uid')
    pwd = config.get(databasename, 'pwd')
    host = config.get(databasename, 'ip')
    port = config.get(databasename, 'port')
    # service=config.get(databasename,'service')
    # 连接数据库
    task_list=0
    try:
        conn = pymysql.connect(host=host, port=int(port), user=uid, password=pwd, database=databasename, charset='utf8')
        print('连接数据库成功！')
    except Exception as e:
        print(e)
    cur = conn.cursor()
    # 读取任务表，并按照时间顺序进行排列
    sql='''select task_id,task_name,participant_name,learning_algorithm,task_progress,operation_time from %s.%s where task_progress 
    not like \'%待%\''''% (databasename, tablename)
    try:
        cur.execute(sql)
        task_list = pd.DataFrame(columns=[des[0] for des in cur.description], data=cur.fetchall())
        print('查询成功！')
    except Exception as e:
        print(e)
    cur.close()
    conn.close()
    return task_list
TaskList()
#%%
# 训练任务列表
def TrainTaskList():
    databasename = 'sys'
    tablename = 'task'
    config = configparser.ConfigParser()
    path = os.path.abspath('.')
    config.read((path + '\\test\\config\\dbconfig.conf'))
    uid = config.get(databasename, 'uid')
    pwd = config.get(databasename, 'pwd')
    host = config.get(databasename, 'ip')
    port = config.get(databasename, 'port')
    # service=config.get(databasename,'service')
    # 连接数据库
    task_list=0
    try:
        conn = pymysql.connect(host=host, port=int(port), user=uid, password=pwd, database=databasename, charset='utf8')
        print('连接数据库成功！')
    except Exception as e:
        print(e)
    cur = conn.cursor()
    # 读取任务表，并按照时间顺序进行排列
    sql='''select task_id,task_name,participant_name,learning_algorithm,task_progress,operation_time from %s.%s where task_progress like \'%训练%\'''' % (databasename, tablename)
    try:
        cur.execute(sql)
        task_list = pd.DataFrame(columns=[des[0] for des in cur.description], data=cur.fetchall())
        print('查询成功！')
    except Exception as e:
        print(e)
    cur.close()
    conn.close()
    return task_list
TrainTaskList()
#%%
# 预测任务列表
def PredictTaskList():
    databasename = 'sys'
    tablename = 'task'
    config = configparser.ConfigParser()
    path = os.path.abspath('.')
    config.read((path + '\\test\\config\\dbconfig.conf'))
    uid = config.get(databasename, 'uid')
    pwd = config.get(databasename, 'pwd')
    host = config.get(databasename, 'ip')
    port = config.get(databasename, 'port')
    # service=config.get(databasename,'service')
    # 连接数据库
    task_list=0
    try:
        conn = pymysql.connect(host=host, port=int(port), user=uid, password=pwd, database=databasename, charset='utf8')
        print('连接数据库成功！')
    except Exception as e:
        print(e)
    cur = conn.cursor()
    # 读取任务表，并按照时间顺序进行排列
    sql='''select task_id,task_name,participant_name,learning_algorithm,task_progress,operation_time from %s.%s where task_progress like \'%预测%\'''' % (databasename, tablename)
    try:
        cur.execute(sql)
        task_list = pd.DataFrame(columns=[des[0] for des in cur.description], data=cur.fetchall())
        print('查询成功！')
    except Exception as e:
        print(e)
    cur.close()
    conn.close()
    return task_list
PredictTaskList()
#%%
# 任务详情
def TaskDetails(task_id,task_name):
    databasename = 'sys'
    tablename = 'task'
    config = configparser.ConfigParser()
    path = os.path.abspath('.')
    config.read((path + '\\test\\config\\dbconfig.conf'))
    uid = config.get(databasename, 'uid')
    pwd = config.get(databasename, 'pwd')
    host = config.get(databasename, 'ip')
    port = config.get(databasename, 'port')
    # service=config.get(databasename,'service')
    # 连接数据库
    task_details=0
    try:
        conn = pymysql.connect(host=host, port=int(port), user=uid, password=pwd, database=databasename, charset='utf8')
        print('连接数据库成功！')
    except Exception as e:
        print(e)
    cur = conn.cursor()
    # 读取任务表，并按照时间顺序进行排列
    sql='''select * from %s.%s where task_id=%d and task_name=\'%s\';''' % (databasename, tablename,task_id,task_name)
    try:
        cur.execute(sql)
        task_details = pd.DataFrame(columns=[des[0] for des in cur.description], data=cur.fetchall())
        print('查询成功！')
    except Exception as e:
        print(e)
    cur.close()
    conn.close()
    return task_details
TaskDetails(1,'test')

#%%
# 发起任务
def InitiateTask(task_details):
    databasename='sys'
    tablename='task'
    config = configparser.ConfigParser()
    path = os.path.abspath('.')
    config.read((path + '\\test\\config\\dbconfig.conf'))
    uid = config.get(databasename, 'uid')
    pwd = config.get(databasename, 'pwd')
    host = config.get(databasename, 'ip')
    port = config.get(databasename, 'port')
    # service=config.get(databasename,'service')
    # 连接数据库
    try:
        conn = pymysql.connect(host=host, port=int(port), user=uid, password=pwd, database=databasename, charset='utf8')
        print('连接数据库成功！')
    except Exception as e:
        print(e)
    cur=conn.cursor()
    # 读取当前表，判断用户是否已注册，并确定用户ID
    sql='''select count(*) from %s.%s'''%(databasename,tablename)
    try:
        cur.execute(sql)
        task_id=cur.fetchone()[0]+1
        print('任务ID为：%d'%task_id)
    except Exception as e:
        print(e)
    create_time=operation_time=dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    task_id=task_details.get('task_id')
    task_name=task_details.get('task_name')
    project_name=task_details.get('project_name')
    model_name=task_details.get('model_name')
    ip=task_details.get('ip')
    port=task_details.get('port')
    if port==None:
        port=0
    protocol=task_details.get('protocol')
    participant_name=task_details.get('participant_name')
    participant_ip=task_details.get('participant_ip')
    participant_port=task_details.get('participant_port')
    if participant_port==None:
        participant_port=0
    participant_protocol=task_details.get('participant_protocol')
    dataset_info=task_details.get('dataset_info')
    learning_algorithm=task_details.get('learning_algorithm')
    align=task_details.get('align')
    pretreatment=task_details.get('pretreatment')
    test_proportion=task_details.get('test_proportion')
    features=task_details.get('features')
    task_progress=task_details.get('task_progress')
    display_location=task_details.get('display_location')
    auc=task_details.get('auc')
    if auc==None:
        auc=0
    ks=task_details.get('ks')
    if ks==None:
        ks=0
    psi=task_details.get('psi')
    if psi==None:
        psi=0
    result_file=task_details.get('result_file')
    result_data=task_details.get('result_data')
    sql='''insert into %s.%s (task_id,task_name,project_name,model_name,ip,port,protocol,participant_name,participant_ip,
    participant_port,participant_protocol,dataset_info,learning_algorithm,align,pretreatment,test_proportion,features,
    task_progress,display_location,auc,ks,psi,result_file,result_data,create_time,operation_time) values (%d,\'%s\',\'%s\',
    \'%s\',\'%s\',%d,\'%s\',\'%s\',\'%s\',%d,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',%f,%f,%f,\'%s\',
    \'%s\',\'%s\',\'%s\')'''%(databasename,tablename,task_id,task_name,project_name,model_name,ip,port,protocol,participant_name,
    participant_ip,participant_port,participant_protocol,dataset_info,learning_algorithm,align,pretreatment,test_proportion,features,
    task_progress,display_location,auc,ks,psi,result_file,result_data,create_time,operation_time)
    try:
        conn.begin()
        cur.execute(sql)
        conn.commit()
        print('任务创建成功，任务ID：%s，任务名称：%s'%(task_id,task_name))
    except Exception as e:
        print(e)
    cur.close()
    conn.close()


task_details={'task_name':'test'}
InitiateTask({'task_name':'test'})

#%%
# 从Mysql数据库取数
def DataFetchMysql(databasename,tablename):
    config=configparser.ConfigParser()
    path = os.path.abspath('.')
    config.read((path + '\\test\\config\\dbconfig.conf'))
    uid=config.get(databasename,'uid')
    pwd=config.get(databasename,'pwd')
    host=config.get(databasename,'ip')
    port=config.get(databasename,'port')
    # service=config.get(databasename,'service')
    conn=pymysql.connect(host=host,port=int(port),user=uid,password=pwd,database=databasename,charset='utf8')
    cur=conn.cursor()
    dic=dict()
    for i in tablename:
        cur.execute('select * from %s.%s'%(databasename,i))
        dic[i]=pd.DataFrame(columns=[des[0] for des in cur.description],data=cur.fetchall())
    cur.close()
    conn.close()
    return dic

#%%
#从oracle数据库取数
def DataFetchOracle(databasename,tablename):
    config = configparser.ConfigParser()
    path = os.path.abspath('.')
    config.read((path + '\\test\\config\\dbconfig.conf'))
    uid = config.get(databasename, 'uid')
    pwd = config.get(databasename, 'pwd')
    host = config.get(databasename, 'ip')
    port = config.get(databasename, 'port')
    service=config.get(databasename,'service')
    dsn=cx_Oracle.makedsn(host,port,service)
    conn = cx_Oracle.connect(uid,pwd,dsn) #按照上面的连接格式改写，添加DSN
    cur = conn.cursor()
    dic = dict()
    for i in tablename:
        cur.execute('select * from %s.%s' % (databasename, i))
        dic[i] = pd.DataFrame(columns=[des[0] for des in cur.description], data=cur.fetchall())
    cur.close()
    conn.close()
    return dic



key='phone_num'
def get_data_key():
    data = pd.read_csv('%s/data_storage/data.csv' % os.getcwd())
    key_word = data[key]
    return data,key_word