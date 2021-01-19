import pandas as pd
import os
import cx_Oracle
import pymysql
import configparser
import datetime as dt

# 注册新账号
def Register(user,password,identity):
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

#%%
# 发起训练
def InitiateTraining(task_name,mode_name,):
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