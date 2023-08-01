import datetime


class Logs:
    def __init__(self):  # 初期設定を行うメソッド。
        self.timezone = datetime.timezone(
            datetime.timedelta(hours=-7), name='US')
        self.flight_starttime = datetime.datetime.now(self.timezone)
        nm = str(str(self.flight_starttime.month)+'-'+str(self.flight_starttime.day)+'_' +
                 str(self.flight_starttime.hour)+':'+str(self.flight_starttime.minute)+':'+str(self.flight_starttime.second))
        self.connm = str('con_'+nm)  # file名を設定。ファイルが作られた時間がファイル名になっている。
        self.ffnm = str('ff_'+nm)
        self.camnm = str('cam_'+nm)

    def ff_log(self, loglist):  # はじめの状態からlogを出力するメソッド。ff は from flightの意味。通信と一緒に動くので、GPSのデータを常に残し続ける。「***」は任意のフォルダを選択する。
        f = open('/***/'+self.ffnm+'.csv', "a")
        f.write(str(datetime.datetime.now(self.timezone)))
        for log in loglist:
            f.write(',')
            f.write(str(log))
        f.write('\n')
        f.close

    def con_log(self, loglist):  # 制御履歴を残すメソッド。
        f = open('/***/'+self.connm+'.csv', "a")
        f.write(str(datetime.datetime.now(self.timezone)))
        for log in loglist:
            f.write(',')
            f.write(str(log))
        f.write("\n")
        f.close

    def cam_log(self, loglist):  # 画像処理走行の制御履歴を残すメソッド。
        f = open('/***/'+self.camnm+'.csv', "a")
        f.write(str(datetime.datetime.now(self.timezone)))
        for log in loglist:
            f.write(',')
            f.write(str(log))
        f.write('\n')
        f.close
