from server.ml import lr

import rsa

def train1(keyAndu):
    ppk_b = keyAndu[0]
    ub_list= keyAndu[1]
    spk_u_list = lr.lr1(ub_list,ppk_b)
    return spk_u_list


def train2(a):
    return []


def train3(a):
    return []


