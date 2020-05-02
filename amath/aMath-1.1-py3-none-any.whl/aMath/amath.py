def add(*args):
    """
    This function returns the Sum of all the numbers provided as paratmeters.
    In case of exception, it will return -1.
    If no parameter is provided, it will return 0.
    add(1,2,3,4) will return 10
    """
    s = 0
    try:
        for i in args:
            s = s + i
    except TypeError as e:
        print("Only numeric values are accepted as parameter , error : ",e)
        return -1
    return s

def mul(*args):
    """
    This function returns the Multiplication of all the numbers provided as paratmeters.
    In case of exception, it will return -1.
    If no parameter is provided, it will return 1.
    mul(1,2,3,4) will return 24
    """
    m = 1
    try:
        for i in args:
            m = m * i
    except TypeError as e:
        print("Only numeric values are accepted as parameter , error : ", e)
        return -1
    return m

if __name__ == "__main__":
    print("call functions with any number of arguments>0")
