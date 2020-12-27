# -*- coding:UTF-8 -*-
import time
import cv2
import pygame
import re
from sys import getsizeof
from aip import AipSpeech
from aip import AipOcr
#百度ai平台的个人信息
app_id='17653972'
app_key ='bceQySc3GhGquaprSdtMTckX'
secret_key ='KWabMLIC9LjuY16Z4ah1VvwctrcmYBpG'
music_index=0
#调用-api文字识别
def critic_word(file_path):
    client=AipOcr(app_id,app_key,secret_key)
    img_path=file_path+'.jpg'
    with open(img_path, 'rb') as fp:
        image=fp.read()
    options = {}
    options["language_type"] = "CHN_ENG"
    options["probability"] = "true"
    content=client.basicGeneral(image, options)
    # 将图片转为文字，写入文本
    fname = time.strftime("%Y%m%d%H%M", time.localtime())
    flag = 0
    with open(fname + '.txt', 'w', errors='ignore') as file:
        if (content['words_result']):  # 看是否识别到文字
            for word_result in content['words_result']:
                print("word_result: ", word_result)
                cost = re.findall(r'[1-9]+\.?[0-9]*', word_result['words'])
                print("cost: ", cost)
                if len(cost):  # 看文字中是否有数字
                    file.write(cost[0])
                    file.write("路公交车即将到站。")
                    flag = 1
                    break
            if (flag == 0):  # 有文字，但文字中没有数字的情况
                file.write(("未识别到公交车号"))
        else:
            file.write(("未识别到公交车号"))
        file.close()
    print("fname: ", fname + '.txt')
    return fname
#调用api-语音朗读
def speak(word_path,index):
    print("speak!")
    client=AipSpeech(app_id,app_key,secret_key)
    size=getsizeof(word_path)
    music_file = word_path + '-' + str(index) + '.mp3'
    pygame.mixer.init()
    with open(word_path+'.txt', 'r', encoding='GBK', errors='ignore') as txt_file:
        while (True):
            content = txt_file.read(1024)
            if getsizeof(content) == 49:
                break
            print("content: ", content)
            result = client.synthesis(content, 'zh', 1, {
            'vol': 5,
            })
            if not isinstance(result, dict):
                with open(music_file, 'wb') as f:
                    f.write(result)
                    f.close()
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()
    txt_file.close()
    time.sleep(int(size/10))
#主函数
def main(index):
    cap=cv2.VideoCapture(0)
    cap.set(3,900)
    cap.set(4,900)
    while(cap.isOpened()):
        ret_flag,Vshow=cap.read()
        cv2.imshow('Capture',Vshow)
        k=cv2.waitKey(1)
        if k==ord('x'):
            index+=1
            print('开始拍照')
            fname = time.strftime("%Y%m%d%H%M", time.localtime())
            cv2.imwrite(fname+'.jpg',cv2.resize(Vshow, (2000, 1200), interpolation=cv2.INTER_AREA))
            word_path = critic_word(fname)
            speak(word_path,index)
        elif k==ord('q'):
            break
    print('---end---')
    time.sleep(1)
    cap.release()
    cv2.destroyAllWindows()
main(music_index)