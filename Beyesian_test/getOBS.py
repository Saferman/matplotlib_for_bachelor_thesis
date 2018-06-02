# encoding:utf-8
# 参考文献：贝叶斯优化调参 笔记前面这些链接，代码来自http://36kr.com/p/5114423.html
import numpy as np
import matplotlib.pyplot as plt

x_obs = [-4,-2,0] # 初始值  训练数据  会变化
y_obs = []  # 初始值  训练数据  会变化

coefs = [6, -2.5, -2.4, -0.1, 0.2, 0.03]

def f(x):
    total  = 0
    for exp, coef in enumerate(coefs):
        total += coef * (x ** exp)
    return total

for x in x_obs:
    y = f(x)
    y_obs.append(y)

print y_obs

xs = np.linspace(-5.0, 3.5, 100)
ys = f(xs)
plt.figure()
plt.plot(xs, ys)
plt.show()












