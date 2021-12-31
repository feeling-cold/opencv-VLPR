import os
import cv2


def ExtractVideoFrame(video_input,output_path):
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    times = 0
    frame_frequency = 2
    count = 0
    cap = cv2.VideoCapture(video_input)

    print('开始提取', video_input, '视频的图片')
    while True:
        times += 1
        res, image = cap.read()
        if not res:
            print('图片提取结束')
            break
        if times % frame_frequency == 0:
            img_name = str(count).zfill(6)+'.png'
            cv2.imwrite(output_path + os.sep + img_name, image)
            count += 1
            print(output_path + os.sep + img_name)
    cap.release()

'''
def ShowSpecialFrame(file_path,frame_index):
    cap = cv2.VideoCapture(file_path) 
    cap.set(cv2.CAP_PROP_POS_FRAMES, float(frame_index))
    if cap.isOpened(): 
        rval, frame = cap.read()
        cv2.imshow("image:",frame)
        cv2.imwrite(output_path + os.sep + ".png" , frame)
        cv2.waitKey()
    cap.release()
'''



