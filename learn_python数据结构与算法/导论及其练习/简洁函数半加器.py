def half_adder(bit_a, bit_b):
    """
    半加器函数实现
    参数：
        bit_a (int): 第一个二进制位（0或1）
        bit_b (int): 第二个二进制位（0或1）
    返回：
        tuple: (进位位, 和位)
    """
    # 和位 = A XOR B（异或运算）
    sum_bit = bit_a ^ bit_b
    # 进位位 = A AND B（与运算）
    carry_bit = bit_a & bit_b

    return carry_bit, sum_bit


# 测试半加器功能
print("半加器真值表测试：")
print("A | B | C | S")
print("--|---|---|--")

# 遍历所有可能的输入组合
test_inputs = [(0, 0), (0, 1), (1, 0), (1, 1)]
for a, b in test_inputs:
    carry, sum_bit = half_adder(a, b)
    print(f"{a} | {b} | {carry} | {sum_bit}")

# 具体示例
print("\n具体计算示例：")
print(f"1 + 1 = {half_adder(1, 1)[1]} (进位：{half_adder(1, 1)[0]})")
print(f"0 + 1 = {half_adder(0, 1)[1]} (进位：{half_adder(0, 1)[0]})")

