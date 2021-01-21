from client.federation import iAo
import copy

tasklist =[
    {
  "taskID": "A17B13",
    "taskName":"京东联邦学习测试项目",
    'partner':'京东数科',
  "lastModifyTime": "2021-01-21 05:11:52",
  "learningType": "VLR",
  "taskState": 2
},
    {
  "taskID": "A15B14",
    "taskName":"内部测试",
    'partner':'上汽财务',
  "lastModifyTime": "2021-01-21 05:11:52",
  "learningType": "VSB",
  "ipAddress": "127.0.0.1",
  "taskState": 1
},
    {
  "queryRecordId": "zzzzz",
  "queryDate": "2021-01-21T05:11:52.735Z",
  "userId": "bbbbb",
  "ipAddress": "127.0.0.1",
  "queryType": 2,
  "timeConsuming": 200
},
    {
  "queryRecordId": "zzzzz",
  "queryDate": "2021-01-21T05:11:52.735Z",
  "userId": "bbbbb",
  "ipAddress": "127.0.0.1",
  "queryType": 2,
  "timeConsuming": 200
},
    {
  "queryRecordId": "zzzzz",
  "queryDate": "2021-01-21T05:11:52.735Z",
  "userId": "bbbbb",
  "ipAddress": "127.0.0.1",
  "queryType": 2,
  "timeConsuming": 200
},
    {
  "queryRecordId": "zzzzz",
  "queryDate": "2021-01-21T05:11:52.735Z",
  "userId": "bbbbb",
  "ipAddress": "127.0.0.1",
  "queryType": 2,
  "timeConsuming": 200
}]
fenye = 6


def update_tasklist():
    tasklisk = []
    for showtask in iAo.tasklist:
        onetask = {}
        onetask['taskID'] = showtask['']
        onetask['taskName'] = showtask['']
        onetask['partner'] = showtask['']
        onetask['lastModifyTime'] = showtask['']
        onetask['learningType'] = showtask['']
        onetask['taskState'] = showtask['']
        tasklisk.append(copy.deepcopy(onetask))


def gettasklist(page):
    update_tasklist()
    total = len(tasklist)
    start = (page-1)*fenye
    if page*fenye<total:
        result_list = tasklist[start:page*fenye]
    else:
        result_list = tasklist[start:]
    return {'data':result_list,'total':total}