from server.ml import lr

import rsa

def tarin1(keyAndu):
    ppk_b = keyAndu[0]
    ub_list= keyAndu[1]
    u_list = lr.lr1(ub_list,ppk_b)
    return u_list
