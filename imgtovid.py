import cv2
import os


def images_to_video():
    fps = 15
    img_array = []
    img_width = 512
    img_height = 512
    path = "E:/pic3/"
    for file_name in os.listdir(path):
        img = cv2.imread(path + file_name)
        if img is None:
            print(file_name + "不存在")
            continue
        img_array.append(img)

    out = cv2.VideoWriter('demo_car.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (img_width, img_height))

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

