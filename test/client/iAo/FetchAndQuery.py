import pandas as pd
import os
import cx_Oracle
import pymysql
import configparser
import datetime as dt


# 注册新账号
def Register(username,passwd,identity):
    databasename='sys'
    tablename='account'
    config = configparser.ConfigParser()
    config.read(r'D:\test\dbconfig.conf')
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
    return tag
# 用户登录
def SignIn(username,passwd):
    databasename = 'sys'
    tablename = 'account'
    config = configparser.ConfigParser()
    config.read(r'D:\test\dbconfig.conf')
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
        cur.execute('select * from %s.%s where user=%s' % (databasename, tablename,username))
        if passwd==cur.fetchone()[2]:
            tag=1
    except Exception as e:
        print(e)
    cur.close()
    conn.close()
    return tag

#%%
# 读取任务列表
def TaskList():
    databasename = 'sys'
    tablename = 'task'
    config = configparser.ConfigParser()
    config.read(r'D:\test\dbconfig.conf')
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
    try:
        cur.execute('select task_id,task_name,participant_name,learning_algorithm,task_progress,operation_time from %s.%s' % (databasename, tablename))
        task_list = pd.DataFrame(columns=[des[0] for des in cur.description], data=cur.fetchall())
        print('查询成功！')
    except Exception as e:
        print(e)
    cur.close()
    conn.close()
    return task_list

# 训练任务列表
def TrainTaskList():
    databasename = 'sys'
    tablename = 'task'
    config = configparser.ConfigParser()
    config.read(r'D:\test\dbconfig.conf')
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
    sql='''select task_id,task_name,participant_name,learning_algorithm,task_progress,operation_time from %s.%s where task_progress in ('待审核训练','待加入训练','训练中','训练完')''' % (databasename, tablename)
    try:
        cur.execute(sql)
        task_list = pd.DataFrame(columns=[des[0] for des in cur.description], data=cur.fetchall())
        print('查询成功！')
    except Exception as e:
        print(e)
    cur.close()
    conn.close()
    return task_list

# 预测任务列表
def PredictTaskList():
    databasename = 'sys'
    tablename = 'task'
    config = configparser.ConfigParser()
    config.read(r'D:\test\dbconfig.conf')
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
    sql='''select task_id,task_name,participant_name,learning_algorithm,task_progress,operation_time from %s.%s where task_progress in ('待审核预测','待加入预测','预测中','预测完')''' % (databasename, tablename)
    try:
        cur.execute(sql)
        task_list = pd.DataFrame(columns=[des[0] for des in cur.description], data=cur.fetchall())
        print('查询成功！')
    except Exception as e:
        print(e)
    cur.close()
    conn.close()
    return task_list

# 任务详情
def TaskDetails(task_id,task_name):
    databasename = 'sys'
    tablename = 'task'
    config = configparser.ConfigParser()
    config.read(r'D:\test\dbconfig.conf')
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
    sql='''select * from %s.%s where task_id=%d and task_name=%s;''' % (databasename, tablename,task_id,task_name)
    try:
        cur.execute(sql)
        task_details = pd.DataFrame(columns=[des[0] for des in cur.description], data=cur.fetchall())
        print('查询成功！')
    except Exception as e:
        print(e)
    cur.close()
    conn.close()
    return task_details

#%%
# 发起训练
def InitiateTraining(task_name,mode_name,):
    databasename='sys'
    tablename='task'
    config = configparser.ConfigParser()
    config.read(r'D:\test\dbconfig.conf')
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
    try:
        cur.execute('select * from %s.%s'%(databasename,tablename))
        user_list=[acc[1] for acc in cur.fetchall()]
        if user not in user_list:
            accountid=len(user_list)+1
        print('账户ID为：%d'%accountid)
    except Exception as e:
        print(e)
    # 执行插入和更新
    create_time=dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql='insert into %s.%s (accountid,user,password,identity,create_time) values (%d,\'%s\',\'%s\',\'%s\',\'%s\');'%(databasename,tablename,accountid,user,password,identity,create_time)
    try:
        conn.begin()
        cur.execute(sql)
        conn.commit()
        print('新账户信息写入成功！')
    except Exception as e:
        conn.rollback()
        print(e)
    cur.close()
    conn.close()
Register('jc1','jc','普通用户')



def DataFetchMysql(databasename,tablename):
    config=configparser.ConfigParser()
    config.read(r'D:\test\dbconfig.conf')
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



def DataFetchPlsql(databasename,tablename):
    config = configparser.ConfigParser()
    config.read(r'D:\test\dbconfig.conf')
    uid = config.get(databasename, 'uid')
    pwd = config.get(databasename, 'pwd')
    host = config.get(databasename, 'ip')
    port = config.get(databasename, 'port')
    service=config.get(databasename,'service')
    conn = cx_Oracle.connect(uid,pwd,host+':'+port+'/'+service) #按照上面的连接格式改写，添加DSN
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