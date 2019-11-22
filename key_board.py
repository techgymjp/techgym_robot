#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import select
import tty
import termios

# キーボードコントロールクラス


class KeyBoard(object):

    # 初期化
    def __init__(self):
        # 標準入力のファイルディスクリプタを取得する
        self.__fd = sys.stdin.fileno()
        # ファイルディスクリプタの属性を取得、変更する
        self.__old = termios.tcgetattr(self.__fd)
        new = termios.tcgetattr(self.__fd)
        new[3] = new[3] & ~termios.ICANON
        termios.tcsetattr(self.__fd, termios.TCSANOW, new)

        # cbreakモードに設定
        tty.setcbreak(self.__fd)

    def __del__(self):
        # ファイルディクリプタの属性を元に戻す
        termios.tcsetattr(self.__fd, termios.TCSANOW, self.__old)

    # 入力キーを受け取る
    def get_key(self):
        # キー入力をポーリング
        rlist, _, _ = select.select([sys.stdin], [], [], 0)

        if rlist:
            key = sys.stdin.read(1)
        else:
            pass
            key = None
        return key
