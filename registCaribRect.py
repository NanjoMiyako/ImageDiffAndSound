import cv2
import sys

args = sys.argv

print(len(sys.argv))



#diffFolder = args[1];
#diffEdgeFolder = args[2]


mouse_sx = 0;
mouse_sy = 0;
mouse_ex = 0;
mouse_ey = 0;

sFlg = False;
eFlg = False;
dragFlg = False;

callCount = 0;

def callback(event, x, y, flags, param):
    global mouse_sx, mouse_ex, mouse_sy, mouse_ey, dragFlg;
    global capture;
    global sFlg, eFlg;
    global callCount;

    #マウスの左ボタンがクリックされたとき
    if event == cv2.EVENT_LBUTTONDOWN:
        print("aaa")
        
        dragFlg = True
        mouse_sx = x;
        mouse_sy = y;
        
        sFlg = True;
        eFlg = False;
        

    #マウスの左ボタンが離されたとき
    if event == cv2.EVENT_LBUTTONUP and dragFlg == True:
        print("bbb")
        
        if mouse_sx <= x :
            mouse_ex = x
        else:
            mouse_ex = mouse_sx
            mouse_sx = x
            
        if mouse_sy <= y :
            mouse_ey = y
        else:
            mouse_ey = mouse_sy
            mouse_sy = y
        
        dragFlg = False;
        sFlg = False;
        eFlg = True;
        
    #カメラ画像を読み込む
    ret, frame = capture.read()
    #画像ファイルを読み込む
    #frame = cv2.imread("lena.jpg")


    
    
    if eFlg == True:
        cv2.rectangle(frame, (mouse_sx, mouse_sy), (mouse_ex, mouse_ey), (0, 0, 0), -1)
       
        if callCount >= 20:
            sFlg = False;
            eFlg = False;
            callCount = 0;
        else:
            callCount = callCount + 1;
        
    elif sFlg == True:
        cv2.drawMarker(frame, (mouse_sx, mouse_sy), (0, 0, 255), markerType=cv2.MARKER_TILTED_CROSS, markerSize=15);
        
 
    cv2.imshow("img", frame)
    return 0

global g_width;
global g_height;

g_width = 320;
g_height = 240;
# VideoCapture オブジェクトを取得します
capture = cv2.VideoCapture(0)

print(capture.set(cv2.CAP_PROP_FRAME_WIDTH, g_width))
print(capture.set(cv2.CAP_PROP_FRAME_HEIGHT, g_height))


cv2.namedWindow("img", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("img", callback)

out_img = cv2.imread("white.jpg");


global FuncCount
FuncCount = 0;

import time

      

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

def main():

    global dragFlg, sFlg, eFlg;
    global mouse_sx, mouse_ex;
    global mouse_sy, mouse_ey;
    global aRect_sx, aRect_sy, aRect_ex, aRect_ey;
    global bRect_sx, bRect_sy, bRect_ex, bRect_ey;
    global aRectFlg, bRectFlg;
    
    print(dragFlg);
    print(sFlg);
    print(eFlg);
    
    #処理ループ
    while True:
        #カメラ画像を読み込む
        ret, frame = capture.read()
        #画像ファイルを読み込む
        #frame = cv2.imread("lena.jpg")

        k = cv2.waitKey(1)
        #Escキーを押すと終了
        if k == 27 or k == ord("q") :
            print(">>> Exit")
            break
            
        #aを押すと今書いた矩形領域aを保存1
        elif k == ord("a") and eFlg == True:
            aRect_sx = mouse_sx;
            aRect_sy = mouse_sy;
            aRect_ex = mouse_ex;
            aRect_ey = mouse_ey;
            aRectFlg = True;
            
        #bを押すと今書いた矩形領域bを保存2
        elif k == ord("b") and eFlg == True:
            bRect_sx = mouse_sx;
            bRect_sy = mouse_sy;
            bRect_ex = mouse_ex;
            bRect_ey = mouse_ey;
            
            str1 = str(bRect_sx) + ',' + str(bRect_sy) + ',' + str(bRect_ex) + ',' + str(bRect_ey)
            print(str1)
            bRectFlg = True;

        #sを押すと矩形領域をファイルに保存
        elif k == ord("s"):
            f = open('./caribRects.txt', mode='w', encoding='utf-8');
            
            str1 = 'aRect:'+ str(aRect_sx) + ',' + str(aRect_sy) + ',' + str(aRect_ex) + ',' + str(aRect_ey) + '\n'
            f.write(str1)

            str1 = 'bRect:'+ str(bRect_sx) + ',' + str(bRect_sy) + ',' + str(bRect_ex) + ',' + str(bRect_ey) + '\n'
            f.write(str1)
            
            f.close();

            print('ファイル保存しました');
            
        if aRectFlg == True:
            cv2.rectangle(frame, (aRect_sx, aRect_sy), (aRect_ex, aRect_ey), (255, 0, 0), 5)

        if bRectFlg == True:
            cv2.rectangle(frame, (bRect_sx, bRect_sy), (bRect_ex, bRect_ey), (0, 255, 0), 5)

        cv2.imshow("img", frame)

    capture.release()
    cv2.destroyAllWindows()

    
    return 0
    
main()