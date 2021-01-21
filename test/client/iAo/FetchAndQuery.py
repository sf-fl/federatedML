import pandas as pd
import os
import cx_Oracle
import pymysql
import configparser
import datetime as dt
import sys

#%%
# 建表：account,task,log
def CreateTable():
    db_nickname='jc'
    config = configparser.ConfigParser()
    config.read('.\\config\\dbconfig.conf')
    uid = config.get(db_nickname, 'uid')
    pwd = config.get(db_nickname, 'pwd')
    host = config.get(db_nickname, 'ip')
    port = config.get(db_nickname, 'port')
    databasename=config.get(db_nickname, 'databasename')
    # service=config.get(databasename,'service')
    # 连接数据库
    tag=0
    try:
        conn = pymysql.connect(host=host, port=int(port), user=uid, password=pwd, database=databasename, charset='utf8')
        print('连接数据库成功！')
    except Exception as e:
        print(e)
        return(tag)
    cur=conn.cursor()
    # 建用户表
    tablename='account'
    sql='''create table %s.%s(
    accountid integer, -- 用户ID
    username varchar(20), -- 账户名
    passwd varchar(20), -- 账户密码
    identity varchar(20), -- 账户身份
    create_time timestamp
    );'''%(databasename,tablename)
    try:
        conn.begin()
        cur.execute(sql)
        conn.commit()
        print('建用户表成功！')
    except Exception as e:
        print(e)
        return(tag)
    # 建任务表
    tablename = 'task'
    sql = '''create table %s.%s(
    task_id integer, -- 任务ID
    task_name varchar(100), -- 任务名称
    project_name varchar(100), -- 项目名称
    model_name varchar(200), -- 模型名称
    ip varchar(50), -- 我方ip地址
    port_num integer, -- 我方端口
    protocol  varchar(50), -- 我方协议
    participant_name varchar(100), -- 参与方名称
    participant_ip varchar(50), -- 参与方ip
    participant_port integer, -- 参与方端口
    participant_protocol varchar(50), -- 参与方协议
    dataset_info varchar(200), -- 我方数据集来源信息
    learning_algorithm varchar(50), -- 机器学习算法
    align varchar(50), -- 对齐方式，按照哪个字段对齐
    pretreatment varchar(50), -- 预处理方法概览
    -- encode varchar(50), -- 编码方式
    -- normalization varchar(50), -- 归一化方法
    -- cross_proportion varchar(50), -- 交叉验证比例
    test_proportion varchar(50), -- 训练验证测试集比例
    features varchar(1000), -- 使用的特征
    task_progress varchar(50), -- 任务进度：待审批训练、待加入训练、训练中、训练完、待审批预测、待加入预测、预测中、预测完
    display_location varchar(500), -- 展示结果保存位置
    auc double,
    ks double,
    psi varchar(50),
    result_file varchar(200), -- 结果文件保存位置
    result_data varchar(200), -- 数据库结果保存位置
    create_time date, -- 任务创建时间
    operation_time date -- 任务最后操作时间
    );''' % (databasename, tablename)
    try:
        conn.begin()
        cur.execute(sql)
        conn.commit()
        print('建任务表成功！')
    except Exception as e:
        print(e)
        return (tag)
    # 建日志表
    tablename = 'log'
    sql = '''create table %s.%s(
    task_id integer, -- 任务ID
    task_name varchar(100), -- 任务名称
    model_name varchar(200), -- 模型名称
    task_progress varchar(50), -- 任务进度
    operation_time date -- 任务最后操作时间
    );''' % (databasename, tablename)
    try:
        conn.begin()
        cur.execute(sql)
        conn.commit()
        print('建日志表成功！')
    except Exception as e:
        print(e)
        return (tag)
    cur.close()
    conn.close()
    return tag
#%%
# 建任务表task

#%%
# 建日志表log


#%%
# 注册新账号
def Register(username,passwd,identity):
    db_nickname='sys'
    tablename='account'
    config = configparser.ConfigParser()
    config.read('.\\config\\dbconfig.conf')
    uid = config.get(db_nickname, 'uid')
    pwd = config.get(db_nickname, 'pwd')
    host = config.get(db_nickname, 'ip')
    port = config.get(db_nickname, 'port')
    databasename = config.get(db_nickname, 'databasename')
    # service=config.get(databasename,'service')
    # 连接数据库
    tag=0
    try:
        conn = pymysql.connect(host=host, port=int(port), user=uid, password=pwd, database=databasename, charset='utf8')
        print('连接数据库成功！')
    except Exception as e:
        print(e)
        return(tag)
    cur=conn.cursor()
    # 读取当前表，判断用户是否已注册，并确定用户ID
    try:
        cur.execute('select * from %s.%s'%(databasename,tablename))
        user_list=[acc[1] for acc in cur.fetchall()]
        if username not in user_list:
            accountid=len(user_list)+1
            print('账户ID为：%d'%accountid)
        else:
            print('账户已存在：%s'%username)
            return(tag)
    except Exception as e:
        print(e)
        return(tag)
    # 执行插入和更新
    create_time=dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql='insert into %s.%s (accountid,username,passwd,identity,create_time) values (%d,\'%s\',\'%s\',\'%s\',\'%s\');'%(databasename,tablename,accountid,username,passwd,identity,create_time)
    try:
        conn.begin()
        cur.execute(sql)
        conn.commit()
        tag=1
        print('新账户信息写入成功！')
    except Exception as e:
        conn.rollback()
        print(e)
        return(tag)
    cur.close()
    conn.close()
    return tag   # 注册成功返回1,否则返回0
#%%
# 用户登录
def SignIn(username,passwd):
    db_nickname = 'sys'
    tablename = 'account'
    config = configparser.ConfigParser()
    config.read('.\\config\\dbconfig.conf')
    uid = config.get(db_nickname, 'uid')
    pwd = config.get(db_nickname, 'pwd')
    host = config.get(db_nickname, 'ip')
    port = config.get(db_nickname, 'port')
    databasename = config.get(db_nickname, 'databasename')
    # service=config.get(databasename,'service')
    # 连接数据库
    tag=0
    try:
        conn = pymysql.connect(host=host, port=int(port), user=uid, password=pwd, database=databasename, charset='utf8')
        print('连接数据库成功！')
    except Exception as e:
        print(e)
        return(tag)
    cur = conn.cursor()
    # 读取当前表，判断用户密码是否正确
    try:
        cur.execute('''select * from %s.%s where username=\'%s\'''' % (databasename, tablename,username))
        if passwd==cur.fetchone()[2]:
            print('密码输入正确')
            tag=1
        else:
            print('密码错误')
    except Exception as e:
        print(e)
        return(tag)
    cur.close()
    conn.close()
    return tag   # 登录成功返回1,否则返回0
#%%
# 读取任务列表
def TaskList():
    db_nickname = 'sys'
    tablename = 'task'
    config = configparser.ConfigParser()
    config.read('.\\config\\dbconfig.conf')
    uid = config.get(db_nickname, 'uid')
    pwd = config.get(db_nickname, 'pwd')
    host = config.get(db_nickname, 'ip')
    port = config.get(db_nickname, 'port')
    databasename = config.get(db_nickname, 'databasename')
    # service=config.get(databasename,'service')
    # 连接数据库
    task_list=0
    try:
        conn = pymysql.connect(host=host, port=int(port), user=uid, password=pwd, database=databasename, charset='utf8')
        print('连接数据库成功！')
    except Exception as e:
        print('连接数据库失败')
        print(e)
        return task_list
    cur = conn.cursor()
    # 读取任务表，并按照时间顺序进行排列
    sql='''select task_id,task_name,participant_name,learning_algorithm,task_progress,operation_time from %s.%s where task_progress not like \'%%待%%\''''% (databasename, tablename)
    try:
        cur.execute(sql)
        task_list = pd.DataFrame(columns=[des[0] for des in cur.description], data=cur.fetchall())
        print('查询任务列表成功！')
    except Exception as e:
        print('查询失败')
        print(e)
        return task_list
    cur.close()
    conn.close()
    return task_list
#%%
# 待加入任务列表
def TaskList():
    db_nickname = 'sys'
    tablename = 'task'
    config = configparser.ConfigParser()
    config.read('.\\config\\dbconfig.conf')
    uid = config.get(db_nickname, 'uid')
    pwd = config.get(db_nickname, 'pwd')
    host = config.get(db_nickname, 'ip')
    port = config.get(db_nickname, 'port')
    databasename = config.get(db_nickname, 'databasename')
    # service=config.get(databasename,'service')
    # 连接数据库
    task_list=0
    try:
        conn = pymysql.connect(host=host, port=int(port), user=uid, password=pwd, database=databasename, charset='utf8')
        print('连接数据库成功！')
    except Exception as e:
        print('连接数据库失败')
        print(e)
        return task_list
    cur = conn.cursor()
    # 读取任务表，并按照时间顺序进行排列
    sql='''select task_id,task_name,participant_name,learning_algorithm,task_progress,operation_time from %s.%s where task_progress like \'%%加入%%\''''% (databasename, tablename)
    try:
        cur.execute(sql)
        task_list = pd.DataFrame(columns=[des[0] for des in cur.description], data=cur.fetchall())
        print('查询待加入任务列表成功！')
    except Exception as e:
        print('查询失败')
        print(e)
        return task_list
    cur.close()
    conn.close()
    return
#%%
# 训练任务列表
def TrainTaskList():
    db_nickname = 'sys'
    tablename = 'task'
    config = configparser.ConfigParser()
    config.read('.\\config\\dbconfig.conf')
    uid = config.get(db_nickname, 'uid')
    pwd = config.get(db_nickname, 'pwd')
    host = config.get(db_nickname, 'ip')
    port = config.get(db_nickname, 'port')
    databasename = config.get(db_nickname, 'databasename')
    # service=config.get(databasename,'service')
    # 连接数据库
    task_list=0
    try:
        conn = pymysql.connect(host=host, port=int(port), user=uid, password=pwd, database=databasename, charset='utf8')
        print('连接数据库成功！')
    except Exception as e:
        print('连接数据库失败')
        print(e)
        return task_list
    cur = conn.cursor()
    # 读取任务表，并按照时间顺序进行排列
    sql='''select task_id,task_name,participant_name,learning_algorithm,task_progress,operation_time from %s.%s where task_progress like \'%%训练%%\'''' % (databasename, tablename)
    try:
        cur.execute(sql)
        task_list = pd.DataFrame(columns=[des[0] for des in cur.description], data=cur.fetchall())
        print('查询训练任务列表成功！')
    except Exception as e:
        print(e)
        return task_list
    cur.close()
    conn.close()
    return task_list
#%%
# 预测任务列表
def PredictTaskList():
    db_nickname = 'sys'
    tablename = 'task'
    config = configparser.ConfigParser()
    config.read('.\\config\\dbconfig.conf')
    uid = config.get(db_nickname, 'uid')
    pwd = config.get(db_nickname, 'pwd')
    host = config.get(db_nickname, 'ip')
    port = config.get(db_nickname, 'port')
    databasename = config.get(db_nickname, 'databasename')
    # service=config.get(databasename,'service')
    # 连接数据库
    task_list=0
    try:
        conn = pymysql.connect(host=host, port=int(port), user=uid, password=pwd, database=databasename, charset='utf8')
        print('连接数据库成功！')
    except Exception as e:
        print(e)
        return task_list
    cur = conn.cursor()
    # 读取任务表，并按照时间顺序进行排列
    sql='''select task_id,task_name,participant_name,learning_algorithm,task_progress,operation_time from %s.%s where task_progress like \'%%预测%%\'''' % (databasename, tablename)
    try:
        cur.execute(sql)
        task_list = pd.DataFrame(columns=[des[0] for des in cur.description], data=cur.fetchall())
        print('查询预测任务列表成功！')
    except Exception as e:
        print(e)
        return task_list
    cur.close()
    conn.close()
    return task_list
#%%
# 任务详情
def TaskDetails(task_id,task_name):
    db_nickname = 'sys'
    tablename = 'task'
    config = configparser.ConfigParser()
    config.read('.\\config\\dbconfig.conf')
    uid = config.get(db_nickname, 'uid')
    pwd = config.get(db_nickname, 'pwd')
    host = config.get(db_nickname, 'ip')
    port = config.get(db_nickname, 'port')
    databasename = config.get(db_nickname, 'databasename')
    # service=config.get(databasename,'service')
    # 连接数据库
    task_details=0
    try:
        conn = pymysql.connect(host=host, port=int(port), user=uid, password=pwd, database=databasename, charset='utf8')
        print('连接数据库成功！')
    except Exception as e:
        print(e)
        return task_details
    cur = conn.cursor()
    # 读取任务表，并按照时间顺序进行排列
    sql='''select * from %s.%s where task_id=%d and task_name=\'%s\';''' % (databasename, tablename,task_id,task_name)
    try:
        cur.execute(sql)
        task_details = pd.DataFrame(columns=[des[0] for des in cur.description], data=cur.fetchall())
        print('查询任务详情成功！')
    except Exception as e:
        print(e)
        return task_details
    cur.close()
    conn.close()
    return task_details
#%%
# 发起任务
def InitiateTask(task_details):
    db_nickname = 'sys'
    tablename = 'task'
    config = configparser.ConfigParser()
    config.read('.\\config\\dbconfig.conf')
    uid = config.get(db_nickname, 'uid')
    pwd = config.get(db_nickname, 'pwd')
    host = config.get(db_nickname, 'ip')
    port = config.get(db_nickname, 'port')
    databasename = config.get(db_nickname, 'databasename')
    # service=config.get(databasename,'service')
    # 连接数据库
    tag=0
    try:
        conn = pymysql.connect(host=host, port=int(port), user=uid, password=pwd, database=databasename, charset='utf8')
        print('连接数据库成功！')
    except Exception as e:
        print(e)
        return tag
    cur=conn.cursor()
    # 读取当前表，判断用户是否已注册，并确定用户ID
    sql='''select count(*) from %s.%s'''%(databasename,tablename)
    try:
        cur.execute(sql)
        task_id=cur.fetchone()[0]+1
        print('任务ID为：%d'%task_id)
    except Exception as e:
        print(e)
        return tag
    create_time=operation_time=dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
        return tag
    cur.close()
    conn.close()
#%%
# 从Mysql数据库取数
def DataFetchMysql(databasename,tablename):
    config=configparser.ConfigParser()
    config.read('.\\config\\dbconfig.conf')
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
    config.read('.\\config\\dbconfig.conf')
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


if __name__=='__main__':
    os.chdir(os.path.dirname(os.path.dirname(sys.path[0])))
    CreateTable()
    Register('jc2','109','管理员')
    SignIn('jc1', 'jc')
    t=TaskList()
    TrainTaskList()
    TaskDetails(1, 'test')
    PredictTaskList()
    task_details = {'task_name': 'test'}
    InitiateTask({'task_name': 'test'})