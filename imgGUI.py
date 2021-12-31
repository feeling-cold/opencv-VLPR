import tkinter

import os
from tkinter import *
from tkinter.filedialog import askopenfilename

import cv2
import numpy as np
from PIL import Image, ImageTk

from tensorflow import keras

from CNN import cnn_predict
from Unet import unet_predict
from a.a.vidGUI import VidWindow
from core import locate_and_correct
from imgtovid import images_to_video




class ImgWindow:
    def __init__(self, win, ww, wh):
        self.win = win
        self.ww = ww
        self.wh = wh
        self.win.title("车牌识别系统--图像处理模块")
        self.win.geometry("%dx%d+%d+%d" % (ww, wh, 200, 50))
        self.img_src_path = None


        self.can_src = Canvas(self.win, width=512, height=512, bg='white', relief='solid', borderwidth=1)
        self.can_src.place(x=50, y=35)

        self.textlabe = Label(text="图像处理", fg="white", bg='black', font=("微软雅黑", 18))
        self.textlabe.place(x=750, y=15)

        self.can_lic1 = Canvas(self.win, width=245, height=85, bg='white', relief='solid', borderwidth=1)
        self.can_lic1.place(x=670, y=60)

        self.can_pred1 = Canvas(self.win, width=245, height=65, bg='white', relief='solid', borderwidth=1)
        self.can_pred1.place(x=670, y=170)

        self.can_lic2 = Canvas(self.win, width=245, height=85, bg='white', relief='solid', borderwidth=1)
        self.can_lic2.place(x=670, y=275)

        self.can_pred2 = Canvas(self.win, width=245, height=65, bg='white', relief='solid', borderwidth=1)
        self.can_pred2.place(x=670, y=385)


        self.button1 = Button(self.win, text='选择文件', width=10, height=1, command=self.load_show_img)
        self.button1.place(x=600, y=520)

        self.button2 = Button(self.win, text='车牌定位', width=10, height=1, command=self.display)
        self.button2.place(x=700, y=520)

        self.button3 = Button(self.win, text='识别车牌', width=10, height=1, command=self.display2)
        self.button3.place(x=800, y=520)

        self.button4 = Button(self.win, text='清空所有', width=10, height=1, command=self.clear)
        self.button4.place(x=900, y=520)

        self.button5 = Button(self.win, text='视频处理', width=8, height=1, command=self.back, bg="DimGray")
        self.button5.place(x=670, y=20)

        self.unet = keras.models.load_model('unet.h5')
        self.cnn = keras.models.load_model('cnn.h5')

        print('正在启动中,请稍等...')

        cnn_predict(self.cnn, [np.zeros((80, 240, 3))])

        print("已启动,开始识别吧！")

    def back(self):
        self.win.destroy()

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
        win2.mainloop()


    def load_show_img(self):
        self.clear()
        sv = StringVar()
        sv.set(askopenfilename())
        self.img_src_path = Entry(self.win, state='readonly', text=sv).get()
        #print(self.img_src_path)
        img_open = Image.open(self.img_src_path)
        if img_open.size[0] * img_open.size[1] > 240 * 80:
            img_open = img_open.resize((512, 512), Image.ANTIALIAS) #图片 512x512
        self.img_Tk = ImageTk.PhotoImage(img_open)
        self.can_src.create_image(258, 258, image=self.img_Tk, anchor='center')


    def display(self):
        if self.img_src_path == None:
            self.can_pred1.create_text(32, 15, text='请选择图片', anchor='nw', font=('黑体', 28))
        else:
            img_src = cv2.imdecode(np.fromfile(self.img_src_path, dtype=np.uint8), -1)
            h, w = img_src.shape[0], img_src.shape[1]
            if h * w <= 240 * 80 and 2 <= w / h <= 5:  # 整个图片就是一张车牌无需定位
                lic = cv2.resize(img_src, dsize=(240, 80), interpolation=cv2.INTER_AREA)[:, :, :3]  # resize(240,80)
                img_src_copy, Lic_img = img_src, [lic]
            else:
                img_src, img_mask = unet_predict(self.unet, self.img_src_path)
                img_src_copy, Lic_img = locate_and_correct(img_src, img_mask)
                #cv2.imwrite('E:/pic3.jpeg',img_src_copy)


            Lic_pred = cnn_predict(self.cnn, Lic_img)  # 利用cnn进行车牌的识别预测,Lic_pred中存的是元祖(车牌图片,识别结果)
            if Lic_pred:
                img = Image.fromarray(img_src_copy[:, :, ::-1])  # img_src_copy[:, :, ::-1]将BGR转为RGB
                self.img_Tk = ImageTk.PhotoImage(img)
                self.can_src.delete('all')
                self.can_src.create_image(258, 258, image=self.img_Tk,
                                          anchor='center')
                for i, lic_pred in enumerate(Lic_pred):
                    if i == 0:
                        self.lic_Tk1 = ImageTk.PhotoImage(Image.fromarray(lic_pred[0][:, :, ::-1]))
                        self.can_lic1.create_image(5, 5, image=self.lic_Tk1, anchor='nw')
                    elif i == 1:
                        self.lic_Tk2 = ImageTk.PhotoImage(Image.fromarray(lic_pred[0][:, :, ::-1]))
                        self.can_lic2.create_image(5, 5, image=self.lic_Tk2, anchor='nw')
            else:
                self.can_pred1.create_text(47, 15, text='未能识别', anchor='nw', font=('黑体', 27))


    def display2(self):
        if self.img_src_path == None:
            self.can_pred1.create_text(32, 15, text='请选择图片', anchor='nw', font=('黑体', 28))
        else:
            img_src = cv2.imdecode(np.fromfile(self.img_src_path, dtype=np.uint8), -1)
            h, w = img_src.shape[0], img_src.shape[1]
            if h * w <= 240 * 80 and 2 <= w / h <= 5:
                lic = cv2.resize(img_src, dsize=(240, 80), interpolation=cv2.INTER_AREA)[:, :, :3]
                img_src_copy, Lic_img = img_src, [lic]
            else:
                img_src, img_mask = unet_predict(self.unet, self.img_src_path)
                img_src_copy, Lic_img = locate_and_correct(img_src, img_mask)
                #cv2.imwrite('E:/pic3.jpeg',img_src_copy)


            Lic_pred = cnn_predict(self.cnn, Lic_img)
            if Lic_pred:
                for i, lic_pred in enumerate(Lic_pred):
                    if i == 0:
                        self.lic_Tk1 = ImageTk.PhotoImage(Image.fromarray(lic_pred[0][:, :, ::-1]))
                        self.can_lic1.create_image(5, 5, image=self.lic_Tk1, anchor='nw')
                        self.can_pred1.create_text(35, 15, text=lic_pred[1], anchor='nw', font=('黑体', 28))
                    elif i == 1:
                        self.lic_Tk2 = ImageTk.PhotoImage(Image.fromarray(lic_pred[0][:, :, ::-1]))
                        self.can_lic2.create_image(5, 5, image=self.lic_Tk2, anchor='nw')
                        self.can_pred2.create_text(40, 15, text=lic_pred[1], anchor='nw', font=('黑体', 28))
            else:
                self.can_pred1.create_text(47, 15, text='未能识别', anchor='nw', font=('黑体', 27))

    def clear(self):
        self.can_src.delete('all')
        self.can_lic1.delete('all')
        self.can_lic2.delete('all')
        self.can_pred1.delete('all')
        self.can_pred2.delete('all')
        self.img_src_path = None


if __name__ == '__main__':
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
    win.mainloop()

'''
root = tkinter.Tk()
root.title('车牌识别系统--图像处理')
root.resizable(False, False)
windowWidth = 1000
windowHeight = 600
screenWidth, screenHeight = root.maxsize()
geometryParam = '%dx%d+%d+%d' % (
windowWidth, windowHeight, (screenWidth - windowWidth) / 2, (screenHeight - windowHeight) / 2)
root.geometry(geometryParam)
root.wm_attributes('-topmost', 1)  # 窗口置顶

class imgGUI:
    def __init__(self):
    img_gif = tkinter.PhotoImage(file="2.gif")
    label_img = tkinter.Label(root, image=img_gif, width = "1000",height = "600")
    label_img.place(x=0, y=0)

    can_lic1 = tkinter.Canvas(root, width=512, height=512, bg='white', relief='solid', borderwidth=1)
    can_lic1.place(x=50, y=35)

    textlabe  = tkinter.Label(text = "图像处理", fg="white",bg = 'black', font=("微软雅黑", 18))
    textlabe.place(x=750, y=15)

    can_lic1 = tkinter.Canvas(root, width=245, height=85, bg='white', relief='solid', borderwidth=1)
    can_lic1.place(x=670, y=60)

    can_pred1 = tkinter.Canvas(root, width=245, height=65, bg='white', relief='solid', borderwidth=1)
    can_pred1.place(x=670, y=170)

    can_lic2 = tkinter.Canvas(root, width=245, height=85, bg='white', relief='solid', borderwidth=1)
    can_lic2.place(x=670, y=275)

    can_pred2 = tkinter.Canvas(root, width=245, height=65, bg='white', relief='solid', borderwidth=1)
    can_pred2.place(x=670, y=385)

    button1 = tkinter.Button(root, text='选择文件', width=10, height=1,bg = "DarkGray")
    button1.place(x=650, y=520)

    button2 = tkinter.Button(root, text='识别车牌', width=10, height=1,bg = "DarkGray")
    button2.place(x=750, y=520)

    button3 = tkinter.Button(root, text='清空所有', width=10, height=1,bg = "DarkGray")
    button3.place(x=850, y=520)

    root.mainloop()
'''