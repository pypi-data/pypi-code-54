# -*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import trik

# sin函数采样点数。
points_number = 100

# 生成训练数据。
c_x = np.arange(points_number).reshape([points_number, 1])
c_y = np.sin(c_x / 5)

# 构造1x32x1回归神经网络（最后一层不激活）。
model = trik.Model()
model.add(trik.Dense(16, in_dim=1))  # 1维输入32维输出的全连接层。
model.add(trik.Activation('tanh'))  # 使用tanh激活函数。
model.add(trik.Dense(16))  # 1维输入32维输出的全连接层。
model.add(trik.Activation('tanh'))  # 使用tanh激活函数。
model.add(trik.Dense(1))
model.loss('mse')

# 使用Adam下降优化器。
model.optimizer('adam',0.01)

# 执行训练。
model.train(c_x, c_y, epochs=2000)

# 生成预测数据。
x = np.arange(-5, 135, 0.1)
y = model.predict(x.reshape([x.shape[0], 1]))

# 绘制图像。
plt.title('1x64x1 Regression Neural Network')
plt.plot(c_x, c_y, 'ro', label='Sin(x)')
plt.plot(x,y,'b', label='Regression')
plt.legend()
plt.show()
