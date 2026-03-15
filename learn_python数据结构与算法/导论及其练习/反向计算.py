class LogicGate:
    def __init__(self, n):
        self.label = n
        self.output = None
        self.downstream_gates = []  # 新增：存储下游门列表

    def add_downstream(self, gate):
        """添加一个下游门到列表中"""
        if gate not in self.downstream_gates:
            self.downstream_gates.append(gate)

    def getOutput(self):
        # 在正向计算中，此方法可能仅返回当前缓存值，或完全被新方法取代
        return self.output

    def propagate(self):
        """将本门输出值的变化传播给所有下游门"""
        for gate in self.downstream_gates:
            gate.input_changed(self, self.output)

class Connector:
    def __init__(self, fgate, tgate, pin_name):
        self.fromgate = fgate
        self.togate = tgate
        self.pin_name = pin_name
        tgate.connected_gates[pin_name] = fgate
        fgate.add_downstream(tgate)


class BinaryGate(LogicGate):
    def __init__(self, n):
        super().__init__(n)
        self.pinA = None
        self.pinB = None
        self.connected_gates = {'A': None, 'B': None}

    def set_pin(self, pin_name, value, from_gate=None):
        """设置引脚值，并触发重新计算"""
        if pin_name == 'A':
            self.pinA = value
        elif pin_name == 'B':
            self.pinB = value

        # 如果两个引脚都有值了，就计算输出
        if self.pinA is not None and self.pinB is not None:
            old_output = self.output
            self.output = self.performGateLogic()  # 调用具体逻辑计算
            # 如果输出发生了变化，通知所有下游门
            if self.output != old_output:
                self.propagate()

    # 下游门被通知输入变化的方法
    def input_changed(self, from_gate, new_value):
        """被上游门调用，更新对应引脚值并重新计算"""
        for pin, g in self.connected_gates.items():
            if g == from_gate:
                self.set_pin(pin, new_value, from_gate)
                break

class AndGate(BinaryGate):
    def performGateLogic(self):
        # 现在pinA和pinB已在set_pin中确保非None
        if self.pinA == 1 and self.pinB == 1:
            return 1
        else:
            return 0

class InputGate(LogicGate):
    def __init__(self, n):
        super().__init__(n)
        self.value = None

    def set_value(self, value):
        """用户调用此方法设置输入值，触发正向传播"""
        self.value = value
        self.output = value
        self.propagate()  # 立即通知下游门

# 测试代码：检测AND门电路
print("测试AND门电路：")

# 创建输入门
inputA = InputGate("InputA")
inputB = InputGate("InputB")

# 创建AND门
andGate = AndGate("AND")

# 连接输入到AND门
Connector(inputA, andGate, 'A')
Connector(inputB, andGate, 'B')

# 测试所有输入组合
test_cases = [(0, 0), (0, 1), (1, 0), (1, 1)]
expected_outputs = [0, 0, 0, 1]

for i, (a, b) in enumerate(test_cases):
    print(f"\n测试输入：A={a}, B={b}")
    inputA.set_value(a)
    inputB.set_value(b)
    output = andGate.getOutput()
    expected = expected_outputs[i]
    print(f"输出：{output} (期望：{expected})")
    if output == expected:
        print("✓ 通过")
    else:
        print("✗ 失败")

print("\n测试完成。")
