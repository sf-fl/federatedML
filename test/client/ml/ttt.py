import time

t = time.time()  # 程序起始时间


def foo(a, b):
    k = 0
    for i in range(a, b):
        k += i
    return k

def double_cir(a,b):
    t= 0
    for i in range(a):
        for j in range(b):
            t += 1
    return t

# print(foo(1, 100000000))
print(double_cir(10000,10000))
print(time.time() - t)  # 输出程序运行结束时消耗时间