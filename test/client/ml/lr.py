



def logistic_regression(X, y):
    """
    逻辑回归算法
    :param X: mxn矩阵
    :param y: mx1矩阵
    :return: nx1矩阵
    """
    start = time.clock()
    m = X.shape[0] # 样本个数
    n = X.shape[1] # 特征个数
    y = y.reshape(m, 1)
    cost_record = []  # 记录代价函数的值
    alpha = 0.1  # 学习率
    maxiters = 1000 # 最大迭代次数
    theta = np.zeros(n).reshape(n, 1)  # 设置权重参数的初始值
    cost_val = cosst_function(theta, X, y)
    cost_record.append(cost_val)
    iters = 0
    while True:
        if iters >= maxiters:
            break
        grad = derivative(theta, X, y)
        # 权重参数更新
        new_theta = gradient(grad, theta, alpha)
        theta = new_theta
        cost_update = cosst_function(new_theta, X, y)
        cost_val = cost_update
        cost_record.append(cost_val)
        iters += 1
    end = time.clock()
    print("cost time: %f s" % (end - start))
    return cost_record, theta, iters