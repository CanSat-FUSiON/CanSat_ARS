import runpattern as motor


class Motor:  # 初期設定を行うメソッド。
    def __init__(self):
        self.lefttimes = 0
        self.righttimes = 0
        pass

    def left(self):  # 前進してから左に回る走行を行うメソッド。
        motor.forward(0.02*(self.lefttimes % 11))
        motor.leftturn(0.2-0.02*(self.lefttimes % 11))
        self.lefttimes = self.lefttimes + 1

    def right(self):  # 前進してから右に回る走行を行うメソッド。
        motor.forward(0.02*(self.lefttimes % 11))
        motor.rightturn(0.2-0.02*(self.lefttimes % 11))
        self.righttimes = self.righttimes + 1

    def forward_gps(self):  # 前進するメソッド。
        self.lefttimes = 0
        self.righttimes = 0
        motor.forward()

    def forward_cam(self):  # 後退するメソッド。
        self.lefttimes = 0
        self.righttimes = 0
        motor.forward(0.2)
