def add(a, b):
    return a + b

for x in (10, 20, 30):
    print(2*x)
for x in "abcdef":
    print(x)
d = {"name": "wll", "age": 18, "job": "program"}
for x in d:
    print(x)  # 遍历字典所有的key
for x in d.keys():
    print(x)  # 遍历字典所有的key
for x in d.values():
    print(x)  # 遍历字典所有的value
for x in d.items():
    print(x)  # 遍历字典所有的键值对
print("############################################################")
sum1 = 0
sum_o = 0
sum_j = 0
for i in range(101):
    sum1 = sum1 + i
    if i % 2 == 0:
        sum_o = sum_o + i
    else:
        sum_j = sum_j + i
print("1-100所有数的和为：", sum1)
print("1-100所有偶数的和为：", sum_o)
print("1-100所有奇数的和为：", sum_j)
print("1-100所有和为{0}，偶数为{1}，奇数为{2}".format(sum1, sum_o, sum_j))








