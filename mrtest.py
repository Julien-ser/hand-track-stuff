import cv2
import streamlit as st
import mediapipe as mp
import Hand_track as h
from PIL import Image
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer

detector = h.handDetector(maxHands = 1, detectionCon = 0.75)

st.title("Webcam shit beach")

placeholder = st.empty()

def video_frame_callback(frame):
    global placeholder
    img = frame.to_ndarray(format="bgr24")
    img = detector.findHands(img, True)
    img = cv2.flip(img, 1)

    #print(img.shape)
    lmLis = detector.findPos(img)

    #img[0:200, 0:200] = overlay[0]

    x = []
    y = []

    if len(lmLis) != 0:


        for id, xa, ya in lmLis:
            x.append(xa)
            y.append(ya)

        min_x = min(x)
        min_y = min(y)
        max_x = max(x)
        max_y = max(y)

        #cv2.rectangle(img, (min_x, min_y), (max_x, max_y), (0, 255, 255), 2)

        try:
            if lmLis[8][2] > lmLis[6][2] and lmLis[16][2] > lmLis[14][2] and lmLis[20][2] > lmLis[18][2] and lmLis[10][2] > lmLis[12][2]:
                #cv2.putText(img, 'Fuck you', (0, 0), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)
                placeholder.empty()
                placeholder.text('Middle finger 🖕')

            if lmLis[8][2] < lmLis[6][2] and lmLis[16][2] > lmLis[14][2] and lmLis[20][2] > lmLis[18][2] and lmLis[10][2] > lmLis[12][2]:
                #cv2.putText(img, 'Peace', (0, 0), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)
                placeholder.empty()
                placeholder.text('Peace ✌')

            if lmLis[8][2] > lmLis[6][2] and lmLis[16][2] > lmLis[14][2] and lmLis[20][2] > lmLis[18][2] and lmLis[10][2] < lmLis[12][2]:
                if lmLis[4][2] < lmLis[6][2]:
                    #cv2.putText(img, 'Thumbs up', (0, 0), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)
                    placeholder.empty()
                    placeholder.text('Thumbs Up 👍')
                else:
                    #cv2.putText(img, 'Fist', (0, 0), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)
                    placeholder.empty()
                    placeholder.text('Fist 👊')

            if lmLis[8][2] < lmLis[6][2] and lmLis[16][2] < lmLis[14][2] and lmLis[20][2] < lmLis[18][2] and lmLis[10][2] > lmLis[12][2]:
                if abs(abs(lmLis[12][1] - lmLis[16][1])/(abs(lmLis[12][1] - lmLis[8][1])) + 1) >= 3 and abs(abs(lmLis[12][1] - lmLis[16][1])/(abs(lmLis[20][1] - lmLis[16][1]) + 1)) >= 3:
                    #cv2.putText(img, 'Vulcans', (0, 0), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)
                    placeholder.text('Vulcan salute 🖖')
        except:
            pass
    return img
    
webrtc_streamer(key="example", video_frame_callback=video_frame_callback)
