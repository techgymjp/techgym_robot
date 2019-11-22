#!/usr/bin/env python
# -*- coding:utf-8 -*-

import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera

h=0
s=0
v=0
cam = PiCamera()
cam.resolution = (320,240)
cam.framerate = 120
stream = PiRGBArray(cam, size=(320,240))

# イベントコールバック
def callback(event, x, y, flags, param):
    global h,s,v,cam
    # マウスの左ボタンがクリックされた時
    if event == cv2.EVENT_LBUTTONDOWN:
        #cam.capture(stream, 'bgr', use_video_port=True)
        hsv = cv2.cvtColor(stream.array, cv2.COLOR_BGR2HSV)
        h = hsv[y, x, 0]
        s = hsv[y, x, 1]
        v = hsv[y, x, 2]
        cv2.waitKey(1)
        stream.seek(0)
        stream.truncate()

def main():
    global h,s,v
    cv2.namedWindow("RGB", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("RGB", callback, None)

    while True:
        cam.capture(stream, 'bgr', use_video_port=True)
        cv2.imshow('RGB', stream.array)
        hsv = cv2.cvtColor(stream.array, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array([h-5, 100, 100]), np.array([h+5, 255, 255]))
        image_mask = cv2.bitwise_and(stream.array, stream.array, mask=mask)
        cv2.imshow('mask', image_mask)
        print("h:%3d,s:%3d,v:%3d" % (h,s,v))
        cv2.waitKey(1)
        stream.seek(0)
        stream.truncate()
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("EXIT")
