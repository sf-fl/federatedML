
global task
task = []


def save_task(task_info):
    global task
    task.append(task_info)

def show_task_list():
    global task