#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from key_board import KeyBoard
from moter_control import MotorControl
import time

MAX_VEL = 250
MIN_VEL = -MAX_VEL

# メインループ
def main():
    print('[Info]Start program')
    # キーボーボクラスの初期化
    key = KeyBoard()

    # モータコントロールクラスの初期化
    moter = MotorControl()
    moter.setup()

    while True:
        # キー入力を取得
        c =  key.get_key()

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
                msg = '右旋回  :'
                moter.set_target_velocity(MAX_VEL, MIN_VEL)
            elif c == 'x':
                msg = '後退  :'
                moter.set_target_velocity(MIN_VEL, MIN_VEL)
            print(msg + c)
        # 'q' が押された場合は終了
        if c == 'q':
            break
if __name__ == '__main__':
    try:
        # メインループ
        main()
        print('[Info]Exit')

    except KeyboardInterrupt:
        # Ctrl-Cが押された時
        print('[Info]Ctrl-C pressed ...')
