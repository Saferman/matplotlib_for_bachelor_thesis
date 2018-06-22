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
    global_conf = "/usr/local/snort/rules/rules/etc/snort.conf"
    global_traffic = "/home/lcx/snortEXP/onedayHTTP.pcap"
    def f(x):
        def change_conf(conf = global_conf, x=20):
            with open(conf, "r") as f:
                lines = f.readlines()
            for i in xrange(0, len(lines)):
                if lines[i].find("max-pattern-len") != -1:
                    lines[i] = "config detection: search-method ac-split search-optimize max-pattern-len" + " " + str(x)
                    lines[i] = lines[i] + "\n"
            with open(conf, "w") as f:
                f.writelines(lines)
        y = 0.0
        if 'windows' in platform.platform().lower():
            command = 'net'
            command = command.split()
            child = subprocess.Popen(command, stdout=subprocess.PIPE)
            child.wait()
            return y
        change_conf(x=x)
        command = "snort -d -A fast -r "+ global_traffic +" -c  " + global_conf
        command = command.split()
        child = subprocess.Popen(command, stdout=subprocess.PIPE)
        child.wait()
        with open("time_measure_handled.txt", "r") as f:
            lines = f.readlines()
        for line in lines:
            if line.find("seconds") != -1:
                timeline = line.split()[2]
                y += float(timeline)
        return -1 * y

    # 因为要做十组实验，所以设置配置文件的规则集合
    # 规则集合目录 /usr/local/snort/rules/rules/rules/ownrules/rulesets/
    # 清空配置文件默认指定的所有规则 include $RULE_PATH

    class ruleHandle(object):
        def __init__(self, conf=global_conf):
            self.conf = conf
            self.original_lines = []
            self.clear_lines = []
            self.current_lines = []
            with open(conf, "r") as f:
                self.original_lines = f.readlines()  # 每个元素含有\n
            self.ruleClear()

        def _saveConf(self, temp_lines=[]):
            with open(self.conf, "w") as f:
                f.writelines(temp_lines)

        def ruleClear(self):
            temp_lines = []
            for i in xrange(0, len(self.original_lines)):
                if self.original_lines[i].find("include $RULE_PATH") != -1:
                    temp_lines[i] = "# " + self.original_lines[i]
            self.clear_lines = temp_lines

        def ruleSet(self, rule="/usr/local/snort/rules/rules/rules/ownrules/rulesets/1.rules"):
            self.current_lines = []
            for i in xrange(0, len(self.clear_lines)):
                if self.clear_lines[i].find("# site specific rules") != -1:
                    self.current_lines.append(self.clear_lines[i])
                    new_line = "include " + rule + "\n"
                    self.current_lines.append(new_line)
                else:
                    self.current_lines.append(self.clear_lines[i])

            self._saveConf(self.current_lines)

        def finish(self):
            self._saveConf(self.original_lines)


    ruleH = ruleHandle()

    for i in xrange(1,11):
        rule = "/usr/local/snort/rules/rules/rules/ownrules/rulesets/%d.rules" % i
        ruleH.ruleSet(rule)
        bo = BayesianOptimization(resultFile="bayesian"+str(i)+".txt", goalFunc=f, initX=[0, 10, 20, 30],
                                  X=np.linspace(0, 40, 41))
        bo.optimize()

    ruleH.finish()






