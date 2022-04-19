import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from PIL import Image

img = st.file_uploader('Upload your desired background here:')

if img is not None:
    img = Image.open(img)
    img.save('img.jpg')
    img = cv.imread('img.jpg')

    video = cv.VideoCapture('greenscreen_jameson.mp4')
    width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
    heigth = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))

    while True:
        ret, frame = video.read()

        # frame = cv.resize(frame, (640, 480))
        lower_bound = (30, 40, 40)
        img = cv.resize(img, (width, heigth))

        hsv_img = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        upper_bound = (85, 255, 255)
        mask = cv.inRange(hsv_img, lower_bound, upper_bound)
        final = cv.bitwise_and(frame, frame, mask=mask)

        f = frame - final
        f = np.where(f == 0, img, f)

        cv.imshow('video', frame)
        cv.imshow('mask', f)

        if cv.waitKey(5) == ord('q'):
            break
    video.release()
    cv.destroyAllWindows()
