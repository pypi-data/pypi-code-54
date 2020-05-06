# -*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import trik

# 每类随机生成点的个数。
points_sum = 100

# 产生一个互相环绕的螺旋形数据分布。
c1_x, c1_y, c2_x, c2_y = [], [], [], []
r_step = 5 / points_sum
theta_step = 3 * np.pi / points_sum
r = 0
theta = 0
for _ in range(points_sum):
    c1_x.append(r * np.cos(theta))
    c1_y.append(r * np.sin(theta))
    c2_x.append(-r * np.cos(theta))
    c2_y.append(-r * np.sin(theta))
    r += r_step
    theta += theta_step
c_x = c1_x + c2_x
c_y = c1_y + c2_y

# 定义每个点的分类类别。
classification = trik.yu.generate_label_matrix([0] * points_sum + [1] * points_sum)[0]

# 定义符号。
A = trik.V(np.array([c_x, c_y]).transpose(), name='A')
W1 = trik.V(np.random.random((2, 8)), name='W1')  # 输入层到隐含层的权重矩阵。
W2 = trik.V(np.random.random((8, 8)), name='W2')  # 第1层隐含层到输出层的权重矩阵。
W3 = trik.V(np.random.random((8, 2)), name='W3')  # 第2层隐含层到输出层的权重矩阵。
B1 = trik.V(np.random.random((1, 8)), name='B1')  # 第1层隐含层的偏置。
B2 = trik.V(np.random.random((1, 8)), name='B2')  # 第2层隐含层的偏置。
B3 = trik.V(np.random.random((1, 2)), name='B3')  # 输出层的偏置。

# 构建2x8x8x2网络，使用ReLu激活函数。
model = trik.relu(trik.relu(trik.relu(A(trik.MM(),W1)(trik.Plus(),B1))(trik.MM(), W2)(trik.Plus(),B2))(trik.MM(), W3)(trik.Plus(),B3))

# 使用Softmax loss。
loss = trik.softmax_loss(model, trik.constant(classification))

print(loss)

loss.variables=[W1, W2, W3, B1, B2, B3]
optimizer = trik.SGD(0.1,0,0)
for epoch in range(10000):
    optimizer.minimize(loss)
    if epoch % 100 == 0:  # 每100次epoch检查一次loss。
        loss_value = loss.val()
        print('{},loss = {:.8f}'.format(epoch,loss_value))
        if loss_value < 0.01:  # loss阈值。
            break

predict = trik.where(trik.constant([[-1, 1]])(trik.Mul(), model)(trik.ReduceMean(axis=1))(trik.Lt(),0), -1, 1)

h = 0.1
# 生成预测采样点网格。
x, y = np.meshgrid(np.arange(np.min(c_x) - 1, np.max(c_x) + 1, h), np.arange(np.min(c_y) - 1, np.max(c_y) + 1, h))
predict.bind = {A: np.array([x.ravel(), y.ravel()]).transpose()}

z = predict.val().reshape(x.shape)

# 绘制图像。
plt.title('Paradox implement 2x8x8x2 Neural Network')
plt.plot(c1_x, c1_y, 'ro', label='Category 1')
plt.plot(c2_x, c2_y, 'bo', label='Category 2')
plt.contourf(x, y, z, 2, cmap='RdBu', alpha=.6)
plt.legend()
plt.show()
