import pandas as pd
import os
import cx_Oracle
import pymysql
import configparser
import datetime as dt
import sys


# %%
# 用户登录
def signIn(username, passwd):
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
        cur.execute('select * from %s.%s where username=\'%s\'' % (databasename, tablename,username))
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


# %%
# 读取任务列表
def taskList():
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
    sql='''select task_id,task_name,participant_name,learning_algorithm,task_progress,operation_time 
    from %s.%s where task_progress not like \'%%待%%\'
    order by operation_time desc'''% (databasename, tablename)
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
def appendTaskList():
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
    task_list = pd.DataFrame()
    try:
        conn = pymysql.connect(host=host, port=int(port), user=uid, password=pwd, database=databasename, charset='utf8')
        print('连接数据库成功！')
    except Exception as e:
        print('连接数据库失败')
        print(e)
        return task_list
    cur = conn.cursor()
    # 读取任务表，并按照时间顺序进行排列
    sql='''select task_id,task_name,participant_name,learning_algorithm,task_progress,operation_time 
    from %s.%s where task_progress like \'%%加入%%\'
    order by operation_time desc'''% (databasename, tablename)
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
    return task_list


# %%
# 训练任务列表
def trainTaskList():
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
    sql='''select task_id,task_name,participant_name,learning_algorithm,task_progress,operation_time 
    from %s.%s where task_progress like \'%%训练%%\'''' % (databasename, tablename)
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


# %%
# 预测任务列表
def predictTaskList():
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
    sql='''select task_id,task_name,participant_name,learning_algorithm,task_progress,operation_time 
    from %s.%s where task_progress like \'%%预测%%\'''' % (databasename, tablename)
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


# %%
# 任务详情
def taskDetails(task_id, task_name=None):
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
    # 读取任务表，得到所需任务
    if task_name is not None:
        sql='select * from %s.%s where task_id=%d and task_name=\'%s\';' % (databasename, tablename,task_id,task_name)
    else:
        sql = 'select * from %s.%s where task_id=%d;' % (databasename, tablename, task_id)
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


# %%
# 发起任务
def initiateTask(task_details):
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
    task_id = 0
    try:
        conn = pymysql.connect(host=host, port=int(port), user=uid, password=pwd, database=databasename, charset='utf8')
        print('连接数据库成功！')
    except Exception as e:
        print(e)
        return task_id
    cur=conn.cursor()
    # 读取当前任务数，并计算任务编号，待优化
    sql='''select count(*) from %s.%s'''%(databasename,tablename)
    try:
        cur.execute(sql)
        task_id=cur.fetchone()[0]+1  # todo
        print('任务ID为：%d'%task_id)
    except Exception as e:
        print(e)
        return task_id
    create_time=operation_time=dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    task_name=task_details.get('task_name')
    project_name=task_details.get('project_name')
    model_name=task_details.get('model_name')
    ip=task_details.get('ip')
    port=task_details.get('port')
    protocol=task_details.get('protocol')
    participant_name=task_details.get('participant_name')
    participant_ip=task_details.get('participant_ip')
    participant_port=task_details.get('participant_port')
    participant_protocol=task_details.get('participant_protocol')
    dataset_info=task_details.get('dataset_info')
    learning_algorithm=task_details.get('learning_algorithm')
    align=task_details.get('align')
    pretreatment=task_details.get('pretreatment')
    train_proportion=task_details.get('train_proportion')
    features=task_details.get('features')
    task_progress=task_details.get('task_progress')
    display_location=task_details.get('display_location')
    auc=task_details.get('auc', 0)
    ks=task_details.get('ks', 0)
    psi=task_details.get('psi', 0)
    result_file=task_details.get('result_file')
    result_data=task_details.get('result_data')
    sql='''insert into %s.%s (task_id,task_name,project_name,model_name,ip,port_num,protocol,participant_name,participant_ip,
    participant_port,participant_protocol,dataset_info,learning_algorithm,align,pretreatment,train_proportion,features,
    task_progress,display_location,auc,ks,psi,result_file,result_data,create_time,operation_time) values (%d,\'%s\',\'%s\',
    \'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',%f,%f,%f,\'%s\',
    \'%s\',\'%s\',\'%s\')'''%(databasename,tablename,task_id,task_name,project_name,model_name,ip,port,protocol,participant_name,
    participant_ip,participant_port,participant_protocol,dataset_info,learning_algorithm,align,pretreatment,train_proportion,features,
    task_progress,display_location,auc,ks,psi,result_file,result_data,create_time,operation_time)
    try:
        conn.begin()
        cur.execute(sql)
        conn.commit()
        print('任务创建成功，任务ID：%s，任务名称：%s'%(task_id,task_name))
    except Exception as e:
        print(e)
        return task_id
    cur.close()
    conn.close()
    return task_id


# 发起任务
def changeTask(task_details):
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
    task_id = 0
    try:
        conn = pymysql.connect(host=host, port=int(port), user=uid, password=pwd, database=databasename, charset='utf8')
        print('连接数据库成功！')
    except Exception as e:
        print(e)
        return task_id
    task_id = task_details.get('task_id')
    cur=conn.cursor()
    # 读取当前任务数，并计算任务编号，待优化
    sql='''select * from %s.%s
            where task_id = %s'''%(databasename,tablename,task_id)
    try:
        cur.execute(sql)
        task_details_raw = pd.DataFrame(columns=[des[0] for des in cur.description], data=cur.fetchall()).T.to_dict()[0]
        print('任务ID为：%s' % str(task_id))
    except Exception as e:
        print(e)
        return task_id
    create_time=task_details_raw.get('create_time')
    operation_time=dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    task_name=task_details.get('task_name',task_details_raw.get('task_name'))
    project_name=task_details.get('project_name',task_details_raw.get('project_name'))
    model_name=task_details.get('model_name',task_details_raw.get('model_name'))
    ip=task_details.get('ip',task_details_raw.get('ip'))
    port=task_details.get('port',task_details_raw.get('port'))
    protocol=task_details.get('protocol',task_details_raw.get('protocol'))
    participant_name=task_details.get('participant_name',task_details_raw.get('participant_name'))
    participant_ip=task_details.get('participant_ip',task_details_raw.get('participant_ip'))
    participant_port=task_details.get('participant_port',task_details_raw.get('participant_port'))
    participant_protocol=task_details.get('participant_protocol',task_details_raw.get('participant_protocol'))
    dataset_info=task_details.get('dataset_info',task_details_raw.get('dataset_info'))
    learning_algorithm=task_details.get('learning_algorithm',task_details_raw.get('learning_algorithm'))
    align=task_details.get('align',task_details_raw.get('align'))
    pretreatment=task_details.get('pretreatment',task_details_raw.get('pretreatment'))
    train_proportion=task_details.get('train_proportion',task_details_raw.get('train_proportion'))
    features=task_details.get('features',task_details_raw.get('features'))
    task_progress=task_details.get('task_progress',task_details_raw.get('task_progress'))
    display_location=task_details.get('display_location',task_details_raw.get('display_location'))
    auc=task_details.get('auc',task_details_raw.get('auc'))
    ks=task_details.get('ks',task_details_raw.get('ks'))
    psi=task_details.get('psi',task_details_raw.get('psi'))
    result_file=task_details.get('result_file',task_details_raw.get('result_file'))
    result_data=task_details.get('result_data',task_details_raw.get('result_data'))
    sql = '''DELETE from %s.%s
                where task_id = %s''' % (databasename, tablename, task_id)
    conn.begin()
    cur.execute(sql)
    conn.commit()
    sql='''insert into %s.%s (task_id,task_name,project_name,model_name,ip,port_num,protocol,participant_name,participant_ip,
    participant_port,participant_protocol,dataset_info,learning_algorithm,align,pretreatment,train_proportion,features,
    task_progress,display_location,auc,ks,psi,result_file,result_data,create_time,operation_time) values (%s,\'%s\',\'%s\',
    \'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',%f,%f,%f,\'%s\',
    \'%s\',\'%s\',\'%s\')'''%(databasename,tablename,task_id,task_name,project_name,model_name,ip,port,protocol,participant_name,
    participant_ip,participant_port,participant_protocol,dataset_info,learning_algorithm,align,pretreatment,train_proportion,features,
    task_progress,display_location,auc,ks,psi,result_file,result_data,create_time,operation_time)
    try:
        conn.begin()
        cur.execute(sql)
        conn.commit()
        print('任务创建成功，任务ID：%s，任务名称：%s'%(task_id,task_name))
    except Exception as e:
        print(e)
        return task_id
    cur.close()
    conn.close()
    return task_id


# %%
# 从Mysql数据库取数
def dataFetchMysql(databasename, tablename):
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


# %%
# 从oracle数据库取数
def dataFetchOracle(databasename, tablename):
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
    signIn('jc1', 'jc')
    t=taskList()
    trainTaskList()
    taskDetails(1, 'test')
    predictTaskList()
    task_details = {'task_name': 'test'}
    initiateTask({'task_name': 'test'})