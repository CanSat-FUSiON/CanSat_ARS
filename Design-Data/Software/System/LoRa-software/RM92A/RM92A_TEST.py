'''
command program
'''
from micropython import const
from machine import Pin, UART, reset, Timer, lightsleep
from utime import ticks_ms
import time, os
import sys

from FUSiON_RM92A import RM92A #無線機

'''
通信関係
'''
# UART通信
rm_uart= UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

'''
クラスからインスタンスを生成
'''
rm = RM92A(rm_uart)

'''
Timerオブジェクト(周期処理用)
'''
downlink_timer = Timer()

'''
ダウンリンク（割り込み処）
'''
def downlink(t):
    send_data = bytearray(21)
    send_data[0] = 0x24
    send_data[1] = 1 #ここ以降に各データ（1byte以下）を格納してください
    send_data[2] = 1
    send_data[3] = 1
    send_data[4] = 1
    send_data[5] = 1
    send_data[6] = 1
    send_data[7] = 1

    rm.send(0xFFFF, send_data)
downlink_timer.init(period=5000, callback=downlink)

while True:
    time.sleep(0.1)