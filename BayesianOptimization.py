# encoding:utf-8
"""
这是贝叶斯优化封装的类
作者：Saferman
爱人：纯洁花
"""
import os
import subprocess
import platform
import numpy as np

class BayesianOptimization:
    def __init__(self, resultFile="bayesian.txt",goalFunc = None, initX = [], X = np.linspace(0, 40, 41), plot=False):
        # 保存结果
        self.resultFile = resultFile
        # 执行函数
        self.goalFunc = goalFunc
        # 初始采样点
        self.initX = initX
        # 初始采样点采样结果
        self.initY = []
        # 保存结果
        self.resultString = ""
        # 自变量的全部取值空间
        self.X = X
        # 记录所有采样过的点和采样值,包括正式和初始
        self.xobs = []
        self.yobs = []
        # 记录正式采样过程中当前最大的采样点和采样值
        self.W = 0
        self.xbest = 0
        # 记录每次正式采样过程中最大的W值
        self.allW = []
        self._init()
        # 是否要将结果按照画图展示
        self.plot = plot
        pass

    def _init(self):
        if os.path.exists(self.resultFile):
            os.remove(self.resultFile)

    def _sampling(self, x):
        y = self.goalFunc(x)
        self.xobs.append(x)
        self.yobs.append(y)
        return y

    def _meetStop(self, stopNum = 10):
        # 指定终止条件
        if len(self.allW) < stopNum:
            pass
        else:
            recentW = self.allW[-stopNum:]
            if len(set(recentW)) == 1:
                return True
        if (len(self.xobs)) == len(self.X):
            return True
        return False

    def output(self):
        self.resultString += "初始采样点:"  + str(self.initX) + "\n"
        self.resultString += "初始样本值：" + str(self.initY) + "\n"
        self.resultString += "最大性能值：" + str(self.W)   + "\n"
        self.resultString += "最大性能值采样点" + str(self.xbest) + "\n"
        self.resultString += "采样点全过程:" + str(self.xobs) + "\n"
        self.resultString += "采样值全过程:" + str(self.yobs) + "\n"
        self.resultString += "收敛次数：" + str(self.xobs.index(self.xbest)) + "\n"
        with open(self.resultFile, "w") as f:
            f.write(self.resultString)

        if self.plot:
            self._plot()

    def _plot(self, count = 5):
        if 'windows' in platform.platform().lower():
            pass

    def optimize(self):
        # 初始采样
        for x in self.initX:
            y = self._sampling(x)
            self.initY.append(y)

        self.xobs = self.initX
        self.yobs = self.initY

        # 贝叶斯优化采样
        while not self._meetStop():
            # 存放所有X中未采样过的点
            other_x = [item for item in self.X if item not in self.xobs]
            K = self.k(self.xobs, self.xobs)
            K_s = self.k(self.xobs, other_x)
            K_ss = self.k(other_x, other_x)
            K_sTKinv = np.matmul(K_s.T, np.linalg.pinv(K))

            mu_s = self.m(other_x) + np.matmul(K_sTKinv, self.yobs - self.m(self.xobs))
            Sigma_s = K_ss - np.matmul(K_sTKinv, K_s)
            sigma_s = np.diag(Sigma_s)
            next_sampling_x = self.acq(mu_s, sigma_s)

            x = other_x[next_sampling_x ]
            y = self._sampling(x)   # 这个函数会添加x,y到yobs和xobs里
            W = max(self.yobs)
            if W > self.W:
                self.W = W
                self.xbest = x
            self.allW.append(W)
        # 保存结果
        self.output()

    def polyfit(x, y, degree):
        results = {}
        coeffs = np.polyfit(x, y, degree)
        f = np.poly1d(coeffs)
        results['function'] = f
        results['polynomial'] = coeffs.tolist()

        # r-squared
        p = np.poly1d(coeffs)
        # fit values, and mean
        yhat = p(x)  # or [p(z) for z in x]
        ybar = np.sum(y) / len(y)  # or sum(y)/len(y)
        ssreg = np.sum((yhat - ybar) ** 2)  # or sum([ (yihat - ybar)**2 for yihat in yhat])
        sstot = np.sum((y - ybar) ** 2)  # or sum([ (yi - ybar)**2 for yi in y])
        results['determination'] = ssreg / sstot  # 准确率
        return results

    def acq(self, mu_s, sigma_s, beta=2):
        # 根据最大收获函数返回下一个采样最可能的位置
        eva = mu_s + sigma_s * beta
        return np.where(eva == np.max(eva))[0][0]

    def m(self, x):
        """The mean function. As discussed, we can let the mean always be zero"""
        return np.zeros_like(x)

    def k(self, xs, xs2, sigma=1, l=1):

        # Pairwise difference matrix
        dx = np.expand_dims(xs, 1) - np.expand_dims(xs2, 0)
        return (sigma ** 2) * np.exp(-((dx / 1) ** 2) / 2)


if __name__ == "__main__":
    x = [0, 1, 5, 10, 17, 20, 24, 26, 30, 34, 36, 38, 40]
    y = [-95, -40, 8, 20, 43, 48, 54, 47, 22, 22, 24, 22, 21]


    def polyfit(x, y, degree):
        results = {}
        coeffs = np.polyfit(x, y, degree)
        f = np.poly1d(coeffs)
        results['function'] = f
        results['polynomial'] = coeffs.tolist()

        # r-squared
        p = np.poly1d(coeffs)
        # fit values, and mean
        yhat = p(x)  # or [p(z) for z in x]
        ybar = np.sum(y) / len(y)  # or sum(y)/len(y)
        ssreg = np.sum((yhat - ybar) ** 2)  # or sum([ (yihat - ybar)**2 for yihat in yhat])
        sstot = np.sum((y - ybar) ** 2)  # or sum([ (yi - ybar)**2 for yi in y])
        results['determination'] = ssreg / sstot  # 准确率
        return results

    z1 = polyfit(x, y, 8)
    all_x = np.linspace(0, 40, 100)
    f = z1['function']

    bo = BayesianOptimization( resultFile="bayesian.txt",goalFunc = f, initX = [0, 10, 20, 30] , X = np.linspace(0, 40, 41))
    bo.optimize()


