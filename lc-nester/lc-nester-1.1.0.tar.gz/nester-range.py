'''
这是nester.py模块，提供了一个名为print_lol的函数
用来打印列表，其中包含或不包含嵌套列表
'''

def print_lol(the_list, level):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level + 1)
        else:
            for tab_stop in range(level):
                print("\t", end='')
            print(each_item)
