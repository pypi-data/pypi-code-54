import numpy as np
import matplotlib.pyplot as plt
import trik
# 每类随机生成点的个数。
points_sum = 100
c1_x = []
c1_y = []
c2_x = []
c2_y = []

# 分别在(0, 0)点附近和(8, 8)点附近生成2类随机数据。
for _ in range(points_sum):
    c1_x.append(np.random.normal(0, 2))
    c1_y.append(np.random.normal(0, 2))
    c2_x.append(np.random.normal(8, 2))
    c2_y.append(np.random.normal(8, 2))
c1 = trik.constant([c1_x, c1_y], name='c1')
c2 = trik.constant([c2_x, c2_y], name='c2')
W = trik.V([[1, 1], [1, 1]], name='w')
B = trik.V([[1], [1]], name='b')
# 定义SVM loss函数。
# loss = trik.reduce_mean(trik.maximum(0, [[1, -1]] @ (W @ c1 + B) + 1) + trik.maximum(0, [[-1, 1]] @ (W @ c2 + B) + 1))
loss1=trik.constant([[1,-1]])(trik.MM(),W(trik.MM(),c1)(trik.Plus(),B))(trik.Plus(),1)(trik.Max(),0)
loss2=trik.constant([[-1,1]])(trik.MM(),W(trik.MM(),c2)(trik.Plus(),B))(trik.Plus(),1)(trik.Max(),0)
loss=loss1(trik.Plus(),loss2)(trik.ReduceMean())
loss.set_variables([W,B])
optimizer = trik.SGD()
for epoch in range(1000):
    optimizer.minimize(loss)
    loss_value = loss.val()
    print('loss = {:.8f}'.format(loss_value))
    if loss_value < 0.00001:  # loss阈值。
        break
# 获取W和B的训练结果。
w_data = W.value
b_data = B.value
print(w_data,b_data)
# 计算分类直线的斜率和截距。
k = (w_data[1, 0] - w_data[0, 0]) / (w_data[0, 1] - w_data[1, 1])
b = (b_data[1, 0] - b_data[0, 0]) / (w_data[0, 1] - w_data[1, 1])
print(k,b)
# 分类面的端点。
x_range = np.array([np.min(c1_x), np.max(c2_x)])

plt.title('Paradox implement Linear SVM')
plt.plot(c1_x, c1_y, 'ro', label='Category 1')
plt.plot(c2_x, c2_y, 'bo', label='Category 2')
plt.plot(x_range, k * x_range + b, 'y', label='SVM')
plt.legend()
plt.show()
