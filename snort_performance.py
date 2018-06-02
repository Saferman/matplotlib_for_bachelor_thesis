# encoding:utf-8
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rc('font', family='Times New Roman')
import numpy as np
fontsize=10.5
x = [100,200,300,400,500,600,700,800]  # Mbps
e = [0,0,0,5,15,30,42,52]
Fv = [100,200,300,320,320,320,312,308]
fig = plt.figure()
ax1 = fig.add_subplot(111)
lns1=ax1.plot(x, Fv, color='#ADD8E6', marker="o",label="Fv (Mbps)")
ax1.set_ylabel("Fv(Mbps)",fontsize=fontsize)
ax1.set_xlabel("Mbps")
plt.xticks(fontsize=fontsize)
plt.yticks(fontsize=fontsize)
# plt.legend(loc="upper left",fontsize=10.5)
ax2 = ax1.twinx()
lns2=ax2.plot(x, np.array(e)/100.0 ,"brown", marker="x",label="e (%)")
# plt.legend(loc=(0,500),fontsize=10.5)
lns = lns1+lns2
labs = [l.get_label() for l in lns]
ax2.legend(lns,labs,loc=0, fontsize=fontsize)
ax2.set_ylabel("e(%)", fontsize=fontsize)
ax2.grid()
plt.yticks(fontsize=fontsize)
plt.show()
