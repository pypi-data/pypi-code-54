# coding:utf-8

# 模型文件
ModelName = 'model_20200502_202646'
# 需要查看的变量 list
ParamsShow = [
    'income',
    'inserve_days',
    ]


cut_points_step = 30
assist_num=3
# score_bond = [168, 440, 470, 500, 560, 620, 650, 710, 740, 771]
# 边界为空则自动划分边界
# score_bond = []
score_bond = [280,310,340,370,400,430, 460, 490, 520, 550, 580, 610, 640, 670, 700, 730, 760, 999]

# 坐标轴名称
x_label = "分数区间"
y_label_left = "区间人数统计"
y_label_right = "区间比率统计"
graph_title = "201911分数分布及离职比例(201911模型)"

# 是否显示折线图
line_flag = True

