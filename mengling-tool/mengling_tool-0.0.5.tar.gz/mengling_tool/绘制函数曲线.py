# import matplotlib.pyplot as plt
# import math
# import numpy as np
#
# plt.figure(1)
#
# x = []
# y = []
#
# # a=np.linspace(1,10,100)
# '''
# for i in range(1,2000):
#     x.append(i)
#     y.append(20*5000*(1000+i)/(i**2+20))
#     print(str(i)+":"+str(round(20*5000*(1000+i)/(i**2+20))))
# plt.plot(x, y)
# plt.show()
# '''
# k = 140
# t = 400
# i1 = 30
# i2 = 1000
#
# temp = 10
# qu = []
# s = []
# for x in range(30, 1001):
#     y = int(round(k * x / (t + x), 0))
#     if temp == y:
#         qu.append(x)
#     else:
#         s.append("[" + str(qu[0]) + "~" + str(qu[-1]) + "]" + ":" + str(temp))
#         qu.clear()
#         qu.append(x)
#         temp = y
# s.append("[" + str(qu[0]) + "~" + str(qu[-1]) + "]" + ":" + str(temp))
# kong = 8
# i = 0
# temp = ""
# temp1 = ""
# for q in range(0, len(s)):
#     temp = s[q]
#     temp1 += temp
#     if i < 2:
#         for k in range(0, kong - len(temp) + 10): temp1 += " "
#         i += 1
#     else:
#         i = 0
#         print(temp1)
#         temp1 = ""
