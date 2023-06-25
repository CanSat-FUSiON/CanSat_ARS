from Modules.motor import Motor
from Modules.longsleep import Longsleep
from Modules.step import Step
from Modules.camerarun import Camerarun
from Modules.logs import Logs
from Modules.stack import Stackrun
from Modules.stack import Gpsstack
from Modules.stack import Accstack
from Modules.communication import Communicator
from Modules.gpsrunner import Gpsrunner
from Modules.sensor import Sensor
from Modules.landingdetecter import Landingdetecter

from geopy.distance import geodesic
import os
import smbus
from itertools import count
import csv
from gps3 import gps3
from time import sleep
import RPi.GPIO as GPIO
import board
import adafruit_bno055
import math
from readline import set_completion_display_matches_hook
from socket import MSG_WAITALL
from tokenize import Double
from adafruit_extended_bus import ExtendedI2C as I2C
import Modules.runpattern as runpattern
import sys
sys.path.insert(4, '/home/pi/.local/lib/python3.7/site-packages')


# import LPS25HB
# import random
# import time
# import serial
# from multiprocessing.connection import wait
# import multiprocessing
# import datetime

# import picamera
# import picamera.array
# import cv2 as cv
# import numpy as np

runpattern.first()  # 起動時にモーターが回ってしまうことを防止


def main():
    try:
        runpattern.first()
        step = Step()  # Step(Class)のインスタンスを作成。あらゆるタイマーはこのインスタンスの値で条件分岐する。
        step.set_longsleep_steptime()  # longsleeptimeを現在時刻(起動時)に設定。
        gps_setting_socket = gps3.GPSDSocket()  # GPS情報をやり取りするインスタンスを作成。
        gps_setting_socket.connect()
        gps_setting_socket.watch()

        logs = Logs()  # Log(Class)のインスタンスを作成。あらゆるlogはこのインスタンスを通して書き込まれる。
        communication = Communicator(bus=smbus.SMBus(
            1), logclass=logs, gps_socket=gps_setting_socket, data_stream=gps3.DataStream())  # 通信をするためのCommunicator(Class)のインスタンスを作成。

        landingdetect = Landingdetecter(  # Landingdetecter(Class)のインスタンスを作成。
            time_limit=0, burn_time=10, hlist=[0, 1, 2, 3, 4])

        longsleep = Longsleep(file_name='sleeptime', encoding='UTF-8',  # Longsleep(Class)のインスタンスを作成。
                              fr_time=0, com_time=2400, ld_time=1200, pt_time=10)

        sensor = Sensor(i2c=I2C(1), sensor=adafruit_bno055.BNO055_I2C(I2C(1)), gps_socket=gps_setting_socket,  # Sensor(Class)のインスタンスを作成。
                        data_stream=gps3.DataStream(), lastval=0xFFFF, offset_mag_x=0, offset_mag_y=0, offset_mag_degree=0)
        gpsrunner = Gpsrunner(goal_lat=40.900522, goal_lon=-119.07909722,  # Gpsrunner(Class)のインスタンスを作成。
                              radius_Earth=6378137., THRESHOLD=15, distance_THR=1.2, pitch_time=1)
        accstack = Accstack(ygradlist=[0, 0, 0, 0, 0, 0],  # Accstack(Class)のインスタンスを作成。
                            startstack_THR=15, finishstack_THR=10, turnover_THR=-5, pitch_time=30, ygradoffset=6)
        gpsstack = Gpsstack(GPS_stack_radius=3, latlist=[200, 300, 400, 500], lonlist=[  # Gpsstack(Class)のインスタンスを作成。
                            200, 300, 400, 500], latrate=111015.4872, lonrate=89925.9685, pitch_time=60)
        stackrun = Stackrun()  # Stackrun(Class)のインスタンスを作成。
        camerarun = Camerarun(resolution=(512, 384), framerate=10,  # Camerarun(Class)のインスタンスを作成。
                              occ_THR_low=0.005, occ_THR_high=0.1, range_THR=200, pt_time=5)
        motor = Motor()  # Motor(Class)のインスタンスを作成。

        while True:
            if int(longsleep.cd_time) <= int(longsleep.com_time):  # com_timeをcd_timeが下回るときにbreakする。
                break
            runpattern.sign_on()  # LEDの操作。longsleep.pt_timeは LEDが点滅する時間*2 & 判定のループインターバル。
            sleep(longsleep.pt_time/2)
            runpattern.sign_off()
            sleep(longsleep.pt_time/2)

            # 1ループ後からlongsleep.pt_timeを超えたらカウントダウンが更新される。
            if step.evaluate_longsleep_steptime().seconds >= longsleep.pt_time:  # 1ループでpt_timeを超えるとcd_timeを更新する(ifは予防線)。
                longsleep.set()  # txtを通してtt_timeを更新する。
                longsleep.rewrite()  # txtの値を更新。
                print(longsleep.cd_time)
                step.set_longsleep_steptime()  # txtからスリープタイムの値を受け取る。

        communication.start()  # 通信開始。

        while True:
            if int(longsleep.cd_time) <= int(longsleep.ld_time):  # ld_timeをcd_timeが下回るときにbreakする。(ld_timeを0とするとわかりやすい)
                break
            if step.evaluate_longsleep_steptime().seconds >= longsleep.pt_time:
                longsleep.set()
                longsleep.rewrite()
                print(longsleep.cd_time)
                step.set_longsleep_steptime()

        step.set_landing_steptime()  # ここから着地判定を始める。

        while True:
            if int(longsleep.cd_time) <= -1:  # longsleepタイムを過ぎた場合は着地をスキップ。
                break
            else:
                if step.evaluate_landing_steptime().seconds + step.evaluate_landing_steptime().microseconds/1000000 > 0.5:  # 0.5秒ごとに判定を行う。
                    landingdetect.set()
                    landingdetect.detect()  # 着地を判定。着地したと判定すると landingdetect.detectsign = 1 を代入。
                    landingdetect.measureprint()
                    step.set_landing_steptime()
                if step.evaluate_longsleep_steptime().seconds >= longsleep.pt_time:
                    longsleep.set()
                    longsleep.rewrite()
                    print(longsleep.cd_time)
                    step.set_longsleep_steptime()
                if landingdetect.detectsign == 1 or longsleep.cd_time == 0:  # 着地判定をした、もしくはcd_timeが0になった場合、エンベロープ展開を行う。
                    landingdetect.warning()
                    landingdetect.nicrburn()
                    print("start burning")
                    sleep(5)
                    landingdetect.finish_run(runtime=5)
                    print("open")
                    runpattern.stop()
                    break

        longsleep.cd_time = -1  # 再起動したらburningの工程を無視して進む。
        longsleep.rewrite()

        while True:  # GPS走行と画像処理走行を繰り返すフェーズ。画像処理走行はゴールから離れすぎたときGPSのフェーズに戻る。
            step.set_gpsrun_steptime()  # それぞれの時間を初期化。各ループに入るための変数。
            step.set_gpsstack_steptime()
            step.set_accstack_steptime()

            while True:
                print("start GPSrun")
                sensor.set_gps()  # gps, 9軸, 加速度の値をそれぞれ取得。
                sensor.set_mag()
                sensor.set_acc()
                gpsrunner.set(sensor)  # センサーの値をgpsrunnerのインスタンスに入力。
                gpsrunner.gpsrun_print()
                if gpsrunner.distance_ntg <= gpsrunner.distance_THR:  # GPS走行で近距離まで近づけたか判断。
                    gpsrunner.gpsrunfinish()
                    break
                if step.evaluate_gpsrun_steptime().seconds >= gpsrunner.pitch_time:
                    gpsrunner.gpsrun(motor)
                    logs.con_log(gpsrunner.loglist)  # 位置などのログを作成。
                    step.set_gpsrun_steptime()  # ステップタイムを更新。
                if step.evaluate_accstack_steptime().seconds+step.evaluate_accstack_steptime().microseconds/1000000 >= accstack.pitch_time:
                    accstack.set(sensor)
                    print(accstack.ygradlist)
                    print(accstack.acc_z)
                    if accstack.acc_z <= accstack.turnover_THR:  # 加速度によるスタックの判定。
                        accstack.startprint()
                        runpattern.stack(pattern=4, runtime=1)  # 一度スタックを抜けるための走行を行う。
                        sensor.set_acc()
                        accstack.set(sensor)
                        accstack.nowprint()
                        sleep(1)
                        if accstack.acc_z <= accstack.turnover_THR:  # もう一度判定。
                            while True:
                                stackrun.set(pattern_range=[
                                    12, 19], runtime_range=[1, 10])  # ランダムなパターンで走行を行う。
                                stackrun.escaperun()
                                sensor.set_acc()
                                accstack.set(sensor)
                                accstack.nowprint()
                                sleep(1)
                                if accstack.acc_z >= accstack.turnover_THR:  # スタック状態を抜けたかどうか判定。
                                    break
                    step.set_accstack_steptime()  # ステップタイムを更新。
                if step.evaluate_gpsstack_steptime().seconds >= gpsstack.pitch_time:
                    gpsstack.set(sensor)  # GPSによるスタックの判定。
                    print(gpsstack.dif_abs_m)
                    print(gpsstack.latlist)
                    if gpsstack.dif_abs_m <= gpsstack.GPS_stack_radius:
                        gpsstack.startprint()
                        while True:
                            stackrun.set(pattern_range=[
                                         1, 19], runtime_range=[2, 6])  # ランダムなパターンで走行を行う。
                            stackrun.escaperun()
                            sensor.set_gps()
                            gpsstack.set_diflist(sensor)
                            gpsstack.nowprint()
                            sleep(1)
                            if min(gpsstack.diflist) > gpsstack.GPS_stack_radius:
                                gpsstack.finishprint()
                                gpsstack.set_latlist(  # 問題のない値に初期化。
                                    latlist=[200, 300, 400, 500])
                                gpsstack.set_lonlist(  # 問題のない値に初期化。
                                    lonlist=[200, 300, 400, 500])
                                break
                    step.set_gpsstack_steptime()  # ステップタイムを更新。
                sleep(0.5)

            step.set_imagesave_steptime()  # それぞれの時間を初期化。各ループに入るための変数。
            step.set_accstack_steptime()
            step.set_error_steptime()

            while True:
                camerarun.getdata()  # カメラからデータを取得。
                camerarun.run(motor)  # 画像処理走行を行う。
                logs.cam_log(camerarun.loglist)  # ログを残す。
                if step.evaluate_imagesave_steptime().seconds >= camerarun.pt_time:
                    camerarun.save()  # 画像を保存。
                    step.set_imagesave_steptime()  # ステップタイムを更新。
                if step.evaluate_accstack_steptime().seconds >= camerarun.pt_time:
                    sensor.set_acc()  # 加速度の値を取得。
                    accstack.set(sensor)
                    if accstack.acc_z <= accstack.turnover_THR:  # 加速度によるスタックの判定。(GPSと同様)
                        accstack.startprint()
                        runpattern.stack(pattern=4, runtime=1)
                        sensor.set_acc()
                        accstack.set(sensor)
                        accstack.nowprint()
                        sleep(1)
                        if accstack.acc_z <= accstack.turnover_THR:
                            while True:
                                stackrun.set(pattern_range=[
                                    12, 19], runtime_range=[1, 10])
                                stackrun.escaperun()
                                sensor.set_acc()
                                accstack.set(sensor)
                                accstack.nowprint()
                                sleep(1)
                                if accstack.acc_z >= accstack.turnover_THR:
                                    break
                    step.set_accstack_steptime()
                if step.evaluate_error_steptime().seconds > 60:
                    sensor.set_gps()  # gpsの値を取得。
                    gpsrunner.set(sensor)
                if camerarun.jd_sign == 2 or gpsrunner.distance_ntg > gpsrunner.distance_THR:  # 画像処理走行でゴールに達したか、ゴールから離れすぎた場合break。
                    break

            if camerarun.jd_sign == 2:  # ゴールに達したと判断した場合break。
                break

            else:  # ゴールから離れすぎた場合、GPS走行から開始。
                pass

        gps_setting_socket.close()

        while True:  # 終了。
            sleep(10)

    except KeyboardInterrupt:
        longsleep.cd_time = longsleep.fr_time
        longsleep.rewrite()


while True:
    try:
        main()
        break
    except KeyboardInterrupt:
        runpattern.stop()
        GPIO.cleanup()
    except:
        pass
