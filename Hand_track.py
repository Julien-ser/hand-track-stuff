import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self,mode=False,maxHands=2,modelComplexity=1,detectionCon=0.5,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity=modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        

        #sets up hand detection
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplexity,
                                        self.detectionCon, self.trackCon)

        #sets up webcam drawing
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        #processes to see if the hand is there
        self.results = self.hands.process(imgRGB)

        #checks to see if the hand is tracked
        if self.results.multi_hand_landmarks:
            #for point in hand detection
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    #draws each point for the hand
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
                    #the last param draws lines
        return img

    def findPos(self, img, handNo=0, draw=True):

        lmList = []

        if self.results.multi_hand_landmarks:

            myhand = self.results.multi_hand_landmarks[handNo]
            
            #tracks coordinates
            for id, lm in enumerate(myhand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
    ##            if id == 8:
    ##                cv2.circle(img, (cx,cy), 15, (255, 0,255), cv2.FILLED)
    ##                     
    ##            elif id == 12:
    ##                cv2.circle(img, (cx,cy), 15, (0, 255,255), cv2.FILLED)

        return lmList 
                    


def main():
    pTime = 0
    cTime = 0

    cap = cv2.VideoCapture(0)

    detector = handDetector()
    
    while True:
        
        #gets camera input
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = cv2.resize(img, (700, 500))

        img = detector.findHands(img)

        posList = detector.findPos(img)

        if len(posList) == 0:
            pass
        else:
            print(posList)

        #tracks fps
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,5,
                    (255,255,255), 3)


        #cv2.namedWindow('Image',cv2.WINDOW_NORMAL)
        #cv2.resizeWindow('Image', 1200,600)
        cv2.imshow('Image', img)

        cv2.waitKey(1)

if __name__ == 'main':
    main()
