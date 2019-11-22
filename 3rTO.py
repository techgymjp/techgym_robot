#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from key_board import KeyBoard
from moter_control import MotorControl
from image_detect import ImageDetect
import time

MAX_VEL = 250
MIN_VEL = -MAX_VEL

WIDTH  = 320
HEIGHT = 240

# キー入力で動作させる
def key_ctrl(c, moter):
    # キーに値が設定されている場合
    if c != None:
        if c == 'w':
            msg = '前進  :'
            moter.set_target_velocity(MAX_VEL, MAX_VEL)
        elif c == 'a':
            msg = '左旋回:'
            moter.set_target_velocity(MIN_VEL, MAX_VEL)
        elif c == 's':
            msg = '停止  :'
            moter.set_target_velocity(0,0)
        elif c == 'd':
            msg = '停止  :'
            moter.set_target_velocity(MAX_VEL, MIN_VEL)
        elif c == 'x':
            msg = '後退  :'
            moter.set_target_velocity(MIN_VEL, MIN_VEL)
        print(msg + c)

# メインループ
def main():
    print('[Info]Start program')
    # キーボーボクラスの初期化
    key = KeyBoard()

    # モータコントロールクラスの初期化
    moter = MotorControl()
    moter.setup()

    # 画像認識クラス
    resolution = (WIDTH, HEIGHT)
    img = ImageDetect(resolution)

    # ボールを認識するときに使うしきい値
    ball_lower = [170, 100, 100]
    ball_upper = [180, 255, 255]

    # ゴールを認識するときに使うしきい値
    goal_lower = [100, 100, 100]
    goal_upper = [115, 255, 255]

    while True:
        # ボールの画像を取得
        rect = img.get_image(ball_lower, ball_upper)
        b_x0 = rect[0]
        b_x1 = rect[0] + rect[2]
        b_y0 = rect[1]
        b_y1 = rect[1] + rect[3]
        # 画像を表示
        img.view_image()

        # ゴールの画像を取得
        img.get_image(goal_lower, goal_upper)
        # 画像を表示
        img.view_image()

        # ボールを認識していない
        if b_x0 == 0 and b_x1 == 0:
            moter.set_target_velocity(0, 0)
        else:
            # 画面の右側にボールがある
            if b_x0 >= (WIDTH / 2) and b_x1 >= (WIDTH / 2):
                moter.set_target_velocity(40, -40)
            # 画面の左側にボールがある
            elif b_x0 < (WIDTH / 2) and b_x1 < (WIDTH / 2):
                moter.set_target_velocity(-40, 40)
            # ボールに近づいた
            elif b_x1*b_y1 >= 76000:
                moter.set_target_velocity(0, 0)
            else:
                moter.set_target_velocity(150, 150)

        # キー入力を取得
        c =  key.get_key()
        # キー入力で動作
        #key_ctrl(c, moter)

        # 'q' が押された場合は終了
        if c == 'q':
            moter.set_target_velocity(0, 0)
            break
if __name__ == '__main__':
    try:
        # メインループ
        main()
        print('[Info]Exit program')

    except KeyboardInterrupt:
        # Ctrl-Cが押された時
        print('[Info]Ctrl-C pressed ...')
