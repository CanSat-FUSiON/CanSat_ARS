import datetime
import time


class Longsleep:

    def __init__(self, file_name, encoding, fr_time, com_time, ld_time, pt_time):  # 初期設定を行うメソッド。
        self.file_name = file_name
        self.encoding = encoding
        self.fr_time = fr_time  # first time
        self.com_time = com_time
        self.ld_time = ld_time  # landing detect time
        self.pt_time = pt_time  # pitch time
        self.tt_time = self.read()  # this time
        self.cu_time = 0  # count up time
        self.cd_time = self.tt_time  # count down time
        self.looptimes = 0

    def set(self):  # longsleepに必要の値を設定するメソッド。
        self.looptimes = self.looptimes + 1
        self.cu_time = int(self.pt_time)*int(self.looptimes)
        self.cd_time = int(self.tt_time) - int(self.cu_time)  # あとどれくらいで通信を始めるのかの秒数が代入される。

    def read(self):  # ファイルからスリープ時間を取得し返すメソッド。
        f = open(self.file_name+'.txt', 'r', encoding=self.encoding)  # ログから値を取ってくる。
        sleeptime = f.read()
        f.close()
        return sleeptime

    def rewrite(self):  # ファイルにスリープ時間を入力するメソッド。
        f = open(self.file_name+'.txt', 'w')
        f.write(str(self.cd_time))
        f.close()
