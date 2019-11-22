#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from key_board import KeyBoard

# メインループ
def main():
    print('[Info]Start program')
    # キーボーボクラスの初期化
    key = KeyBoard()

    while True:
        # キー入力を取得
        c =  key.get_key()

        # キーに値が設定されている場合
        if c != None:
            msg = '入力:'
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
