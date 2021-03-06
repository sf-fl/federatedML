from client.federation import iAo
import copy

fenye = 10


def update_taskdf(type):
    tasklist = iAo.show_task_list(type)

    if type == 'apply':
        col = {'task_id': 'taskID','task_name': 'taskName', 'participant_name': 'partner',
               'learning_algorithm': 'learningType',
               'task_progress': 'taskState', 'operation_time': 'lastModifyTime'}
        tasklist.rename(columns=col, inplace=True)
        tasklist['taskState_ID'] = tasklist['taskState']+'__'+tasklist['taskID'].map(str)

    if type == 'execute':
        col = {'task_id': 'taskID', 'task_name': 'taskName', 'participant_name': 'partner',
               'learning_algorithm': 'learningType',
               'task_progress': 'taskState', 'operation_time': 'lastModifyTime'}
        tasklist.rename(columns=col, inplace=True)
        tasklist['taskState_ID'] = tasklist['taskState'] + '__' + tasklist['taskID'].map(str)

    return tasklist


def gettasklist(page,type):
    taskdf = update_taskdf(type)
    total = len(taskdf)
    start = (page-1)*fenye
    if page*fenye < total:
        result_df = taskdf.iloc[start:page*fenye, :]
    else:
        result_df = taskdf.iloc[start:, :]
    result_list = list(result_df.T.to_dict().values())
    return {'data': result_list, 'total': total}


def get_append_task(id):
    taskinfo = iAo.show_task_info(id)
    result = taskinfo[['task_id','task_name','model_name','participant_ip','participant_port',
                       'learning_algorithm','participant_name','align','train_proportion']]
    col = {'task_id': 'id', 'task_name': 'taskname', 'participant_name': 'partnername',
           'learning_algorithm': 'learningAlgorithm','participant_ip':'ip','participant_port':'port',
           'train_proportion': 'trainratio', 'align': 'alian_feature','model_name':'modelname'}
    result.rename(columns=col, inplace=True)
    resultlist = list(result.T.to_dict().values())
    return resultlist


def get_train_info(id):
    taskinfo = iAo.show_task_info(id)
    result = taskinfo.loc[:,['task_id','task_name','model_name','project_name','create_time',
                       'participant_ip','participant_port','ip','port_num','operation_time',
                       'learning_algorithm','participant_name','align','train_proportion','auc','ks']]
    col = {'task_id': 'taskID', 'task_name': 'taskname', 'participant_name': 'partnername',
           'learning_algorithm': 'MLA','participant_ip':'partnerIP','participant_port':'partnerPort',
           'ip': 'userIP', 'port_num': 'userPort','create_time': 'createtime', 'operation_time': 'lastmodify',
           'train_proportion': 'trainratio', 'align': 'alianfeature','model_name':'modelname',
           'project_name':'projectname','ks': 'ks','auc': 'auc'}
    result.rename(columns=col, inplace=True)
    result.loc[:,'userIPPort'] = result.loc[:,'userIP'] + ':' + result.loc[:,'userPort']
    result.loc[:,'partnerIPPort'] = result.loc[:,'partnerIP'] + ':' + result.loc[:,'partnerPort']
    resultlist = list(result.T.to_dict().values())
    return resultlist

def get_train_detail(id):
    with open(r'./client/data_storage/train_step_%s.log' % id, 'r', encoding='UTF-8') as f1:
        step = f1.read()
    with open(r'./client/data_storage/train_detail_%s.log' % id, 'r', encoding='UTF-8') as f2:
        detail = f2.read()
    return {'step': step, 'detail': detail}
