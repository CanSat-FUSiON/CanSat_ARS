import RPi.GPIO as GPIO
import time
import motor as m

versionlist = []
timelist = []

GPIO.setmode(GPIO.BCM)
GPIO.setup(m.right_front, GPIO.OUT)
GPIO.setup(m.left_front, GPIO.OUT)
GPIO.setup(m.right_back, GPIO.OUT)
GPIO.setup(m.left_back, GPIO.OUT)

print("##########################################################################\n")
print("motor_testへようこそ!\n")
print("ここはモーターが正常に稼働しているのか、何秒回転するとどれくらい回転するのか、")
print("どのように制御するとどう進んでいくのか、などを確認するためのプログラムです!")
print("##########################################################################\n\n")

time.sleep(3)
print("#########################################################\n")
print("***セット数について・・・***\n")
print("セット数とは連続で動かしたいモーターの挙動の数を言います")
print("セット数には停止という挙動も一つのセットと考えます\n")
print("例）前進5秒→後退5秒→停止2秒→右回転1秒")
print("=セット数:4\n")
print("入力は自然数でお願いします。\n")
print("#########################################################\n")


time.sleep(1)


while True:
    number_in = input("セット数を教えてください。 :")
    try:
        number_out = int(number_in)
        if number_out == 0:
            print("数字を入力し直してください。")
        else:
            break
    except:
        print("数字を入力し直してください。")
        time.sleep(1)


print("ご入力ありがとうございます。現在処理中です・・・")
time.sleep(3)
print("処理が完了しました。\n\n")
time.sleep(2)

print("################################################################################################\n")
print("***version, time値について・・・***\n")
print("これから各挙動ごとにversion, time値の入力を行います")
print("これらの値はそれぞれの挙動におけるパラメーターです")
print("入力完了後、10秒間のスタンバイの末、走行を開始します\n")
print("versionは挙動の種類を設定します。1~5の値を入力してください。\n")
print("version:1 停止")
print("version:2 前進")
print("version:3 後退")
print("version:4 左旋回")
print("version:5 右旋回")
print("version:6 後進後前進")
print("version:7 前進後進を5回繰り返す")
print("time値は各挙動における継続時間(s)を設定します。正の値を入力してください。\n")
print("################################################################################################\n")

time.sleep(3)


for i in range(1, number_out+1):
    while True:
        v = input(str(i) + "回目のversionを入力してください。:")
        try:
            V = str(v)
            if V == '1' or V == '2' or V == '3' or V == '4' or V == '5' or V == '6' or V == '7':
                break
            else:
                print("もう一度、入力してください。")
                time.sleep(1)
        except:
            print("もう一度、入力してください。")
            time.sleep(1)

    versionlist.append(V)

    while True:
        t = input(str(i) + "回目のtime値を入力してください。:")
        try:
            T = float(t)
            if T < 0:
                print("もう一度、入力してください。")
                time.sleep(1)
            else:
                break
        except:
            print("もう一度、入力してください。")
            time.sleep(1)

    timelist.append(T)


print("ご入力ありがとうございます。現在処理中です・・・")
time.sleep(3)
print("処理が完了しました!\n")

print("\n")
print("それではこれより走行を開始します。\n")
print("3秒後、走行を開始します。\n")
time.sleep(0.5)
print("3")
time.sleep(1)
print("2")
time.sleep(1)
print("1")
time.sleep(1)
print("start!")


for r in range(0, number_out):
    m.motortest(versionlist[r], timelist[r])


print("走行終了です。お疲れさまでした。")
