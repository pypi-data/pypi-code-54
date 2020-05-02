"""this is a test python file"""

def print_lot(the_list,level):
    for each in the_list:
        if isinstance(each, list):
            print_lot(each,level+1)
        else:
            for stop_lable in range(level):
                print("\t", end='')
            print(each)

            
