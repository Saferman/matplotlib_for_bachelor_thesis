# encoding:utf-8
# coding:utf-8
import matplotlib.pyplot as plt
import numpy as np

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#  问题 除了label，其余中文不能正常显示
# # 失败的解决方法一·
# # https://yongyuan.name/blog/matplotlib-title-using-Chinese.html
# from matplotlib.font_manager import FontProperties
# font = FontProperties(fname=r"c:\SimSun.ttc", size=10.5)

# 解决方案https://segmentfault.com/a/1190000005144275
import matplotlib as mpl
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = 'SimSun,Times New Roman'
# mpl.rcParams['axes.unicode_minus'] = False   # 步骤二（解决坐标轴负数的负号显示问题）

x = np.array([1,2,3,4,5])
y = np.array([1,2,3,4,5])
plt.plot(x, y, '+', label='PoW算法', color='black',fontsize=10.5)

plt.xlabel(u'难度值',fontsize=10.5)
plt.ylabel(u'时间',fontsize=10.5)
plt.title(u'PoW共识的hash难题解决时间表',fontsize=10.5)
plt.legend()
plt.show()