from client.iAo import FetchAndQuery as FAQ

global tasklist
tasklist = []


def save_task(task_info,tag):
    add_task = {}
    info_list = ['taskname', 'alian_feature', 'ip', 'port', 'learningAlgorithm', 'modelname', 'trainratio', 'partnername']
    add_list = ['task_name', 'align', 'participant_ip', 'participant_port', 'learning_algorithm', 'model_name', 'train_proportion','participant_name']
    for x,y in zip(info_list,add_list):
        add_task[y] = task_info[x]
    if tag == 'train':
        add_task['task_progress'] = '待对方加入训练'
    else:
        add_task['task_progress'] = '待对方加入预测'
    FAQ.initiateTask(add_task)
    # 发到对面 todo


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