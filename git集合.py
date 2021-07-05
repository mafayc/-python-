import cv2
import sys
import mediapipe as mp
#from handutil import HandDetector
# 打开摄像头
cap = cv2.VideoCapture(0)
# 创建一个手势识别对象
class HandDetector():
    '''
    手势识别类
    '''
    def __init__(self, mode=False, max_hands=1, detection_con=0.5, track_con=0.5):
        '''
        初始化
        :param mode: 是否静态图片，默认为False
        :param max_hands: 最多几只手，默认为2只
        :param detection_con: 最小检测信度值，默认为0.5
        :param track_con: 最小跟踪信度值，默认为0.5
        '''
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con

        self.hands = mp.solutions.hands.Hands(self.mode, self.max_hands, self.detection_con, self.track_con)

    def find_hands(self, img, draw=True):
        '''
        检测手势
        :param img: 视频帧图片
        :param draw: 是否画出手势中的节点和连接图
        :return: 处理过的视频帧图片
        '''
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # 处理图片，检测是否有手势，将数据存进self.results中
        self.results = self.hands.process(imgRGB)
        if draw:
            if self.results.multi_hand_landmarks:
                for handlms in self.results.multi_hand_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(img, handlms, mp.solutions.hands.HAND_CONNECTIONS)
        return img

    def find_positions(self, img, hand_no=0):
        '''
        获取手势数据
        :param img: 视频帧图片
        :param hand_no: 手编号（默认第1只手）
        :return: 手势数据列表，每个数据成员由id, x, y组成，代码这个手势位置编号以及在屏幕中的位置
        '''
        self.lmslist = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmslist.append([id, cx, cy])

        return self.lmslist
















    
detector = HandDetector()
tip_ids = [4, 8, 12, 16, 20]
while True:
    success, img = cap.read()

    if success:
        # 检测手势
        img = detector.find_hands(img, draw=True)
        # 获取手势数据
        lmslist = detector.find_positions(img)
        if len(lmslist) > 0:
            fingers = []
            for tid in tip_ids:
                # 找到每个指尖的位置
                x, y = lmslist[tid][1], lmslist[tid][2]
                cv2.circle(img, (x, y), 10, (0, 255, 0), cv2.FILLED)
                # 如果是大拇指，如果大拇指指尖x位置大于大拇指第二关节的位置，则认为大拇指打开，否则认为大拇指关闭
                if tid == 4:
                    if lmslist[tid][1] > lmslist[tid - 1][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                # 如果是其他手指，如果这些手指的指尖的y位置大于第二关节的位置，则认为这个手指打开，否则认为这个手指关闭
                else:
                    if lmslist[tid][2] < lmslist[tid - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                        
                # fingers是这样一个列表，5个数据，0代表一个手指关闭，1代表一个手指打开
                # 判断有几个手指打开

            
            if fingers==[1,0,0,0,0]:
                cv2.imwrite('jg.jpg',img)  
                
            if fingers==[0,0,1,0,0]:
                sys.exit(0)                          #关闭程序
                      
        cv2.imshow('Image', img)

    if cv2.waitKey(5) & 0xFF == 27:                  #关闭程序
        sys.exit(0)

