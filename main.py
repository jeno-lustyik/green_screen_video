import cv2 as cv
import numpy as np
import streamlit as st
from PIL import Image

img = st.file_uploader('Upload your desired background here:')

# width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
# heigth = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))

if img is not None:
    img = Image.open(img)
    img.save('img.jpg')
    img = cv.imread('img.jpg')
    select = st.selectbox('Choose a video to change the background on:', options=['Jameson', 'JOJO', 'Patrick Bateman'])

    if select == 'Jameson':
        video = cv.VideoCapture('video/greenscreen_jameson.mp4')
    if select == 'Patrick Bateman':
        video = cv.VideoCapture('video/bateman_greenscreen.mp4')
    if select == 'JOJO':
        video = cv.VideoCapture('video/AYAY.mp4')

    if st.button('Render video'):
        width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
        heigth = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))

        while True:
            ret, frame = video.read()

            # To have a looping video without crashing, we run the code if the ret variable is not none.
            if ret:

                # Set the size of the image to the size of the video used
                frame = cv.resize(frame, (width, heigth))
                img = cv.resize(img, (width, heigth))

                hsv_img = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

                lower_g = (38, 40, 30)
                upper_g = (85, 255, 255)
                mask = cv.inRange(hsv_img, lower_g, upper_g)
                final = cv.bitwise_and(frame, frame, mask=mask)

                f = frame - final
                f = np.where(f == 0, img, f)

                cv.imshow('video', f)


            # Else, we
            else:
                video.set(cv.CAP_PROP_POS_FRAMES, 0)
                continue

            if cv.waitKey(5) == ord('q'):
                break
        video.release()
        cv.destroyAllWindows()
