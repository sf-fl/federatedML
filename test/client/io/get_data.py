import pandas as pd
import os
import cx_Oracle
import pymysql
import configparser


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
    conn = cx_Oracle.connect(uid,pwd,host+':'+port+'/'+service)
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