#
# MIT License
#
# Copyright (c) 2017 - 2020 Firebolt Inc,
# Copyright (c) 2020 - Present Aaron Ma,
# Copyright (c) 2020 - Present proballstar.
# All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
from .error import SkyforceImportError
try:
    import random as rand          # Random library
    import time                # Time library
    import math                    # Math library
except ImportError:
    raise SkyforceImportError("Random is not installed!")

__all__ = ["user", "timer", "random", "floor", "round", "calculator", "progress bar"]

def user(msg):
    """
    Get the user's name.
    - input:
        - message to display
    """
    user = input("What is your name? ")
    print("Hello {}! {}".format(user, msg))


def timer(time):
    """
    A timer function.
    - input:
        - time of counting down
    """
    timer = int(timer)         # convert timer to an integer
    for i in range(timer):     # for loop
        print(timer)           # print
        time.sleep(1)  # wait
        timer -= 1             # countdown


def random(min_num, max_num):
    min_num = int(input("What is the minumum? "))  # min number
    max_num = int(input("What is the maximum? "))  # maximum number
    # select a random number between min - max
    num = rand.randint(min_num, max_num)
    print(num)  # print the random #


def floor(num):
    new_num = math.floor(num)
    print("rf", new_num)
    return new_num


def round(flt):
    strflt = str(flt)
    newstrflt = strflt[-1:]
    intstrflt = int(newstrflt)
    if (intstrflt >= 5):
        newflt = floor(flt)
        newflt = newflt + 1
    else:
        newflt = floor(flt)
    print(newflt)


def calculator(a, operator, b):
    if (operator == "*" or "multiply"):
        num = a*b
        print(num)
    elif (operator == "/" or "divide"):
        num = a/b
        print(num)
    elif (operator == "-" or "subract"):
        num = a - b
        print(num)
    elif (operator == "+" or "add"):
        num = a + b
        print(num)
    else:
        print("invalid")


# Progress Bar
def progress_bar(t):
    """Prints a progress bar that take t seconds to complete loading."""
    for i in range(1, 101):
        print("\r{:>6}% |{:<30}|".format(
            i, u"\u2588" * round(i // 3.333)), end='', flush=True)
        time.sleep(t/100)

    time.sleep(0.1)
    print("\n")