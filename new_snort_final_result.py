# encoding:utf-8
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
mpl.rc('font', family='Times New Roman')
exps = [None,'Ex1','Ex2','Ex3','Ex4','Ex5','Ex6']
t = [4.9, 4.7, 4.0, 2.7, 1.8, 4.2]  # 单 位 H
m = np.array([19,20,19,16,14,20])  #
e = np.array([0,0,0,0,0,80])  #
x = [1,2,3,4,5,6]

fontsize = 10.5
fig=plt.figure()
ax1 = fig.add_subplot(111)
lns1 = ax1.plot(x, t, "deepskyblue", marker="o", label="t (hour)")
ax1.set_xticklabels(exps, fontsize=fontsize)
ax1.set_ylabel("t(hour)", fontsize=fontsize)
ax1.set_ylim(0.0,6.0)
ax1.set_yticklabels([0.0,1.0,2.0,3.0,4.0,5.0,6.0], fontsize=fontsize)
ax1.grid()
plt.yticks(fontsize=fontsize)

ax2 = ax1.twinx()
lns2 = ax2.plot(x, m/100.0, "tomato", marker="*",label="m (%)",linestyle="--")
lns3 = ax2.plot(x, e/100.0, "y", marker="x",label="e (%)", linestyle="-.")

lns = lns1+lns2 +lns3
labs = [l.get_label() for l in lns]
ax2.legend(lns,labs,loc="upper center", fontsize=fontsize)
ax2.set_ylabel("m(%)  e(%)", fontsize=fontsize)
plt.yticks(fontsize=fontsize)

plt.show()