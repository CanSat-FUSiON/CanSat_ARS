import runpattern as motor


class Motor:
    def __init__(self):
        self.lefttimes = 0
        self.righttimes = 0
        pass

    def left(self):
        motor.forward(0.02*(self.lefttimes % 11))
        motor.leftturn(0.2-0.02*(self.lefttimes % 11))
        self.lefttimes = self.lefttimes + 1

    def right(self):
        motor.forward(0.02*(self.lefttimes % 11))
        motor.rightturn(0.2-0.02*(self.lefttimes % 11))
        self.righttimes = self.righttimes + 1

    def forward_gps(self):
        self.lefttimes = 0
        self.righttimes = 0
        motor.forward()

    def forward_cam(self):
        self.lefttimes = 0
        self.righttimes = 0
        motor.forward(0.2)
