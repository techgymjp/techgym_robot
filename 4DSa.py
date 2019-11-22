#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# メインループ
def main():
    print('[Info]Start program')

if __name__ == '__main__':
    try:
        # メインループ
        main()
        print('[Info]Exit')

    except KeyboardInterrupt:
        # Ctrl-Cが押された時
        print('[Info]Ctrl-C pressed ...')
