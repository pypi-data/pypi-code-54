import os

def ansiprint(msg=None,color="reset",end="\n"):
    if not msg == None:
        if color == "red":
            color = "\033[38;5;9m"
        elif color == "yellow":
            color = "\033[38;5;11m"
        elif color == "green":
            color = "\033[38;5;10m"
        elif color == "blue":
            color = "\033[38;5;12m"
        elif color == "purple":
            color = "\033[38;5;13m"
        elif color == "black":
            color = "\033[38;5;0m"
        elif color == "white" or color == "reset":
            color = "\033[38;5;15m"
        else:
            try: 
                int(color)
                color = str(color)
                if not color.startswith("\033"):
                    color = "\033[38;5;" + color + "m"
            except:
                raise Error.UnrecognizedColorName("Available colors are: red, yellow, green, blue, purple, black, white, or reset. If your colorname does not appear here, please refer to the ansi chart in the README.md.")
        #
        print(str(color) + str(msg) + "\033[38;5;15m",end=end)
    else:
        raise Error.MissingFunctionArguments("Please provide a message to output.")

def ansi(color=None):
    if not color == None:
        if color == "red":
            color = "\033[38;5;9m"
        elif color == "yellow":
            color = "\033[38;5;11m"
        elif color == "green":
            color = "\033[38;5;10m"
        elif color == "blue":
            color = "\033[38;5;12m"
        elif color == "purple":
            color = "\033[38;5;13m"
        elif color == "black":
            color = "\033[38;5;0m"
        elif color == "white" or color == "reset":
            color = "\033[38;5;15m"
        else:
            try: 
                int(color)
                color = str(color)
                if not color.startswith("\033"):
                    color = "\033[38;5;" + color + "m"
            except:
                raise Error.UnrecognizedColorName("Available colors are: red, yellow, green, blue, purple, black, white, or reset. If your colorname does not appear here, please refer to the ansi chart in the README.md.")
        return color
    else:
        raise Error.MissingFunctionArguments("Please provide a color-name/ansi code.")

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    
    return None

class MissingFunctionArguments(Exception):
    pass

class UnrecognizedColorName(Exception):
    pass