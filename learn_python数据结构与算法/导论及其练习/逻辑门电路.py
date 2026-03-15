class LogicGate:
    """
    基础逻辑门类，表示一个逻辑门的基本结构。

    属性:
    - label: 门的名称或标签，用于在提示或调试时识别该门
    - output: 缓存门当前计算得到的输出（0 或 1），通过 `getOutput()` 计算并返回
    """

    def __init__(self, n):
        self.label = n
        self.output = None

    def getLabel(self):
        """返回门的标签/名称。"""
        return self.label

    def getOutput(self):
        """计算并返回当前门的输出。

        实现细节：调用子类实现的 `performGateLogic()` 方法得到逻辑结果，
        并将结果缓存到 `self.output` 中以便后续使用。
        """
        self.output = self.performGateLogic()
        return self.output


class BinaryGate(LogicGate):
    def __init__(self, n):
        super().__init__(n)
        self.pinA = None
        self.pinB = None

    def getPinA(self):
        # 如果该引脚未被连接（即为 None），则从用户输入读取整型值（0 或 1）
        if self.pinA is None:
            return int(input(f"Enter Pin A input for gate {self.getLabel()} --> "))
        else:
            # 否则，pinA 是一个 Connector，调用其来源门的输出
            return self.pinA.getFrom().getOutput()

    def getPinB(self):
        # 同上，对 B 引脚的处理
        if self.pinB is None:
            return int(input(f"Enter Pin B input for gate {self.getLabel()} --> "))
        else:
            return self.pinB.getFrom().getOutput()

    def setNextPin(self, source):
        """将来源 `source`（通常为 `Connector`）连接到该门的下一个可用引脚。

        连接顺序：优先填充 `pinA`，然后 `pinB`。如果都已满，则抛出异常。
        """
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
        # 单输入门：如果未连接则请求用户输入，否则获取连接来源的输出
        if self.pin is None:
            return int(input(f"Enter Pin input for gate {self.getLabel()} --> "))
        else:
            return self.pin.getFrom().getOutput()


# 基本逻辑门实现
class AndGate(BinaryGate):
    """与门：两个输入都为1时输出1，否则输出0"""
    def __init__(self, n):
        super().__init__(n)

    def performGateLogic(self):
        a = self.getPinA()
        b = self.getPinB()
        # 返回逻辑与的结果（1 或 0）
        return 1 if a == 1 and b == 1 else 0


class OrGate(BinaryGate):
    """或门：至少一个输入为1时输出1，否则输出0"""
    def __init__(self, n):
        super().__init__(n)

    def performGateLogic(self):
        a = self.getPinA()
        b = self.getPinB()
        # 返回逻辑或的结果（1 或 0）
        return 1 if a == 1 or b == 1 else 0


class NotGate(UnaryGate):
    """非门：输入为1时输出0，输入为0时输出1"""
    def __init__(self, n):
        super().__init__(n)

    def performGateLogic(self):
        a = self.getPin()
        # 非门：取反输入（0/1）
        return 1 if a == 0 else 0


# 复合逻辑门实现
class NandGate(BinaryGate):
    """与非门：与门的输出取反"""
    def __init__(self, n):
        super().__init__(n)

    def performGateLogic(self):
        a = self.getPinA()
        b = self.getPinB()
        # NAND = NOT(AND)
        # 如果 (a and b) 为真，则返回 0，否则返回 1
        return 0 if a == 1 and b == 1 else 1


class NorGate(BinaryGate):
    """或非门：或门的输出取反"""
    def __init__(self, n):
        super().__init__(n)

    def performGateLogic(self):
        a = self.getPinA()
        b = self.getPinB()
        # NOR = NOT(OR)
        # 两个输入都为0时返回1，否则返回0
        return 1 if a == 0 and b == 0 else 0


class XorGate(BinaryGate):
    """异或门：两个输入不同时输出1，相同时输出0"""
    def __init__(self, n):
        super().__init__(n)

    def performGateLogic(self):
        a = self.getPinA()
        b = self.getPinB()
        # XOR: (A AND NOT B) OR (NOT A AND B)
        # 简单实现：两个输入不同时为1
        return 1 if a != b else 0


class XnorGate(BinaryGate):
    """异或非门（同或门）：两个输入相同时输出1，不同时输出0"""
    def __init__(self, n):
        super().__init__(n)

    def performGateLogic(self):
        a = self.getPinA()
        b = self.getPinB()
        # XNOR = NOT(XOR)
        # 两个输入相同时返回1
        return 1 if a == b else 0


class Connector:
    def __init__(self, fgate, tgate):
        self.fromgate = fgate
        self.togate = tgate
        # 创建连接后，立即将当前 Connector 绑定到目标门的下一个可用引脚
        tgate.setNextPin(self)  # 现在 tgate (一个 BinaryGate/UnaryGate 扩展) 拥有 setNextPin 方法

    def getFrom(self):
        """返回连接的来源门对象（Connector 从哪里来的）。"""
        return self.fromgate

    def getTo(self):
        """返回连接的目标门对象（Connector 到哪里去）。"""
        return self.togate


# 示例：三输入与门（扩展示例）
class ThreeInputAndGate(LogicGate):
    """三输入与门：三个输入都为1时输出1，否则输出0"""
    def __init__(self, n):
        super().__init__(n)
        self.pinA = None
        self.pinB = None
        self.pinC = None

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

    def getPinC(self):
        if self.pinC is None:
            return int(input(f"Enter Pin C input for gate {self.getLabel()} --> "))
        else:
            return self.pinC.getFrom().getOutput()

    def setNextPin(self, source):
        """ 用于Connector连接时，设置本门的输入引脚。 """
        if self.pinA is None:
            self.pinA = source
        elif self.pinB is None:
            self.pinB = source
        elif self.pinC is None:
            self.pinC = source
        else:
            raise RuntimeError("Error: NO EMPTY PINS")

    def performGateLogic(self):
        a = self.getPinA()
        b = self.getPinB()
        c = self.getPinC()
        return 1 if a == 1 and b == 1 and c == 1 else 0


# 示例：多路选择器（MUX） - 更复杂的逻辑电路
class MuxGate(LogicGate):
    """2:1多路选择器：根据选择信号S选择输出A或B"""
    def __init__(self, n):
        super().__init__(n)
        self.pinA = None  # 输入A
        self.pinB = None  # 输入B
        self.pinS = None  # 选择信号

    def getPinA(self):
        if self.pinA is None:
            return int(input(f"Enter Pin A input for MUX {self.getLabel()} --> "))
        else:
            return self.pinA.getFrom().getOutput()

    def getPinB(self):
        if self.pinB is None:
            return int(input(f"Enter Pin B input for MUX {self.getLabel()} --> "))
        else:
            return self.pinB.getFrom().getOutput()

    def getPinS(self):
        if self.pinS is None:
            return int(input(f"Enter Select pin for MUX {self.getLabel()} --> "))
        else:
            return self.pinS.getFrom().getOutput()

    def setNextPin(self, source):
        """ 用于Connector连接时，设置本门的输入引脚。 """
        if self.pinA is None:
            self.pinA = source
        elif self.pinB is None:
            self.pinB = source
        elif self.pinS is None:
            self.pinS = source
        else:
            raise RuntimeError("Error: NO EMPTY PINS")

    def performGateLogic(self):
        a = self.getPinA()
        b = self.getPinB()
        s = self.getPinS()
        # MUX逻辑：如果S=0输出A，如果S=1输出B
        return a if s == 0 else b


# 测试函数
def test_circuit():
    """测试扩展的逻辑门电路"""
    print("=== 测试基本逻辑门 ===")
    
    # 测试与门
    g1 = AndGate("G1")
    print(f"与门 {g1.getLabel()} 测试: 输入1,1 -> 输出 {g1.getOutput()}")
    
    # 测试或门
    g2 = OrGate("G2")
    print(f"或门 {g2.getLabel()} 测试: 输入0,1 -> 输出 {g2.getOutput()}")
    
    # 测试非门
    g3 = NotGate("G3")
    print(f"非门 {g3.getLabel()} 测试: 输入1 -> 输出 {g3.getOutput()}")
    
    # 测试与非门
    g4 = NandGate("G4")
    print(f"与非门 {g4.getLabel()} 测试: 输入1,1 -> 输出 {g4.getOutput()}")
    
    # 测试或非门
    g5 = NorGate("G5")
    print(f"或非门 {g5.getLabel()} 测试: 输入0,0 -> 输出 {g5.getOutput()}")
    
    # 测试异或门
    g6 = XorGate("G6")
    print(f"异或门 {g6.getLabel()} 测试: 输入1,0 -> 输出 {g6.getOutput()}")
    
    # 测试异或非门
    g7 = XnorGate("G7")
    print(f"异或非门 {g7.getLabel()} 测试: 输入1,1 -> 输出 {g7.getOutput()}")
    
    print("\n=== 测试电路连接 ===")
    # 创建一个简单的组合电路：NOT(NAND(A, B))
    nand1 = NandGate("NAND1")
    not1 = NotGate("NOT1")
    
    # 连接NAND的输出到NOT的输入
    c1 = Connector(nand1, not1)
    
    print("电路: NOT(NAND(A, B))")
    print(f"当A=1, B=1时，NAND输出0，NOT输出1")
    
    # 测试三输入与门
    print("\n=== 测试三输入与门 ===")
    g8 = ThreeInputAndGate("G8")
    print(f"三输入与门 {g8.getLabel()} 测试: 输入1,1,1 -> 输出 {g8.getOutput()}")


if __name__ == "__main__":
    test_circuit()



