'''这是nester.py模块，提供了一个print_lol函数，这个函数的作用是打印列表，其中有可能包含，也有可以不包含嵌套列表。'''
print("模块函数：")
def print_lol(the_list):
    '''the_list可以是任意嵌套的列表，把所指定的列表输出到屏幕上，
    各个数据项各占一项
    '''
    for item in the_list:
        if isinstance(item, list):
            print_lol(item)
        else:
            print(item)
