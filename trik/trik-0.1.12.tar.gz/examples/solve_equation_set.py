# -*- coding:utf-8 -*-
import trik

# 定义符号，A为方程系数矩阵，x为自变量，b为常数项。
A = trik.constant([[1, 2], [1, 3]], name='A')
x = trik.V([1, 0], name='x')
B = trik.constant([3, 4], name='b')

# 使用最小二乘误差定义loss。
# loss = trik.reduce_mean((A @ x - B) ** 2)
loss=A(trik.MM(),x)(trik.Sub(),B)(trik.Pow(),2)(trik.ReduceMean())#trik创建loss的计算引擎，申明变量为x。
loss.set_variables([x])

optimizer = trik.SGD()
for epoch in range(1000):
	optimizer.minimize(loss)
	loss_value = loss.val()
	if loss_value < 0.0000001:  # loss阈值。
		break
print('\nx={}'.format(x.value))
#~ print(loss.val())