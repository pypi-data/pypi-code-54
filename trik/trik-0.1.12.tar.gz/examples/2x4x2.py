#-*- conding:utf-8 -*-
import matplotlib.pyplot as plt
import trik
# 每类随机生成点的个数。
points_sum = 100

# 在(0, 0)点附近生成一堆点然后以4为半径在周围生成一堆点构成2类随机数据。
c1_x, c1_y, c2_x, c2_y = [], [], [], []
for _ in range(points_sum):
    c1_x.append(trik.random.normal(0, 1))
    c1_y.append(trik.random.normal(0, 1))
    r = trik.random.normal(4, 1)
    theta = trik.random.normal(0,6.28)
    c2_x.append(r * trik.cos(theta))
    c2_y.append(r * trik.sin(theta))
c_x = c1_x + c2_x
c_y = c1_y + c2_y

# 定义符号。
A = trik.variable([c_x, c_y], name='A')
W1 = trik.variable(trik.random.random((32, 2)), name='W1')  # 输入层到隐含层的权重矩阵。
W2 = trik.variable(trik.random.random((2, 32)), name='W2')  # 隐含层到输出层的权重矩阵。
B1 = trik.variable(trik.random.random((32, 1)), name='B1')  # 隐含层的偏置。
B2 = trik.variable(trik.random.random((2, 1)), name='B2')  # 输出层的偏置。
K = trik.constant([[-1] * points_sum + [1] * points_sum, [1] * points_sum + [-1] * points_sum])

# 构建2x4x2网络，使用ReLu激活函数。
model = W2(trik.MM(),W1(trik.MM(),A)(trik.Plus(),B1)(trik.Max(),0))(trik.Plus(),B2)(trik.Max(),0)
# 使用SVM Pluss。
loss =K(trik.Mul(),model)(trik.ReduceSum(axis=0))(trik.Plus(),1)(trik.Max(),0)(trik.ReduceMean())
print(loss)
# 创建lossPlus擎，申明变量为W1，W2，B1和B2。
loss.variables=[W1, W2, B1, B2]

# 创建梯度下降optimizer。
optimizer = trik.SGD()
# 迭代至多10000次最小化loss。

    
for epoch in range(1000):
    optimizer.minimize(loss)
    if epoch % 10 == 0:  # 每100次epoch检查一次loss。
        loss_value = loss.val()
        print('loss = {:.8f}'.format(loss_value))
        if loss_value < 0.001:  # loss阈值。
            break

# 创建预测函数。
predict = trik.where(model(trik.Mul(),[[-1], [1]])(trik.ReduceSum(axis=0))(trik.Lt(),0), -1, 1)

# 创建预测函数计算引擎。


# 设置网格密度为0.1。
h = 0.1

# 生成预测采样点网格。
x, y = trik.meshgrid(trik.arange(min(c_x) - 1, max(c_x) + 1, h), trik.arange(min(c_y) - 1, max(c_y) + 1, h))

# 绑定变量值。
predict.bind = {A: [x.ravel(), y.ravel()]}

# 生成采样点预测值。
z = predict.val().reshape(x.shape)

# 绘制图像。
plt.title('Paradox implement 2x4x2 Neural Network')
plt.plot(c1_x, c1_y, 'ro', label='Category 1')
plt.plot(c2_x, c2_y, 'bo', label='Category 2')
plt.contourf(x, y, z, 2, cmap='RdBu', alpha=.6)
plt.legend()
plt.show()
