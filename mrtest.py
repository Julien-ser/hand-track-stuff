import cv2
import streamlit as st
import Hand_track as h
from PIL import Image
import av
import mediapipe as mp
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

detector = h.handDetector(maxHands = 1, detectionCon = 0.75)

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

st.title("Webcam shit beach")
text = ''

class VideoProcessor:
    global text
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        # img = process(img)
    

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
                    text = 'Middle Finger'
                    
                elif lmLis[8][2] < lmLis[6][2] and lmLis[16][2] > lmLis[14][2] and lmLis[20][2] > lmLis[18][2] and lmLis[10][2] > lmLis[12][2]:
                    text =  'Peace'

                elif lmLis[8][2] > lmLis[6][2] and lmLis[16][2] > lmLis[14][2] and lmLis[20][2] > lmLis[18][2] and lmLis[10][2] < lmLis[12][2]:
                    if lmLis[4][2] < lmLis[6][2]:
                        text = 'Thumbs up'
                    else:
                        text = 'Fist'

                elif lmLis[8][2] < lmLis[6][2] and lmLis[16][2] < lmLis[14][2] and lmLis[20][2] < lmLis[18][2] and lmLis[10][2] > lmLis[12][2]:
                    if abs(abs(lmLis[12][1] - lmLis[16][1])/(abs(lmLis[12][1] - lmLis[8][1])) + 1) >= 3 and abs(abs(lmLis[12][1] - lmLis[16][1])/(abs(lmLis[20][1] - lmLis[16][1]) + 1)) >= 3:
                        text = 'Vulcans'
                else:
                    text = ''
            except:
                pass
        cv2.putText(img, text, (200, 200), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)
        return av.VideoFrame.from_ndarray(img, format="bgr24")
    
webrtc_ctx = webrtc_streamer(
    key="WYH",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": True, "audio": False},
    video_processor_factory=VideoProcessor,
    async_processing=True,
)
