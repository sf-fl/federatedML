from client.federation import iAo
import copy

tasklist1 =[
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


def update_taskdf(type):
    tasklist = iAo.show_task_list()
    col = {'task_id':'taskID','task_name':'taskName', 'participant_name':'partner', 'learning_algorithm':'learningType',
           'task_progress':'taskState', 'operation_time':'lastModifyTime'}
    tasklist.rename(columns=col, inplace=True)
    return tasklist


def gettasklist(page):
    update_taskdf()
    total = len(tasklist1)
    start = (page-1)*fenye
    if page*fenye<total:
        result_list = tasklist1[start:page*fenye]
    else:
        result_list = tasklist1[start:]
    return {'data':result_list,'total':total}


def getapplylist(page):
    taskdf = update_taskdf('apply')
    total = len(taskdf)
    start = (page-1)*fenye
    if page*fenye<total:
        result_df = taskdf.iloc[start:page*fenye,:]
    else:
        result_df = taskdf.iloc[start:,:]
    result_list = list(result_df.T.to_dict().values())
    return {'data':result_list,'total':total}