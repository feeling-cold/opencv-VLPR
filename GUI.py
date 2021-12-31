import tkinter as tk
from PIL import ImageTk,Image
from imgGUI import *
from vidGUI import *
import tkinter

def imgpro():
    root.destroy()

    win = Tk()
    ww = 1000
    wh = 600

    img_gif = tkinter.PhotoImage(file="2.gif")
    label_img = tkinter.Label(win, image=img_gif, width="1000", height="600")
    label_img.place(x=0, y=0)
    ImgWindow(win, ww, wh)
    screenWidth, screenHeight = win.maxsize()
    geometryParam = '%dx%d+%d+%d' % (
        ww, wh, (screenWidth - ww) / 2, (screenHeight - wh) / 2)
    win.geometry(geometryParam)
    #win.protocol("WM_DELETE_WINDOW", ImgWindow.closeEvent)
    win.mainloop()

def vidpro():
    root.destroy()

    win2 = Tk()
    ww = 1000
    wh = 600

    img_gif = tkinter.PhotoImage(file="3.gif")
    label_img = tkinter.Label(win2, image=img_gif, width="1000", height="600")
    label_img.place(x=0, y=0)
    VidWindow(win2, ww, wh)
    screenWidth, screenHeight = win2.maxsize()
    geometryParam = '%dx%d+%d+%d' % (
        ww, wh, (screenWidth - ww) / 2, (screenHeight - wh) / 2)
    win2.geometry(geometryParam)
    #win2.protocol("WM_DELETE_WINDOW", VidWindow.closeEvent)
    win2.mainloop()


root = tkinter.Tk()
root.title('车牌识别系统')
root.resizable(False, False)
windowWidth = 1000
windowHeight = 600
screenWidth, screenHeight = root.maxsize()
geometryParam = '%dx%d+%d+%d' % (
windowWidth, windowHeight, (screenWidth - windowWidth) / 2, (screenHeight - windowHeight) / 2)
root.geometry(geometryParam)
root.wm_attributes('-topmost', 1)  # 窗口置顶

img_gif = tkinter.PhotoImage(file="1.gif")
label_img = tkinter.Label(root, image=img_gif, width = "1000",height = "600")
label_img.place(x=0, y=0)

textlabe  = tkinter.Label(text = "基于cnn的车牌识别系统", fg="white",bg = 'midnightblue',
              font=("微软雅黑", 28))
textlabe.place(x=310, y=40)
button = tkinter.Button(text = "图像处理",width = "10",height = "2",bg = "DimGray",command = imgpro)
button.place(x = 580,y = 500)
button = tkinter.Button(text = "视频处理",width = "10",height = "2",bg = "DimGray",command = vidpro)
button.place(x = 750,y = 500)
'''
team  = tkinter.Label(text = "小组成员：", fg="black",
              font=("微软雅黑", 18))
team.place(x=70, y=550)
teamlabe1  = tkinter.Label(text = "张嘉豪", fg="black",
              font=("微软雅黑", 18))
teamlabe1.place(x=200, y=550)
teamlabe2  = tkinter.Label(text = "程乙航", fg="black",
              font=("微软雅黑", 18))
teamlabe2.place(x=300, y=550)
teamlabe3  = tkinter.Label(text = "赵哲", fg="black",
              font=("微软雅黑", 18))
teamlabe3.place(x=410, y=550)
'''
root.mainloop()