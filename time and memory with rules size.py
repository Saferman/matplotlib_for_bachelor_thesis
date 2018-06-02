# encoding:utf-8
# Snort性能指标随流量大小和规则集合大小的变化情况
# https://www.zhihu.com/question/25404709  中文方格解决思路
import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']
import numpy as np
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# 2G内存，200M流量
x = [0,200,400,600,800,1000] # 单位M
y1 = [7, 42, 79, 110, 147, 173]
y2 = [0.03,0.13,0.22,0.31,0.4,0.48]
font_chinese={'family':'STSong',
              'weight':'normal',
              'size':10.5}

for j in xrange(0, len(y1)):
    y1[j] = y1[j]/200.0
    print y1[j]

name = u'耗时和内存随规则集合大小的变化'

plt.figure(figsize=(5,5), dpi=80, facecolor="w", edgecolor='g')
plt.title(name,font_chinese)
plt.plot(x,y1,marker="o",color='red',linestyle='-',linewidth=0.5,label=u'耗时/300（秒）')
plt.plot(x,y2,marker="o",color='blue',linestyle='-',linewidth=0.5,label=u'内存使用率')
plt.grid(True, axis='both')
plt.axis([0,1000,0,1])
plt.xlabel(u"规则集合大小（M）",font_chinese)
plt.xticks(x)
plt.yticks([0,0.2,0.4,0.6,0.8,1.0])
plt.legend(loc='best',prop=font_chinese)
plt.title(name)
plt.show()

