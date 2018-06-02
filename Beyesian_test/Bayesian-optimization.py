# encoding:utf-8
# 参考文献：贝叶斯优化调参 笔记前面这些链接，代码来自http://36kr.com/p/5114423.html
import numpy as np
from getOBS import f

def k(xs,xs2,sigma=1,l=1):

    # Pairwise difference matrix
    dx = np.expand_dims(xs,1)-np.expand_dims(xs2,0)
    return (sigma ** 2) - np.exp(-((dx / 1) ** 2) / 2)


def m(x):
    """The mean function. As discussed, we can let the mean always be zero"""
    return np.zeros_like(x)

def acq(mu_s, sigma_s, beta=2):
    # 根据最大收获函数返回下一个采样最可能的位置
    eva = mu_s + sigma_s * beta
    return np.where(eva == np.max(eva))[0][0]

stop_w = []
def stop():
    if len(stop_w) < 3:
        pass
    else:
        recent_w = stop_w[-3:]
        if recent_w[0] == recent_w[1] and recent_w[1] == recent_w[2]:
            return True
    if len(x_obs) == len(X):
        return True
    return False

x = 0 # 储存当前采样点
y = 0 # 储存当前采样点经过f的结果
W = 0 # 储存次数最大的f执行结果
X = np.linspace(-5.0, 2, 50) # 变量全部取值空间
other_x = [] # 存放所有不在x_obs的x

xs = [] # 采样点 只起记录的作用和x_obs额外增加的元素同步
fs = [] # 样本点
x_obs = [-4,-2,0] # 初始值  训练数据  会变化
y_obs = [4.48, 4.44, 6.0]  # 初始值  训练数据  会变化


while not stop():
    other_x = [item for item in X if item not in x_obs]
    K = k(x_obs, x_obs)
    K_s = k(x_obs, other_x)
    K_ss = k(other_x, other_x)
    K_sTKinv = np.matmul(K_s.T, np.linalg.pinv(K))
    mu_s = m(other_x) + np.matmul(K_sTKinv, y_obs-m(x_obs))
    Sigma_s = K_ss - np.matmul(K_sTKinv, K_s)
    sigma_s = np.diag(Sigma_s)
    next_pos = acq(mu_s, sigma_s)

    x = other_x[next_pos]
    y = f(x)
    xs.append(x)
    fs.append(y)
    x_obs.append(x)
    y_obs.append(y)
    W = max(y_obs)
    stop_w.append(W)

print "性能最大值: ",W
print "使得性能最大的采样点: ",x_obs[y_obs.index(W)]
print "采样过程: ", xs






