class LogicGate:

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
        return int(input("Enter Pin A input for gate" +
                             self.getLabel() + "-->"))

    def getPinB(self):
            return int(input("Enter Pin B input for gate" +
                             self.getLabel() + "-->"))

class UnaryGate(LogicGate):

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

    def __init__(self,fgate,tgate):
        self.fromgate = fgate
        self.togate = tgate

        tgete.setNextPin(self)

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

