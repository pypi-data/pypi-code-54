from datetime import datetime

timeFormat = "%d-%m-%Y %H:%M:%S"
hasTimestamp = True
hasColor = True

def __init__() :
    import platform
    if platform.system() == "Windows":
        global hasColor
        hasColor = False

def __getTime():
    if hasColor:
        return "\u001b[34;1m[" + datetime.now().strftime(timeFormat) + "]\u001b[0m "
    return "[" + datetime.now().strftime(timeFormat) + "] "

def Log(logData):
    if hasTimestamp:
        print(__getTime(), end="")
    print(logData)

def Warning(logData):
    if hasTimestamp:
        print(__getTime(), end="")
    if hasColor:
        print("\u001b[33mWarning! \u001b[0m", end="")
    else:
        print("Warning! ", end="")
    print(logData)

def Fatal(logData, exit=True):
    if hasTimestamp:
        print(__getTime(), end="")
    if hasColor:
        print("\u001b[31mFatal! \u001b[0m", end="")
    else:
        print("Fatal! ", end="")
    print(logData)
    if exit:
        import sys
        sys.exit()

def Success(logData):
    if hasTimestamp:
        print(__getTime(), end="")
    if hasColor:
        print("\u001b[32mSuccess! \u001b[0m", end="")
    else:
        print("Success! ", end="")
    print(logData)