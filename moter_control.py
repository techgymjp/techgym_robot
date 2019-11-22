#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dynamixel_sdk import *
import time

# 使用している機種：XL430-W250-T
# マニュアル：http://emanual.robotis.com/docs/en/dxl/x/xl430-w250/

# Dynamixelの設定
_LEFT_WHELL_ID = 1
_RIGHT_WHELL_ID = 2
_BROAD_CAST_ID = 254
_PROTOCOL_VERSION = 2.0
_BAUDRATE = 57600

# トルクON/OFFの値
_TRQ_ON = 1
_TRQ_OFF = 0

# 速度の最小,最大値
_VELOCITY_MIN = -260  # XL430-W250-T
_VELOCITY_MAX = 260  # XL430-W250-T

# Dynamixelのコントロールテーブルのアドレス
_DXL_ADDR_TORQUE_ENABLE = 64
_DXL_ADDR_GOAL_VELOCITY = 104
_DXL_ADDR_PRESENT_VELOCITY = 128
_DXL_ADDR_PRESENT_INPUT_VOLTAGE = 144
_DXL_ADDR_PRESENT_TEMPERATURE = 146

# Dynamixelのコントロールテーブルのアイテムのアドレス長
_DXL_LEN_GOAL_VELOCITY = 4
_DXL_LEN_PRESENT_VELOCITY = 4

# Dynamixelのコントロールクラス


class MotorControl(object):

    # ボーレートやポート、パケットのハンドラーを初期化
    def __init__(self, port='/dev/ttyACM0'):
        self.__baudrate = _BAUDRATE
        self.__port_handler = PortHandler(port)
        self.__packet_handler = PacketHandler(_PROTOCOL_VERSION)
        self.__group_write = GroupSyncWrite(self.__port_handler,
                                            self.__packet_handler,
                                            _DXL_ADDR_GOAL_VELOCITY,
                                            _DXL_LEN_GOAL_VELOCITY)

        self.__group_read = GroupSyncRead(self.__port_handler,
                                          self.__packet_handler,
                                          _DXL_ADDR_PRESENT_VELOCITY,
                                          _DXL_LEN_PRESENT_VELOCITY)

    # Dynamixelを動作させるための準備
    def setup(self):
        # 通信ポートをオープン
        if self.__port_handler.openPort():
            print('[Info]Succeeded to open the port : %s' % self.__port_handler.getPortName())
        else:
            print('[Error]Failed to open the port')
            return False

        # 通信ボーレートを設定
        if self.__port_handler.setBaudRate(self.__baudrate):
            print('[Info]Succeeded to change the baudrate : %d' % self.__port_handler.getBaudRate())
        else:
            print('[Error]Failed to change the baudrate')
            return False

        # 接続確認
        for id in range(1, 3):
            dxl_model_number, dxl_comm_result, dxl_error = self.__packet_handler.ping(self.__port_handler, id)
            if dxl_comm_result != COMM_SUCCESS:
                print("[Error]%s" % self.__packet_handler.getTxRxResult(dxl_comm_result))
                return False
            elif dxl_error != 0:
                print("[Error]%s" % self.__packet_handler.getRxPacketError(dxl_error))
                return False
            else:
                print("[Info]ID:%03d ping Succeeded. Dynamixel model number : %d" % (id, dxl_model_number))

        # トルクON
        self.torque_enable()

        # 同期読み込みの設定
        self.__group_read.addParam(_LEFT_WHELL_ID)
        self.__group_read.addParam(_RIGHT_WHELL_ID)

    # 終了処理
    def exit(self):
        # トルクOFF
        self.torque_disable()
        # 通信ポートのクリアとクローズ
        self.__port_handler.clearPort()
        self.__port_handler.closePort()

    # DynamixelのトルクをONにする
    def torque_enable(self):
        # 左右のDynamixelに対してトルクON司令を送る
        self.__packet_handler.write1ByteTxRx(self.__port_handler,
                                             _BROAD_CAST_ID,
                                             _DXL_ADDR_TORQUE_ENABLE,
                                             _TRQ_ON)

    # DynamixelのトルクをOFFにする
    def torque_disable(self):
        # トルクがOFFになるまでループする
        while True:
            # 左右のDynamixelに対してトルクOFF司令を送る
            result, error = self.__packet_handler.write1ByteTxRx(self.__port_handler,
                                                                 _BROAD_CAST_ID,
                                                                 _DXL_ADDR_TORQUE_ENABLE,
                                                                 _TRQ_OFF)
            # 戻り値がエラーの場合は、エラーログを出す
            if result != COMM_SUCCESS:
                print("[Error]1%s" % self.__packet_handler.getTxRxResult(result))
            elif error != 0:
                print("[Error]2%s" % self.__packet_handler.getRxPacketError(error))
            else:
                break

            # 同期書き込み、読み込みのパラメータをクリア
            self.__group_read.clearParam()
            self.__group_write.clearParam()
            time.sleep(0.01)

    # 目標速度を設定
    def set_target_velocity(self, left_vel, right_vel):
        # 速度の最小、最大値をリミット
        if left_vel >= _VELOCITY_MAX:
            left_vel = _VELOCITY_MAX
        elif left_vel <= _VELOCITY_MIN:
            left_vel = _VELOCITY_MIN

        if right_vel >= _VELOCITY_MAX:
            right_vel = _VELOCITY_MAX
        elif right_vel <= _VELOCITY_MIN:
            right_vel = _VELOCITY_MIN

        # 4Byteデータを1Byteの配列に設定
        left_velocity = [DXL_LOBYTE(DXL_LOWORD(left_vel)),
                         DXL_HIBYTE(DXL_LOWORD(left_vel)),
                         DXL_LOBYTE(DXL_HIWORD(left_vel)),
                         DXL_HIBYTE(DXL_HIWORD(left_vel))]

        # 4Byteデータを1Byteの配列に設定
        right_velocity = [DXL_LOBYTE(DXL_LOWORD(right_vel)),
                          DXL_HIBYTE(DXL_LOWORD(right_vel)),
                          DXL_LOBYTE(DXL_HIWORD(right_vel)),
                          DXL_HIBYTE(DXL_HIWORD(right_vel))]

        # 左右のDynamixelへの速度司令を同期書き込み処理に登録
        self.__group_write.addParam(_LEFT_WHELL_ID, left_velocity)
        self.__group_write.addParam(_RIGHT_WHELL_ID, right_velocity)

        # 速度司令を送信
        dxl_comm_result = self.__group_write.txPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("[Error]%s" % self.__packet_handler.getTxRxResult(dxl_comm_result))

        # 同期書き込みの値をクリア
        self.__group_write.clearParam()

        return True

    # 現在速度を取得
    def get_present_velocity(self):

        # 現在速度を取得
        self.__group_read.txRxPacket()

        for id in range(1, 3):
            # データが取得出来たか確認
            get_data_result = self.__group_read.isAvailable(id,
                                                            _DXL_ADDR_PRESENT_VELOCITY,
                                                            _DXL_LEN_PRESENT_VELOCITY)
            if get_data_result != 1:
                print("[Error]ID:%03d groupSyncRead getdata failed" % (id))

        # 取得した左右の現在速度を設定
        left = self.__group_read.getData(_LEFT_WHELL_ID,
                                         _DXL_ADDR_PRESENT_VELOCITY,
                                         _DXL_LEN_PRESENT_VELOCITY)
        right = self.__group_read.getData(_RIGHT_WHELL_ID,
                                          _DXL_ADDR_PRESENT_VELOCITY,
                                          _DXL_LEN_PRESENT_VELOCITY)

        return left, right

    # バッテリーの電圧を取得する
    def get_vattary_voltage(self):
        left, result, error = self.__packet_handler.read1ByteTxRx(self.__port_handler,
                                                                  1,
                                                                  _DXL_ADDR_PRESENT_INPUT_VOLTAGE)

        # 戻り値がエラーの場合は、エラーログを出す
        if result != COMM_SUCCESS:
            print("[Error]1%s" % self.__packet_handler.getTxRxResult(result))
        elif error != 0:
            print("[Error]2%s" % self.__packet_handler.getRxPacketError(error))

        right, result, error = self.__packet_handler.read1ByteTxRx(self.__port_handler,
                                                           2,
                                                           _DXL_ADDR_PRESENT_INPUT_VOLTAGE)
        # 戻り値がエラーの場合は、エラーログを出す
        if result != COMM_SUCCESS:
            print("[Error]1%s" % self.__packet_handler.getTxRxResult(result))
        elif error != 0:
            print("[Error]2%s" % self.__packet_handler.getRxPacketError(error))

        return (left + right)/2
