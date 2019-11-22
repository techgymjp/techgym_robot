#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np    

# 0 <= h <= 180 色相
# 0 <= s <= 255 彩度
# 0 <= v <= 255 明度
# 画像認識クラス


class ImageDetect(object):

   #ラズパイカメラの初期化
   def  __init__(self, resolution=(320,240), framerate=60):
      self._camera = PiCamera()
      self._camera.resolution = resolution
      self._camera.framerate = framerate
      self._stream = PiRGBArray(self._camera, size=resolution)
      
   # ウィンドウの終了処理
   def __del__(self):
      cv2.destroyAllWindows()

   # 画像認識
   def _detect_image(self, image, lower, upper):
      # RGB画像をHSV画像に変換
      hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
      # マスクする画像を作成
      mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
      # 指定した閾値で画像をマスク
      image_mask = cv2.bitwise_and(image, image ,mask=mask)

      # オープニング処理のカーネルを作成
      kernel = np.ones((3, 3), np.uint8)
      image = cv2.erode(mask, kernel, iterations=3)
      image = cv2.dilate(image, kernel, iterations=3)

      # 作成したマスク画像を2値化する
      _, th = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

      # マスクした画像から輪郭を抽出する
      contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      # 凸包処理をし、外接矩形を取得
      rects = []
      for contour in contours:
         approx = cv2.convexHull(contour)
         rect = cv2.boundingRect(approx)
         rects.append(np.array(rect))
      return rects

   # 画像を取得
   def get_image(self, lower, upper):
      # カメラ画像を取得
      self._camera.capture(self._stream, 'bgr', use_video_port=True)

      # 物体認識
      rects = self._detect_image(self._stream.array, lower, upper)

      # 認識した物体を四角形で囲う
      rect = [0, 0, 0, 0]
      if len(rects) > 0:
         rect = max(rects, key=(lambda x: x[2] * x[3]))
         cv2.rectangle(self._stream.array,
                       tuple(rect[0:2]),
                       tuple(rect[0:2] + rect[2:4]),
                       (0, 255, 0),
                       thickness=2)
      return rect

   # 画像を描画
   def view_image(self, name='detect_image'):
      cv2.imshow(name, self._stream.array)
      cv2.waitKey(1)
      self._stream.seek(0)
      self._stream.truncate()
