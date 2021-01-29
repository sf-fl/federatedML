from client.iAo import FetchAndQuery as FAQ
from client.proxy import client_proxy as cp

global tasklist
tasklist = []


def save_task(task_info, tag, tag2):
    add_task = {}
    info_list = ['taskname', 'alian_feature', 'ip', 'port', 'learningAlgorithm', 'modelname', 'partnername']
    add_list = ['task_name', 'align', 'participant_ip', 'participant_port', 'learning_algorithm', 'model_name', 'participant_name']
    if tag == 'train':
        info_list.append('trainratio')
        add_list.append('train_proportion')
    if tag2 ==  'append':
        info_list.append('id')
        add_list.append('task_id')
    for x,y in zip(info_list,add_list):
        add_task[y] = task_info[x]
    if tag2 == 'add':
        if tag == 'train':
            add_task['task_progress'] = '待对方加入训练'
        else:
            add_task['task_progress'] = '待对方加入预测'
        id = FAQ.initiateTask(add_task)
        task_send = FAQ.taskDetails(id).T.to_dict()[0]
        cp.addTask(task_send,tag)
    else:
        if tag == 'train':
            add_task['task_progress'] = '训练中'
        else:
            add_task['task_progress'] = '预测中'
        FAQ.changeTask(add_task)
        cp.begintask(add_task,tag)

    # 发到对面 todo

def receive_task(task_info,tag):
    if tag == 'train':
        task_info['task_progress'] = '待我方加入训练'
    else:
        task_info['task_progress'] = '待我方加入预测'
    FAQ.changeTask(task_info)

def show_task_list(type):
    if type == 'apply':
        return FAQ.appendTaskList()
    return FAQ.taskList()


def show_task_info(id):
    return FAQ.taskDetails(id)


def login(account, password):
    # 和iAo交互
    flag = 'fail'
    if FAQ.signIn(account, password):
        flag = 'success'
    return flag