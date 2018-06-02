# encoding:utf-8
# 参考文献：贝叶斯优化调参 笔记前面这些链接，代码来自http://36kr.com/p/5114423.html
import numpy as np
import matplotlib.pyplot as plt
import os

x_obs = [0, 10, 20, 30] # 初始值  训练数据  会变化
y_obs = []  # 初始值  训练数据  会变化


# def f(x):
#     execute_time = 0.0
#     r = os.popen("")
#     r.read()
#     return execute_time

from curve_fitting import f

for x in x_obs:
    y = f(x)
    y_obs.append(y)

print y_obs










