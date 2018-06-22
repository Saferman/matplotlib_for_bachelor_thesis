# encoding:utf-8
# 参考文献：贝叶斯优化调参 笔记前面这些链接，代码来自http://36kr.com/p/5114423.html
import numpy as np
# import matplotlib.pyplot as plt
import os
from snort_func import output

x_obs = [0.0, 10.0, 20.0, 30.0] # 初始值  训练数据  会变化
y_obs = []  # 初始值  训练数据  会变化

# def f(x):
#     return x


from snort_func import f

for x in x_obs:
    y = f(x)
    y_obs.append(y)

output("初始点：")
output(x_obs)
output(y_obs)










