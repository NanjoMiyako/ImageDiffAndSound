import cv2
import sys
import time

from mutagen.mp3 import MP3 as mp3

import pygame.mixer

args = sys.argv

print(len(sys.argv))

if len(args) < 6:
 exit()


caribRectFilePath = args[1];
aRectDiffKijun = float(args[2]);
bRectDiffKijun = float(args[3]);
aRectTimeSpan = float(args[4]);
bRectTimeSpan = float(args[5]);


global g_width;
global g_height;

g_width = 320;
g_height = 240;
# VideoCapture オブジェクトを取得します
capture = cv2.VideoCapture(0)

print(capture.set(cv2.CAP_PROP_FRAME_WIDTH, g_width))
print(capture.set(cv2.CAP_PROP_FRAME_HEIGHT, g_height))




aRect_sx = 0;
aRect_sy = 0;
aRect_ex = 0;
aRect_ey = 0;

bRect_sx = 0;
bRect_sy = 0;
bRect_ex = 0;
bRect_ey = 0;

aRectFlg = False;
bRectFlg = False;

aRectStartTime = 0;
bRectStartTime = 0;

out_img = cv2.imread("white.jpg");

def aRectDiff(img1, img2):
    global aRect_sx, aRect_sy, aRect_ex, aRect_ey;
    global out_img

    width = aRect_ex - aRect_sx;
    height = aRect_ey - aRect_sy;
    changeRate = 0.0;
    
    chCount = 0;
    allPixels = width * height;
    
    for x in range(0, width) :
         for y in range(0, height) :
            if img1[aRect_sy + y,  aRect_sx + x, 0] >= img2[aRect_sy + y, aRect_sx + x, 0]:
                out_img[aRect_sy + y, aRect_sx + x, 0] = abs(img1[aRect_sy + y, aRect_sx + x, 0] - img2[aRect_sy + y, aRect_sx + x, 0]);
            else:
                out_img[aRect_sy + y, aRect_sx + x, 0] = abs(img2[aRect_sy + y, aRect_sx + x, 0] - img1[aRect_sy + y, aRect_sx + x, 0]);

            if img1[aRect_sy + y, aRect_sx + x, 1] >= img2[aRect_sy + y, aRect_sx + x, 1]:
                out_img[aRect_sy + y, aRect_sx + x, 1] = abs(img1[aRect_sy + y, aRect_sx + x, 1] - img2[aRect_sy + y, aRect_sx + x, 1]);
            else:
                out_img[aRect_sy + y, aRect_sx + x, 1] = abs(img2[aRect_sy + y, aRect_sx + x, 1] - img1[aRect_sy + y, aRect_sx + x, 1]);

            if img1[aRect_sy + y, aRect_sx + x, 2] >= img2[aRect_sy + y, aRect_sx + x, 2]:
                out_img[aRect_sy + y, aRect_sx + x, 2] = abs(img1[aRect_sy + y, aRect_sx + x, 2] - img2[aRect_sy + y, aRect_sx + x, 2]);
            else:
                out_img[aRect_sy + y, aRect_sx + x, 2] = abs(img2[aRect_sy + y, aRect_sx + x, 2] - img1[aRect_sy + y, aRect_sx + x, 2]);

            absSum = int(out_img[aRect_sy + y, aRect_sx + x, 0]) + int(out_img[aRect_sy + y, aRect_sx + x, 1]) + int(out_img[aRect_sy + y, aRect_sx + x, 2])
            if absSum >= 120:
                chCount = chCount + 1;
    
    changeRate = (chCount / allPixels) * 100.0
    
    return changeRate
    
    return 0;

def bRectDiff(img1, img2):
    global bRect_sx, bRect_sy, bRect_ex, bRect_ey;

    width = bRect_ex - bRect_sx;
    height = bRect_ey - bRect_sy;
    changeRate = 0.0;
    
    chCount = 0;
    allPixels = width * height;
    
    for x in range(0, width) :
         for y in range(0, height) :
            if img1[bRect_sy + y,  bRect_sx + x, 0] >= img2[bRect_sy + y, bRect_sx + x, 0]:
                out_img[bRect_sy + y, bRect_sx + x, 0] = abs(img1[bRect_sy + y, bRect_sx + x, 0] - img2[bRect_sy + y, bRect_sx + x, 0]);
            else:
                out_img[bRect_sy + y, bRect_sx + x, 0] = abs(img2[bRect_sy + y, bRect_sx + x, 0] - img1[bRect_sy + y, bRect_sx + x, 0]);

            if img1[bRect_sy + y, bRect_sx + x, 1] >= img2[bRect_sy + y, bRect_sx + x, 1]:
                out_img[bRect_sy + y, bRect_sx + x, 1] = abs(img1[bRect_sy + y, bRect_sx + x, 1] - img2[bRect_sy + y, bRect_sx + x, 1]);
            else:
                out_img[bRect_sy + y, bRect_sx + x, 1] = abs(img2[bRect_sy + y, bRect_sx + x, 1] - img1[bRect_sy + y, bRect_sx + x, 1]);

            if img1[bRect_sy + y, bRect_sx + x, 2] >= img2[bRect_sy + y, bRect_sx + x, 2]:
                out_img[bRect_sy + y, bRect_sx + x, 2] = abs(img1[bRect_sy + y, bRect_sx + x, 2] - img2[bRect_sy + y, bRect_sx + x, 2]);
            else:
                out_img[bRect_sy + y, bRect_sx + x, 2] = abs(img2[bRect_sy + y, bRect_sx + x, 2] - img1[bRect_sy + y, bRect_sx + x, 2]);

            absSum = int(out_img[bRect_sy + y, bRect_sx + x, 0]) + int(out_img[bRect_sy + y, bRect_sx + x, 1]) + int(out_img[bRect_sy + y, bRect_sx + x, 2])
            if absSum >= 120:
                chCount = chCount + 1;
    
    changeRate = (chCount / allPixels) * 100.0
    
    return changeRate

def loadRect():
    global aRect_sx, aRect_sy, aRect_ex, aRect_ey;
    global bRect_sx, bRect_sy, bRect_ex, bRect_ey;
    global caribRectFilePath;
    
    file =  open(caribRectFilePath, encoding='utf-8')

    str1 = file.readline()
    str2 = file.readline()
    
    ary1 = str1.split(':');
    ary1 = ary1[1].split(',');
    aRect_sx = int(ary1[0]);
    aRect_sy = int(ary1[1]);
    aRect_ex = int(ary1[2]);
    aRect_ey = int(ary1[3]);
    
    ary2 = str2.split(':');
    ary2 = ary2[1].split(',');
    bRect_sx = int(ary2[0]);
    bRect_sy = int(ary2[1]);
    bRect_ex = int(ary2[2]);
    bRect_ey = int(ary2[3]);
        
    file.close();
    
    return 0;

DIFF_TIME = 0.5;

def main():

    global aRect_sx, aRect_sy, aRect_ex, aRect_ey;
    global bRect_sx, bRect_sy, bRect_ex, bRect_ey;
    global aRectStartTime, bRectStartTime;
    
    loadRect();
    
    # mixerモジュールの初期化
    pygame.mixer.init();
    
    #処理ループ
    while True:
        currentTime = time.time();
        
        if aRectStartTime == 0:
            aRectStartTime = currentTime;
            ret1, aRectFrame1 = capture.read()
            
        aRectTimeDiff = currentTime - aRectStartTime;
        
        if aRectTimeDiff > aRectTimeSpan:
            aRectStartTime = currentTime;
            ret2, aRectFrame2 = capture.read()
            
            #cv2.imshow("afr1", aRectFrame1)
            #cv2.imshow("afr2", aRectFrame2)
            
            r1 = aRectDiff(aRectFrame1, aRectFrame2);
            if r1 >= aRectDiffKijun:
            	pygame.mixer.music.load('./taiko.mp3');
            	pygame.mixer.music.play(1);
            	
            str1 = 'ar1:' + str(r1) + '%'
            #print(str1);
            aRectFrame1 = aRectFrame2

        if bRectStartTime == 0:
            bRectStartTime = currentTime;
            ret1, bRectFrame1 = capture.read()
            
        bRectTimeDiff = currentTime - bRectStartTime;
        
        if bRectTimeDiff > bRectTimeSpan:
            bRectStartTime = currentTime;
            ret2, bRectFrame2 = capture.read()
            
            #cv2.imshow("bfr1", bRectFrame1)
            #cv2.imshow("bfr2", bRectFrame2)
            
            r2 = bRectDiff(bRectFrame1, bRectFrame2);
            if r2 >= bRectDiffKijun:
            	pygame.mixer.music.load('./taikofuti.mp3');
            	pygame.mixer.music.play(1);
            
            str1 = 'br1:' + str(r1) + '%'
            #print(str1);
            bRectFrame1 = bRectFrame2

        
        #カメラ画像を読み込む
        ret, frame = capture.read()
        #画像ファイルを読み込む
        #frame = cv2.imread("lena.jpg")

        k = cv2.waitKey(1)
        #Escキー or 'q'を押すと終了
        if k == 27 or k == ord("q") :
            print(">>> Exit")
            break
            
        cv2.rectangle(frame, (aRect_sx, aRect_sy), (aRect_ex, aRect_ey), (255, 0, 0), 5)
        cv2.rectangle(frame, (bRect_sx, bRect_sy), (bRect_ex, bRect_ey), (0, 255, 0), 5)

        cv2.imshow("img", frame)

    capture.release()
    cv2.destroyAllWindows()

    pygame.mixer.music.stop();
    
    return 0
    
main()