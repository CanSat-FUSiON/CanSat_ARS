import RPi.GPIO as GPIO
import time

left_front=23       #モータードライバの接続されてるピンに合わせて番号を変更してください
right_front=25
left_back=24
right_back=8

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(right_front,GPIO.OUT)
GPIO.setup(left_front,GPIO.OUT)
GPIO.setup(right_back,GPIO.OUT)
GPIO.setup(left_back,GPIO.OUT)

def stop(x):   #停止
    GPIO.output(right_front,GPIO.LOW)
    GPIO.output(left_front,GPIO.LOW)
    GPIO.output(right_back,GPIO.LOW)
    GPIO.output(right_back,GPIO.LOW)
    time.sleep(x)
    return()

def forward(x):   #前進
    GPIO.output(right_front,GPIO.HIGH)
    GPIO.output(left_front,GPIO.HIGH)
    GPIO.output(right_back,GPIO.LOW)
    GPIO.output(left_back,GPIO.LOW)
    time.sleep(x)
    return()

def back(x):       #後退
    GPIO.output(right_back,GPIO.HIGH)
    GPIO.output(left_back,GPIO.HIGH)
    GPIO.output(right_front,GPIO.LOW)
    GPIO.output(left_front,GPIO.LOW)
    time.sleep(x)
    return()

def leftturn(x):   #左旋回
    GPIO.output(right_front,GPIO.HIGH)
    GPIO.output(left_front,GPIO.LOW)
    GPIO.output(right_back,GPIO.LOW)
    GPIO.output(left_back,GPIO.HIGH)
    time.sleep(x) #路面状況などによって時間調整
    stop()
    return()

def rightturn(x):  #右旋回
    GPIO.output(right_front,GPIO.LOW)
    GPIO.output(left_front,GPIO.HIGH)
    GPIO.output(right_back,GPIO.HIGH)
    GPIO.output(left_back,GPIO.LOW)
    time.sleep(x) #路面状況などによって時間調整
    stop()
    return()

def reforward(x):  #後退後前進
    GPIO.output(right_back,GPIO.HIGH)
    GPIO.output(left_back,GPIO.HIGH)
    GPIO.output(right_front,GPIO.LOW)
    GPIO.output(left_front,GPIO.LOW)
    time.sleep(x)
    GPIO.output(right_front,GPIO.HIGH)
    GPIO.output(left_front,GPIO.HIGH)
    GPIO.output(right_back,GPIO.LOW)
    GPIO.output(left_back,GPIO.LOW)
    time.sleep(x)
    return()

def wave(x):     #前進後進を5回繰り返す
    for i in range(5):
        GPIO.output(right_back,GPIO.HIGH)
        GPIO.output(left_back,GPIO.HIGH)
        GPIO.output(right_front,GPIO.LOW)
        GPIO.output(left_front,GPIO.LOW)
        time.sleep(x)
        GPIO.output(right_front,GPIO.HIGH)
        GPIO.output(left_front,GPIO.HIGH)
        GPIO.output(right_back,GPIO.LOW)
        GPIO.output(left_back,GPIO.LOW)
        time.sleep(x)
        return()

def motortest(version, x):
    if version == '1':
        forward()
    elif version == '2':
        back()
    elif version == '3':
        leftturn(x)
    elif version == '4':
        rightturn(x)
    elif version == '5':
        stop(x)
    elif version == '6':
        reforward(x)
    elif version == '7':
        wave(x)