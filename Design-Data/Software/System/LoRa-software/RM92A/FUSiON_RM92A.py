from math import fabs
from machine import UART, Pin
import time
import binascii

# 使い方
# import PQ_RM92A
# rm92a = RM92A(1, 115200, 8, 9)
# rm92a.begin()
# rm92a.send(tx_data)

class RM92A():
    def __init__(self, rm_uart):   # コンストラクタの宣言
        self.rm = rm_uart
        self.rx_read_lock = False
        self.rx_write_p = 0

    def begin(self): #RM92Aの起動
        time.sleep(0.5)
        self.rm.write("\r\n")
        time.sleep(0.1)
        self.rm.write("1\r\n")
        time.sleep(0.1)
        self.rm.write("y\r\n")
        time.sleep(0.1)
        self.rm.write("s\r\n") 
        return 0

    # 一文字読む．"\n"に達したらlockする．
    def rx_update(self):
        rx_buf = []
        if self.rx_read_lock == False:
            while self.rm.any()>0:
                print('any data')
                data = self.rm.read(1)   # 一文字ずつ読む
                rx_buf.append(data)

                if data == "\n":
                    self.rx_write_p = 0
                    self.rx_read_lock = True
                    break
                else:
                    self.rx_write_p =+ 1
        return self.rx_read_lock

    #
    def read_data(self):
        lock = self.rx_update()
        if lock:
            self.rx_read_lock = False
            return self.rx_buf
        else:   # データが溜まってないのでスルー
            pass
        
    # 一文字読む．"\n"に達したらlockする．
    def rx_reading(self):
        rx_buf = []
        lock = 0
        if self.rx_read_lock == False:
            while self.rm.any()>0:
                data = self.rm.read(1)   # 一文字ずつ読む
                rx_buf.append(data)
                if data == "\n":
                    self.rx_write_p = 0
                    self.rx_read_lock = True
                    lock = 1
                else:
                    self.rx_write_p =+ 1
            return rx_buf

    def send(self, dst, tx_data):
        size = len(tx_data)
        tx_buf = [0]*(size+6)
        tx_buf[0] = int('0x40')     # '@'
        tx_buf[1] = int('0x40')     # '@'    
        tx_buf[2] = size
        tx_buf[3] = int((dst >> 8) & 0xff)
        tx_buf[4] = int((dst >> 0) & 0xff)
        for i in range(size):
            tx_buf[i+5] = int(tx_data[i])
        tx_buf[size+5] = int('0xAA')
        self.rm.write(bytearray(tx_buf))
