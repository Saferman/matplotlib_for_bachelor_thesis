# encoding:utf-8
import numpy
import matplotlib.pyplot as plt
'''
500M规则 、 160G流量
W = (1-m) *  (1 - t/avg_t) * 100 - e * 100
max-pattern-len 取值范围 0 - 40 整数
取值  W  m   t/avg_t   e  
0    -95  10           100   
1    -40   12          80
5     8  14          45
10    20   16    3/4      0
17    43    18          0
20    48     20
24    54   22   1/3
26     47    22
30    22     22
34    22
36     23     22
38     22
40     21   22
'''
x = [0,1,5,10,17,20,24,26,30,34,36,38,40]
y = [-95,-40,8,20,43,48,54,47,22,22,24,22,21]

def polyfit(x, y, degree):
    results = {}
    coeffs = numpy.polyfit(x, y, degree)
    f = numpy.poly1d(coeffs)
    results['function'] = f
    results['polynomial'] = coeffs.tolist()

    # r-squared
    p = numpy.poly1d(coeffs)
    # fit values, and mean
    yhat = p(x)  # or [p(z) for z in x]
    ybar = numpy.sum(y) / len(y)  # or sum(y)/len(y)
    ssreg = numpy.sum((yhat - ybar) ** 2)  # or sum([ (yihat - ybar)**2 for yihat in yhat])
    sstot = numpy.sum((y - ybar) ** 2)  # or sum([ (yi - ybar)**2 for yi in y])
    results['determination'] = ssreg / sstot  # 准确率
    return results

# x=[ 1 ,2  ,3 ,4 ,5 ,6]
# y=[ 2.5 ,3.51 ,4.45 ,5.52 ,6.47 ,7.2]
z1 = polyfit(x, y, 8)
all_x = numpy.linspace(0,40,100)
f = z1['function']
print z1
if __name__=='__main__':
    print f(20)
    plt.figure()
    plt.plot(x, y, linestyle='None', marker="*")
    plt.plot(all_x, f(all_x))
    plt.show()

