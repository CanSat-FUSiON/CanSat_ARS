'''
モータードライバーの動作確認用のプログラムです．
あくまでも動作確認を目的としているのでモジュール化などはしていません
'''

#必要なモジュール等のインストール
import RPi.GPIO as GPIO
import time

#ピン番号の設定
right_front = 25
left_front = 23
right_back = 8
left_back = 24

#各ピンについてすべてOUTPUTに設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(right_front, GPIO.OUT)
GPIO.setup(left_front, GPIO.OUT)
GPIO.setup(right_back, GPIO.OUT)
GPIO.setup(left_back, GPIO.OUT)

#前進用の関数の設定
def forward(time):
    GPIO.output(right_front, GPIO.HIGH)
    GPIO.output(left_front, GPIO.HIGH)
    time.sleep(time)

#後退用の関数の設定
def back(time):
    GPIO.output(right_back, GPIO.HIGH)
    GPIO.output(left_back, GPIO.HIGH)
    time.sleep(time)

#停止用関数の設定．運動を切り替えるときに使用
def stop():
    GPIO.output(right_front, GPIO.LOW)
    GPIO.output(left_front, GPIO.LOW)
    GPIO.output(right_back, GPIO.LOW)
    GPIO.output(left_back, GPIO.LOW)
    time.sleep(0.1)

#実際に動作するプログラムはこの中
#5秒前進，5秒後退を繰り返す．
while True:
    forward(5)
    stop()
    back(5)
    stop()