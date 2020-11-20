
import time
import numpy as np
from client.eAd import paillier


def cal_u2(theta,x,y)
    return np.dot(theta.T, x) - 2 * pow(10,6) * y

def update_grad(theta_a,x_a,*y_a):
    u_list = []
    for t,x,y in zip(theta_a,x_a,y_a):
        u = cal_u2(t,x,y)



def update_theta(grad, theta, alpha):
    pass


def logistic_regression(X, y):
    """
    逻辑回归算法
    :param X: mxn矩阵
    :param y: mx1矩阵
    :return: nx1矩阵
    """
    start = time.time()
    m = X.shape[0]  # 样本个数
    n = X.shape[1]  # 特征个数
    y = y.reshape(m, 1)
    # cost_record = []  # 记录代价函数的值
    alpha = 0.1  # 学习率
    maxiters = 1000  # 最大迭代次数
    theta = np.zeros(n).reshape(n, 1)  # 设置权重参数的初始值
    # cost_val = cosst_function(theta, X, y)
    # cost_record.append(cost_val)
    iters = 0
    while True:
        if iters >= maxiters:
            break
        grad = update_grad(theta, X, y)
        # 权重参数更新
        new_theta = update_theta(grad, theta, alpha)
        theta = new_theta
        # cost_update = cosst_function(new_theta, X, y)
        # cost_val = cost_update
        # cost_record.append(cost_val)
        iters += 1
    end = time.time()
    print("cost time: %f s" % (end - start))
    return theta, iters