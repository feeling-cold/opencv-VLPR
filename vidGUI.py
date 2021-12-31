
from videospilt import ExtractVideoFrame
import os
from tkinter import *
from tkinter.filedialog import askopenfilename

import cv2
import numpy as np
from PIL import Image, ImageTk

from tensorflow import keras

from CNN import cnn_predict
from Unet import unet_predict
from core import locate_and_correct
from imgtovid import images_to_video
import tkinter.messagebox



class VidWindow:
    def __init__(self, win, ww, wh):
        self.win = win
        self.ww = ww
        self.wh = wh
        self.win.title("车牌识别系统--视频处理模块")
        self.win.geometry("%dx%d+%d+%d" % (ww, wh, 200, 50))
        self.img_src_path = None


        self.can_src = Canvas(self.win, width=512, height=512, bg='white', relief='solid', borderwidth=1)
        self.can_src.place(x=50, y=35)

        self.textlabe = Label(text="视频处理", fg="white", bg='black', font=("微软雅黑", 18))
        self.textlabe.place(x=750, y=15)

        self.can_lic1 = Canvas(self.win, width=245, height=85, bg='white', relief='solid', borderwidth=1)
        self.can_lic1.place(x=670, y=60)

        self.can_pred1 = Canvas(self.win, width=245, height=65, bg='white', relief='solid', borderwidth=1)
        self.can_pred1.place(x=670, y=170)

        self.can_lic2 = Canvas(self.win, width=245, height=85, bg='white', relief='solid', borderwidth=1)
        self.can_lic2.place(x=670, y=275)

        self.can_pred2 = Canvas(self.win, width=245, height=65, bg='white', relief='solid', borderwidth=1)
        self.can_pred2.place(x=670, y=385)


        self.button1 = Button(self.win, text='选择文件', width=10, height=1, command=self.load_show_vid)
        self.button1.place(x=600, y=520)

        self.button2 = Button(self.win, text='视频追踪', width=10, height=1, command=self.displayvideo)
        self.button2.place(x=700, y=520)

        self.button3 = Button(self.win, text='单帧分析', width=10, height=1, command=self.frameany)
        self.button3.place(x=800, y=520)

        self.button4 = Button(self.win, text='清空所有', width=10, height=1, command=self.clear)
        self.button4.place(x=900, y=520)


        self.unet = keras.models.load_model('unet.h5')
        self.cnn = keras.models.load_model('cnn.h5')

        print('正在启动中,请稍等...')
        cnn_predict(self.cnn, [np.zeros((80, 240, 3))])
        print("已启动,开始识别吧！")



    def frameany(self):
        self.img_src_path = 'E:/pic/000057.png'

        img_src = cv2.imdecode(np.fromfile(self.img_src_path, dtype=np.uint8), -1)
        h, w = img_src.shape[0], img_src.shape[1]
        if h * w <= 240 * 80 and 2 <= w / h <= 5:
            lic = cv2.resize(img_src, dsize=(240, 80), interpolation=cv2.INTER_AREA)[:, :, :3]
            img_src_copy, Lic_img = img_src, [lic]
        else:
            img_src, img_mask = unet_predict(self.unet, self.img_src_path)
            img_src_copy, Lic_img = locate_and_correct(img_src, img_mask)
            #cv2.imwrite('E:/pic3.jpeg', img_src_copy)

        Lic_pred = cnn_predict(self.cnn, Lic_img)
        if Lic_pred:
            img = Image.fromarray(img_src_copy[:, :, ::-1])
            self.img_Tk = ImageTk.PhotoImage(img)
            self.can_src.delete('all')
            self.can_src.create_image(258, 258, image=self.img_Tk,
                                      anchor='center')
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

    def load_show_vid(self):
        self.movefile()
        self.clear()
        sv = StringVar()
        sv.set(askopenfilename())
        self.vid_src_path = Entry(self.win, state='readonly', text=sv).get()
        video = cv2.VideoCapture(self.vid_src_path)
        out_path = "E:/pic/"
        ExtractVideoFrame(self.vid_src_path, out_path)
        tkinter.messagebox.showinfo(title="提示信息", message="处理结束 准备播放视频")
        while True:
            ref, frame = video.read()
            cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pilImage = Image.fromarray(cvimage)
            pilImage = pilImage.resize((520, 520), Image.ANTIALIAS)
            tkImage = ImageTk.PhotoImage(image=pilImage)
            self.can_src.create_image(258, 258, image=tkImage, anchor='center')
            self.win.update_idletasks()
            self.win.update()
        self.win.mainloop()

    def displayvideo(self):
        self.clear()
        for i in os.listdir('E:/pic/'):
            img_src, img_mask = unet_predict(self.unet,'E:/pic/'+i)
            img_src_copy, Lic_img = locate_and_correct(img_src, img_mask)
            cv2.imwrite('E:/pic3/'+i, img_src_copy)
        tkinter.messagebox.showinfo(title="提示信息",message="处理结束 准备播放视频")
        images_to_video()
        video = cv2.VideoCapture('demo_car.mp4')
        while True:
            ref, frame = video.read()
            cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pilImage = Image.fromarray(cvimage)
            pilImage = pilImage.resize((520, 520), Image.ANTIALIAS)
            tkImage = ImageTk.PhotoImage(image=pilImage)

            self.can_src.create_image(258, 258, image=tkImage, anchor='center')
            self.win.update_idletasks()
            self.win.update()
        self.win.mainloop()


    def movefile(self):
        path1 = "E:/pic/"
        path2 = "E:/pic3/"
        ls = os.listdir(path1)
        for i in ls:
            f_path = os.path.join(path1, i)
            os.remove(f_path)
        ls2 = os.listdir(path2)
        for i in ls2:
            f_path2 = os.path.join(path2, i)
            os.remove(f_path2)

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
    img_gif = tkinter.PhotoImage(file="3.gif")
    label_img = tkinter.Label(win, image=img_gif, width="1000", height="600")
    label_img.place(x=0, y=0)
    VidWindow(win, ww, wh)
    screenWidth, screenHeight = win.maxsize()
    geometryParam = '%dx%d+%d+%d' % (
    ww, wh, (screenWidth - ww) / 2, (screenHeight - wh) / 2)
    win.geometry(geometryParam)
    win.mainloop()

    '''
    root = tkinter.Tk()
    root.title('车牌识别系统--视频处理')
    root.resizable(False, False)
    windowWidth = 1000
    windowHeight = 600
    screenWidth, screenHeight = root.maxsize()
    geometryParam = '%dx%d+%d+%d' % (
    windowWidth, windowHeight, (screenWidth - windowWidth) / 2, (screenHeight - windowHeight) / 2)
    root.geometry(geometryParam)
    root.wm_attributes('-topmost', 1)  # 窗口置顶


    img_gif = tkinter.PhotoImage(file="3.gif")
    label_img = tkinter.Label(root, image=img_gif, width = "1000",height = "600")
    label_img.place(x=0, y=0)

    can_lic1 = tkinter.Canvas(root, width=512, height=512, bg='white', relief='solid', borderwidth=1) 
    can_lic1.place(x=50, y=35)

    textlabe  = tkinter.Label(text = "视频处理", fg="white",bg = 'black', font=("微软雅黑", 18))
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

    button2 = tkinter.Button(root, text='视频追踪', width=10, height=1,bg = "DarkGray")  
    button2.place(x=750, y=520)

    button3 = tkinter.Button(root, text='单帧分析', width=10, height=1,bg = "DarkGray")  
    button3.place(x=850, y=520)


    root.mainloop()
    '''