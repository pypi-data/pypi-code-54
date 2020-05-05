#PyPower Project
#Image Filters (With GUI)
#Source Code

from tkinter import *
import tkinter.messagebox
from PIL import ImageTk, Image
import cv2
import wget
import numpy as np
import os
from tkinter import filedialog
import imutils

#import image
def fileselector():
    global name
    main_win = tkinter.Tk() 
    main_win.withdraw()

    main_win.overrideredirect(True)
    main_win.geometry('0x0+0+0')

    main_win.deiconify()
    main_win.lift()
    main_win.focus_force()

    main_win.sourceFile = filedialog.askopenfilename(filetypes = (("Image Files",("*.jpg","*.png","*.jpeg")),("All Files","*")),parent=main_win, initialdir= "/",
    title='Please select a image file')
    main_win.destroy()
    
    img_path = main_win.sourceFile
    print(type(img_path))
    name1 = (os.path.basename(img_path))
    n =len(name1)
    name = name1[:n-4]
    print(name)
    image = cv2.imread(img_path)
    width = 1000
    height = 600 # keep original height
    dim = (width, height)
    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    os.mkdir(name)
    cv2.imwrite("image.png",image)
    cv2.imwrite('./'+name+'/'+name+'.png',image)
    
def takeselfie():
    global counter
    global name
    name = ""
    counter = counter +1
    name = "Selfie" + str(counter) 
    os.mkdir(name)
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    while(cap.isOpened()):
        cv2.imwrite("image.png",frame)
        cv2.imwrite('./'+name+'/'+name+'.png',frame)
        break
    tkinter.messagebox.showinfo("Image Captured","Selfie is Captured. \n   Apply Filters")
        
def showImage():
    os.startfile("image.png")

def verify_alpha_channel(frame):
    try:
        frame.shape[2] # looking for the alpha channel
    except IndexError:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    return frame

    
def applyInvert():
    global name
    img = cv2.imread("./image.png")
    invert = cv2.bitwise_not(img)
    cv2.imwrite('./'+name+'/invert.png',invert)
    cv2.imshow("invert",invert)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def apply_sepia():
    global name
    intensity = 0.5
    frame =cv2.imread("./image.png")
    frame = verify_alpha_channel(frame)
    frame_h, frame_w, frame_c = frame.shape
    sepia_bgra = (20, 66, 150, 1)
    overlay = np.full((frame_h, frame_w, 4), sepia_bgra, dtype='uint8')
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA) 
    cv2.addWeighted(src1=overlay, alpha=intensity, src2=frame, beta=1.0 , gamma=0, dst=frame)
    cv2.imwrite('./'+name+'/sepia.png',frame)
    cv2.imshow("sepia",frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
  
def sunnyday():
    global name
    intensity = 0.5
    frame =cv2.imread("./image.png")
    frame = verify_alpha_channel(frame)
    frame_h, frame_w, frame_c = frame.shape
    sepia_bgra = (102, 255, 255, 1)
    overlay = np.full((frame_h, frame_w, 4), sepia_bgra, dtype='uint8')
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA) 
    cv2.addWeighted(src1=overlay, alpha=intensity, src2=frame, beta=1.0 , gamma=0, dst=frame)
    cv2.imwrite('./'+name+'/sunnyday.png',frame)
    cv2.imshow("sunnyday",frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
  
        
def alpha_blend(frame_1, frame_2, mask):
    alpha = mask/255.0 
    blended = cv2.convertScaleAbs(frame_1*(1-alpha) + frame_2*alpha)
    return blended

def potrait_mode():
    global name
    frame = cv2.imread("./image.png")
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 120,255,cv2.THRESH_BINARY)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGRA)
    blured = cv2.GaussianBlur(frame, (21,21), 11)
    blended = alpha_blend(frame, blured, mask)
    #cv2.imshow("blended",blended)
    #cv2.imshow("grey",gray)
    cv2.imwrite('./'+name+'/potrait.png',frame)
    cv2.imshow("potrait",frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def apply_circle_focus_blur( ):
    global name
    frame = cv2.imread("./image.png")
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    intensity=0.2
    frame = verify_alpha_channel(frame)
    frame_h, frame_w, frame_c = frame.shape
    y = int(frame_h/2)
    x = int(frame_w/2)

    mask = np.zeros((frame_h, frame_w, 4), dtype='uint8')
    cv2.circle(mask, (x, y), int(y/2), (255,255,255), -1, cv2.LINE_AA)
    mask = cv2.GaussianBlur(mask, (21,21),11 )

    blured = cv2.GaussianBlur(frame, (25,25), 11)
    blended = alpha_blend(frame, blured, 255-mask)
    frame = cv2.cvtColor(blended, cv2.COLOR_BGRA2BGR)
    
    cv2.imwrite('./'+name+'/blur.png',frame)
    cv2.imshow("blur",frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def apply_black_white():
    global name
    img = cv2.imread("./image.png")
    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    cv2.imwrite('./'+name+'/chaplin.png',grayImage)
    cv2.imshow('chaplin', grayImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

img = cv2.imread("./sample.png")
name = ""
counter = 0
click = False
flag =0            
root = Tk()
root.title("GUI : Image Filters")

root.geometry("873x450")

root.configure(background = '#99ffbb')
Tops = Frame(root,bg = '#99ffbb',pady = 1, width =450, height = 50, relief = "ridge")
Tops.grid(row=0,column=0)


Title_Label = Label(Tops,font=('Comic Sans MS',19,'bold'),text = "     PyPower  Presents  GUI  based  Image  Filters  with Python\t\t",bg= 'black',fg='white',justify ="center")
Title_Label.grid(row=0,column=0)
MainFrame = Frame(root,bg = '#99ffbb',pady=2,padx=2, width =1350, height = 100, relief = RIDGE)
MainFrame.grid(row=1,column=0)

LeftFrame = Frame(MainFrame, width =200, height=200, pady=2,bg='#99ffbb'  ,relief=RIDGE)
LeftFrame.pack(side=LEFT)

RightFrame  =  Frame(MainFrame ,bd=5, width =200, height=200, padx=1,pady=2,bg='#f2ccff',relief=RIDGE)
RightFrame.pack(side=RIGHT)






Label_1 =Label(RightFrame, font=('lato black', 37,'bold'), text=" Image Filters ",padx=2,pady=2, bg="yellow",fg ="black")
Label_1.grid(row=0, column=0)

Label_2 =Label(RightFrame, font=('arial', 30,'bold'), text="",padx=2,pady=2, bg="#f2ccff",fg = "black")
Label_2.grid(row=1, column=0,sticky=W)

Label_9 =Button(RightFrame, font=('arial', 19,'bold'), text="  Invert ",padx=2,pady=2, bg="red",fg = "white",command=applyInvert)
Label_9.grid(row=2, column=0,sticky=W)

Label_9 =Button(RightFrame, font=('arial', 19,'bold'), text="  Blur   ",padx=2,pady=2, bg="red",fg = "white",command=apply_circle_focus_blur)
Label_9.grid(row=2, column=0,sticky=E)

Label_2 =Label(RightFrame, font=('arial', 13,'bold'), text="",padx=2,pady=2, bg="#f2ccff",fg = "black")
Label_2.grid(row=3, column=0,sticky=W)

Label_9 =Button(RightFrame, font=('arial', 19,'bold'), text=" Potrait ",padx=2,pady=2, bg="red",fg = "white",command=potrait_mode)
Label_9.grid(row=4, column=0,sticky=W)

Label_9 =Button(RightFrame, font=('arial', 19,'bold'), text="  Sepia ",padx=2,pady=2, bg="red",fg = "white",command=apply_sepia)
Label_9.grid(row=4, column=0,sticky=E)

Label_2 =Label(RightFrame, font=('arial', 13,'bold'), text="",padx=2,pady=2, bg="#f2ccff",fg = "black")
Label_2.grid(row=5, column=0,sticky=W)

Label_9 =Button(RightFrame, font=('arial', 16,'bold'), text="SunnyDay",padx=2,pady=2, bg="red",fg = "white",command=sunnyday)
Label_9.grid(row=6, column=0,sticky=W)

Label_9 =Button(RightFrame, font=('arial', 19,'bold'), text="Chaplin",padx=2,pady=2, bg="red",fg = "white",command=apply_black_white)
Label_9.grid(row=6, column=0,sticky=E)

Label_7 =Label(RightFrame, font=('arial', 30,'bold'), text="      ",padx=2,pady=2, bg="#f2ccff",fg = "black")
Label_7.grid(row=7, column=1,sticky=W)








Label_1 =Label(LeftFrame, font=('lato black', 37,'bold'), text=" Select Image ",padx=2,pady=2, bg="yellow",fg ="black")
Label_1.grid(row=0, column=0,sticky=W)

Label_2 =Label(LeftFrame, font=('arial', 20,'bold'), text="",padx=2,pady=2, bg="#99ffbb",fg = "black")
Label_2.grid(row=1, column=0,sticky=W)

Label_9 =Button(LeftFrame, font=('arial', 17,'bold'), text="Take Selfie (Webcam)",padx=2,pady=2, bg="blue",fg = "white",command=takeselfie)
Label_9.grid(row=2, column=0)

Label_7 =Label(LeftFrame, font=('arial', 7,'bold'), text="",padx=2,pady=2, bg="#99ffbb",fg = "black")
Label_7.grid(row=3, column=0,sticky=W)

Label_8 =Button(LeftFrame, font=('Arial', 18,'bold'), text="  Choose From File  ",padx=2,pady=2, bg="blue",fg = "white",command=fileselector)
Label_8.grid(row=4, column=0)

Label_7 =Label(LeftFrame, font=('arial', 30,'bold'), text="",padx=2,pady=2, bg="#99ffbb",fg = "black")
Label_7.grid(row=5, column=0,sticky=W)

Label_4 =Button(LeftFrame, font=('arial', 23,'bold'), text="Show Image",padx=2,pady=2, bg="white",fg = "blue",command=showImage)
Label_4.grid(row=6, column=0)

Label_7 =Label(LeftFrame, font=('arial', 30,'bold'), text="      ",padx=2,pady=2, bg="#99ffbb",fg = "black")
Label_7.grid(row=7, column=1,sticky=W)

root.mainloop()

