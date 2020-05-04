import numpy as np
import turtle

global pi
pi = 3.14

def normalize(xarray):
    normalizated_x = (xarray - np.min(xarray)) / (np.max(xarray) - np.min(xarray))
    return normalizated_x

def circle_size(circle_radius):
    circle_size_val = circle_radius * pi
    return circle_size_val

def circle_circ(circle_radius):
    circle_circumference_val = circle_radius * pi * 2
    return circle_circumference_val

def square_size(squareside):
    return squareside ** 2

def square_circ(squareside):
    return squareside * 4

def triang_size(base,height):
    return (base * height) / 2

def rect_size(w,h):
    return w*h

def rect_circ(w,h):
    return (w*2) + (h*2)

def perp_triangle(a,showangles):
    if showangles is False:
        hyp = a * 2**0.5
        s = turtle.Screen()
        t = turtle.Turtle()
        t.forward(a)
        t.left(135)
        t.forward(hyp)
        t.left(135)
        t.forward(a)
        t.hideturtle()
    elif showangles is True:
        hyp = a * 2**0.5
        s = turtle.Screen()
        t = turtle.Turtle()
        t.write('90',font=("Courier",8))
        t.forward(a)
        t.left(135)
        t.write('45',font=("Courier",8))
        t.forward(hyp)
        t.left(135)
        t.write('45',font=("Courier",8))
        t.forward(a)
        t.hideturtle()

