try:
    from getkey import getkey
    from AnsiPrint import *
except ModuleNotFoundError:
    from os import system
    system("pip install getkey;pip install AnsiPrint;")

def readpass(prompt,replacement=None):
    class ReplacementLengthError(Exception):
        pass
    prompt = str(prompt)
    if replacement != None and len(str(replacement)) > 5:
        raise ReplacementLengthError("Length of replacement must not exceed 5.")
    replacement = str(replacement)
    print(prompt,end="",flush=True)
    output = ""
    while True:
        inp = getkey()
        if len(inp) == 1 and ord(inp) == 127:
            if output != "":
                if len(output) == 1:
                    output = ""
                else:
                    output = output[:-1]
                
                if replacement != "None":
                    print("\b \b" * len(replacement),end="",flush=True)
                else:
                    print("\b \b" * 1,end="",flush=True)
            else:
                print("\a",end="",flush=True)
        elif len(inp) == 1 and ord(inp) == 10:
            print("\n",end="",flush=True)
            return output
        elif len(inp) == 1:
            output = output + inp
            print(inp,end="",flush=True)
        if replacement != "None" and ord(inp) != 127 and len(inp) == 1:
            if replacement != "":
                print("\b" + replacement,end="",flush=True)
            else:
                print("\b \b",end="",flush=True)