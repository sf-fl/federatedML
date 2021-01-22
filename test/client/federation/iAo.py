from client.iAo import FetchAndQuery as FAQ

global tasklist
tasklist = []


def save_task(task_info):
    add_task = {}
    info_list = ['taskname', 'alian_feature', 'ip', 'port', 'learningAlgorithm', 'modelname', 'trainratio', 'partnername']
    add_list = ['task_name', 'align', 'participant_ip', 'participant_port', 'learning_algorithm', 'model_name', 'train_proportion','participant_name']
    for x,y in zip(info_list,add_list):
        add_task[y] = task_info[x]
    add_task['task_progress'] = '对方待加入'
    FAQ.initiateTask(add_task)
    # 发到对面 todo


def show_task_list():
    return FAQ.appendTaskList()


def login(account, password):
    # 和iAo交互
    flag = 'fail'
    if FAQ.signIn(account, password):
        flag = 'success'
    return flag