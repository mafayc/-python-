import cv2
import sys
from handutil import HandDetector
cap = cv2.VideoCapture(0)# 打开摄像头
detector = HandDetector()# 创建一个手势识别对象
tip_ids = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()

    if success:
        img = detector.find_hands(img, draw=True)
        lmslist = detector.find_positions(img)
        if len(lmslist) > 0:
            fingers = []
            for tid in tip_ids:
                x, y = lmslist[tid][1], lmslist[tid][2]
                cv2.circle(img, (x, y), 10, (0, 255, 0), cv2.FILLED)
                if tid == 4:
                    if lmslist[tid][1] > lmslist[tid - 1][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                else:
                    if lmslist[tid][2] < lmslist[tid - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)           
            if fingers==[1,0,0,0,0]:
                cv2.imwrite('jg.jpg',img)  
                
            if fingers==[0,0,1,0,0]:
                sys.exit(0)
                      
        cv2.imshow('Image', img)
    if cv2.waitKey(5) & 0xFF == 27:                  #关闭程序
          break
cap.release()
cv2.destroyAllWindows()
