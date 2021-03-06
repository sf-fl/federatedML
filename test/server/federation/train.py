from server.ml import lr


def train1(keyAndu):
    ppk_b = keyAndu[0]
    ub_list= keyAndu[1]
    spk_u_list = lr.lr1(ub_list,ppk_b)
    return spk_u_list


def train2(grad):
    gradB_pa = grad[0]
    gradA_r = grad[1]
    spk_u_list = lr.lr2(gradB_pa, gradA_r)
    return spk_u_list


def predict(ub_list):
    result = lr.pre(ub_list)
    return result

def save(id):
    lr.save(id)
    return {'result':'success'}


def train3(grad):
    gradB_pa = grad[0]
    gradA_r = grad[1]
    gradB_r = lr.lr3(gradB_pa,gradA_r)
    return gradB_r


