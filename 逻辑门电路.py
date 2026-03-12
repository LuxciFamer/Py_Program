class LogicGate:
    """
    基础逻辑门类，表示一个逻辑门的基本结构。
    """

    def __init__(self,n):
        self.label = n
        self.output = None

    def getLabel(self):
        return self.label

    def getOutput(self):
        self.output = self.performGateLogic()
        return self.output

class BinaryGate(LogicGate):
    def __init__(self, n):
        super().__init__(n)
        self.pinA = None
        self.pinB = None

    def getPinA(self):
        if self.pinA is None:
            return int(input(f"Enter Pin A input for gate {self.getLabel()} --> "))
        else:
            return self.pinA.getFrom().getOutput()

    def getPinB(self):
        if self.pinB is None:
            return int(input(f"Enter Pin B input for gate {self.getLabel()} --> "))
        else:
            return self.pinB.getFrom().getOutput()

    def setNextPin(self, source):
        """ 用于Connector连接时，设置本门的输入引脚。 """
        if self.pinA is None:
            self.pinA = source
        elif self.pinB is None:
            self.pinB = source
        else:
            raise RuntimeError("Error: NO EMPTY PINS")

class UnaryGate(LogicGate):
    def __init__(self, n):
        super().__init__(n)
        self.pin = None

    def getPin(self):
        if self.pin is None:
            return int(input(f"Enter Pin input for gate {self.getLabel()} --> "))
        else:
            return self.pin.getFrom().getOutput()

class AndGate(BinaryGate): # 正确继承自 BinaryGate
    def __init__(self, n):
        super().__init__(n)

    def performGateLogic(self):
        a = self.getPinA()
        b = self.getPinB()
        if a == 1 and b == 1:
            return 1
        else:
            return 0

class Connector:
    def __init__(self, fgate, tgate):
        self.fromgate = fgate
        self.togate = tgate
        tgate.setNextPin(self) # 现在 tgate (一个BinaryGate) 拥有 setNextPin 方法

    def getFrom(self):
        return self.fromgate
    def getTo(self):
        return self.togate


