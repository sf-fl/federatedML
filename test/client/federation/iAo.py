
global tasklist
tasklist = []


def save_task(task_info):
    global tasklist
    tasklist.append(task_info)

def show_task_list():
    global task
    pass

def login(account,password):
    # 和iAo交互
    flag = 'fail'
    if account == 'admin' and password == 'password':
        flag = 'success'
    return flag