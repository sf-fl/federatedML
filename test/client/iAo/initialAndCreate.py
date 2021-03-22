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
    db_nickname='sys'
    config = configparser.ConfigParser()
    config.read(os.path.join(os.getcwd(), 'config/dbconfig.conf'))
    uid = config.get(db_nickname, 'uid')
    pwd = config.get(db_nickname, 'pwd')
    host = config.get(db_nickname, 'ip')
    port = config.get(db_nickname, 'port')
    databasename=config.get(db_nickname, 'databasename')
    # service=config.get(databasename,'service')
    # 连接数据库
    tag = 0
    try:
        conn = pymysql.connect(host=host, port=int(port), user=uid, password=pwd, database=databasename, charset='utf8')
        print('连接数据库成功！')
    except Exception as e:
        print(e)
        return(tag)
    cur=conn.cursor()
    # 建用户表 todo 主键，三者分离
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
    port_num varchar(50), -- 我方端口
    protocol  varchar(50), -- 我方协议
    participant_name varchar(100), -- 参与方名称
    participant_ip varchar(50), -- 参与方ip
    participant_port varchar(50), -- 参与方端口
    participant_protocol varchar(50), -- 参与方协议
    dataset_info varchar(200), -- 我方数据集来源信息
    learning_algorithm varchar(50), -- 机器学习算法
    align varchar(50), -- 对齐方式，按照哪个字段对齐
    pretreatment varchar(50), -- 预处理方法概览
    -- encode varchar(50), -- 编码方式
    -- normalization varchar(50), -- 归一化方法
    -- cross_proportion varchar(50), -- 交叉验证比例
    train_proportion varchar(50), -- 训练验证测试集比例
    features varchar(1000), -- 使用的特征
    task_progress varchar(50), -- 任务进度：待审批训练、待加入训练、训练中、训练完、待审批预测、待加入预测、预测中、预测完
    display_location varchar(500), -- 展示结果保存位置
    auc double,
    ks double,
    psi double,
    result_file varchar(200), -- 结果文件保存位置
    result_data varchar(200), -- 数据库结果保存位置
    create_time varchar(200), -- 任务创建时间
    operation_time varchar(200) -- 任务最后操作时间
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


# %%
# 注册新账号
def Register(username,passwd,identity):
    db_nickname='sys'
    tablename='account'
    config = configparser.ConfigParser()
    config.read(os.path.join(os.getcwd(),'config/dbconfig.conf'))
    uid = config.get(db_nickname, 'uid')
    pwd = config.get(db_nickname, 'pwd')
    host = config.get(db_nickname, 'ip')
    port = config.get(db_nickname, 'port')
    databasename = config.get(db_nickname, 'databasename')
    # service=config.get(databasename,'service')
    # 连接数据库
    tag = 0
    try:
        conn = pymysql.connect(host=host, port=int(port), user=uid, password=pwd, database=databasename, charset='utf8')
        print('连接数据库成功！')
    except Exception as e:
        print(e)
        return(tag)
    cur = conn.cursor()
    # 读取当前表，判断用户是否已注册，并确定用户ID
    try:
        cur.execute('select * from %s.%s' % (databasename, tablename))
        user_list = [acc[1] for acc in cur.fetchall()]
        if username not in user_list:
            accountid = len(user_list)+1
            print('账户ID为：%d' % accountid) # todo 用户删除导致listbug
        else:
            print('账户已存在：%s' % username)
            return(tag)
    except Exception as e:
        print(e)
        return(tag)
    # 执行插入和更新
    create_time=dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql='insert into %s.%s (accountid,username,passwd,identity,create_time) values (%d,\'%s\',\'%s\',\'%s\',\'%s\');' \
        % (databasename,tablename,accountid,username,passwd,identity,create_time)
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

