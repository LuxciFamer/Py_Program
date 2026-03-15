class LogicGate:
    """逻辑门基类"""

    def __init__(self, name):
        self.name = name
        self.output = None

    def get_name(self):
        return self.name

    def get_output(self):
        return self.output


class BinaryGate(LogicGate):
    """二输入逻辑门基类"""

    def __init__(self, name, input_a=None, input_b=None):
        super().__init__(name)
        self.input_a = input_a
        self.input_b = input_b

    def set_inputs(self, a, b):
        self.input_a = a
        self.input_b = b


class AndGate(BinaryGate):
    """与门"""

    def __init__(self, name, input_a=None, input_b=None):
        super().__init__(name, input_a, input_b)

    def get_output(self):
        if self.input_a is not None and self.input_b is not None:
            # 与逻辑：仅当两个输入都为1时输出1
            self.output = 1 if (self.input_a == 1 and self.input_b == 1) else 0
        return self.output


class XorGate(BinaryGate):
    """异或门"""

    def __init__(self, name, input_a=None, input_b=None):
        super().__init__(name, input_a, input_b)

    def get_output(self):
        if self.input_a is not None and self.input_b is not None:
            # 异或逻辑：当两个输入不同时输出1
            self.output = 1 if (self.input_a != self.input_b) else 0
        return self.output


class HalfAdder:
    """半加器类"""

    def __init__(self, name, input_a=None, input_b=None):
        self.name = name
        self.input_a = input_a
        self.input_b = input_b
        self.sum_output = None
        self.carry_output = None

    def set_inputs(self, a, b):
        self.input_a = a
        self.input_b = b

    def compute(self):
        """执行半加器计算"""
        if self.input_a is not None and self.input_b is not None:
            # 创建异或门计算和位
            xor_gate = XorGate(f"{self.name}_xor", self.input_a, self.input_b)
            self.sum_output = xor_gate.get_output()

            # 创建与门计算进位位
            and_gate = AndGate(f"{self.name}_and", self.input_a, self.input_b)
            self.carry_output = and_gate.get_output()

        return self.carry_output, self.sum_output

    def get_outputs(self):
        return self.carry_output, self.sum_output


# 测试面向对象实现
print("面向对象半加器测试：")
ha = HalfAdder("ha1")
ha.set_inputs(1, 1)
carry, sum_bit = ha.compute()
print(f"输入：A=1, B=1 -> 和位={sum_bit}, 进位={carry}")

# 批量测试
print("\n完整真值表验证：")
for a, b in [(0, 0), (0, 1), (1, 0), (1, 1)]:
    ha.set_inputs(a, b)
    c, s = ha.compute()
    print(f"A={a}, B={b} -> S={s}, C={c}")


def half_adder(a, b):
    """
    半加器函数
    参数：
        a, b: 两个输入位（0或1）
    返回：
        (和位, 进位)
    """
    sum_bit = a ^ b  # 异或运算得到和位
    carry = a & b    # 与运算得到进位
    return sum_bit, carry


def full_adder(bit_a, bit_b, carry_in):
    """
    全加器实现（基于半加器）
    参数：
        bit_a, bit_b: 当前位的两个加数
        carry_in: 来自低位的进位
    返回：
        (进位输出, 和位)
    """
    # 第一个半加器：计算bit_a和bit_b的部分和
    sum1, carry1 = half_adder(bit_a, bit_b)

    # 第二个半加器：将部分和与进位输入相加
    final_sum, carry2 = half_adder(sum1, carry_in)

    # 最终进位：carry1或carry2（两者不会同时为1）
    final_carry = carry1 or carry2

    return final_carry, final_sum


# 测试全加器
print("\n全加器测试（1 + 1 + 进位1）：")
carry_out, sum_out = full_adder(1, 1, 1)
print(f"结果：和位={sum_out}, 进位={carry_out}")  # 输出：和位=1, 进位=1（即1+1+1=11，二进制3）


def binary_adder(bin_a, bin_b, n_bits=8):
    """
    多位二进制加法器
    参数：
        bin_a, bin_b: 二进制字符串（如"1101"）
        n_bits: 位数
    返回：
        相加结果的二进制字符串
    """
    # 确保输入位数一致
    a = bin_a.zfill(n_bits)
    b = bin_b.zfill(n_bits)

    carry = 0
    result_bits = []

    # 从最低位（最右侧）开始逐位相加
    for i in range(n_bits - 1, -1, -1):
        bit_a = int(a[i])
        bit_b = int(b[i])

        carry, sum_bit = full_adder(bit_a, bit_b, carry)
        result_bits.append(str(sum_bit))

    # 如果最后有进位，添加到结果最高位
    if carry:
        result_bits.append('1')

    # 反转结果（因为我们是从低位开始计算的）
    result = ''.join(result_bits[::-1])

    return result


# 测试8位加法器
print("\n8位二进制加法器测试：")
num1 = "11011010"  # 十进制218
num2 = "01100101"  # 十进制101
result = binary_adder(num1, num2, 8)
print(f"{num1} + {num2} = {result}")
print(f"验证：{int(num1, 2)} + {int(num2, 2)} = {int(result, 2)}")
