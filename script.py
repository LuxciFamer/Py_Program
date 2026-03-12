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

    def __init__(self,n):
        super().__init__(n)

        self.pinA = None
        self.pinB = None

    def getPinA(self):
        if self.pinA == None:
            return input("Enter Pin A input for gate" +
                         self.getName() + "-->")
        else:
            return self.pinA.getFrom().getOutput()

    def getPinB(self):
        if self.pinB == None:
            return input("Enter Pin B input for gate" +
                         self.getName() + "-->")
        else:
            return self.pinB.getFrom().getOutput()

class UnaryGate(LogicGate):
    """
    一元逻辑门类，继承自LogicGate，用于处理一个输入的逻辑门。
    """

    def __init__(self,n):
        super().__init__(n)

        self.pin = None

        def getPin(self):
            return int(input("Enter Pin input for gate" +
                                 self.getLabel() + "-->"))

class AndGate(LogicGate):

    def __init__(self,n):
        super().__init__(n)

    def performGateLogic(self):

        a = self.getPinA()
        b = self.getPinB()
        if a==1 and b==1:
            return 1
        else:
            return 0

class Connector:
    """
    连接器类，用于连接逻辑门之间的输入和输出。
    """

    def __init__(self,fgate,tgate):
        self.fromgate = fgate
        self.togate = tgate

        tgate.setNextPin(self)

    def getFrom(self):
        return self.fromgate

    def getTo(self):
        return self.togate

    def setNextPin(self,source):
        if self.pinA == None:
            self.pinA = source
        else:
            if self.pinB ==None:
                self.pinB = source
            else:
                raise RuntimeError("Error: NO EMPTY PINS")

