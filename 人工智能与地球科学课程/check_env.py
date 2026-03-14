"""Python 数据分析与机器学习环境验证脚本。

此脚本用于检查常用数据分析与机器学习库的安装状态与版本，帮助快速确认开发环境是否具备基本条件。
功能：
- 检查 Python 版本
- 检查一组常用库是否已安装并尝试获取版本号

备注：脚本尽量使用轻量的检测方法，不会自动安装任何包，仅给出安装建议。
"""

import sys
import importlib.util
import warnings

# 忽略非致命的警告信息，防止输出过多噪声
warnings.filterwarnings('ignore')

# 定义需要检查的库列表（这里使用包名/导入名）
REQUIRED_LIBRARIES = [
    'numpy',
    'pandas',
    'matplotlib',
    'sklearn',  # scikit-learn 的导入名为 sklearn
    'torch',
    'jupyter',
    'openai',
    'requests'
]

# 显示名称映射（用于输出更友好的名称）
LIB_DISPLAY_NAMES = {
    'sklearn': 'scikit-learn'
}


def check_python_version():
    """检查运行时 Python 版本是否满足最低要求。

    返回 True 表示通过，False 表示需要升级 Python。
    """
    required_version = (3, 6)  # 最低要求 Python 3.6
    current_version = sys.version_info

    print("=" * 50)
    print("步骤 1: 检查 Python 版本")
    print("-" * 30)

    # 比较元组 (major, minor)
    if current_version < required_version:
        print(f"\033[91m[失败] 当前 Python 版本是 {current_version.major}.{current_version.minor}.{current_version.micro}")
        print(f"       需要 Python >= {required_version[0]}.{required_version[1]}\033[0m")
        return False
    else:
        print(f"\033[92m[通过] Python 版本符合要求: {current_version.major}.{current_version.minor}.{current_version.micro}\033[0m")
        return True


def check_library_installation(lib_name):
    """检查单个库是否可导入，并尽量获取其版本信息。

    步骤：
    1. 使用 importlib.util.find_spec 快速判断模块是否存在（不实际导入）。
    2. 如果存在，尝试导入模块并读取常见的 __version__ 属性。
    3. 对于特殊包（如 torch、jupyter），尝试使用特定方式获取版本。

    返回: (installed: bool, display_name: str, version: str|None)
    """
    display_name = LIB_DISPLAY_NAMES.get(lib_name, lib_name)

    # 先用 find_spec 检查模块规范，效率较高且不会触发模块顶层代码
    spec = importlib.util.find_spec(lib_name)
    if spec is None:
        # 有些包可能存在别名或元包情况，这里保留针对性的处理逻辑
        if lib_name == 'sklearn':
            spec = importlib.util.find_spec('sklearn')
        if spec is None:
            return False, display_name, None

    # 如果找到了 spec，再尝试导入以读取版本信息。导入可能触发模块初始化代码。
    try:
        module = __import__(lib_name)
        # 大多数 Python 包会在 module.__version__ 中定义版本号
        version = getattr(module, '__version__', None)

        # 针对少数包的特殊处理
        if version is None:
            if lib_name == 'torch':
                # torch 使用 torch.__version__
                version = getattr(module, '__version__', None)
            elif lib_name == 'jupyter':
                # jupyter 是一个元包，版本信息可能在子组件中
                version = getattr(module, 'version', '版本信息不可用')

        return True, display_name, version
    except Exception:
        # 导入失败通常意味着包不可用或导入时出现错误，视为未安装
        return False, display_name, None


def main():
    """主函数：按步骤执行环境检测并打印结果摘要。"""
    print("\n\033[94m开始进行 Python 数据分析与机器学习环境验证...\033[0m")
    print("目标库: numpy, pandas, matplotlib, scikit-learn, torch, jupyter, openai, requests")

    # 1. 检查 Python 版本
    if not check_python_version():
        print("\n\033[91mPython 版本不符合要求，请先升级 Python 环境。\033[0m")
        return

    # 2. 逐个检查必需库
    print(f"\n{'='*50}")
    print("步骤 2: 检查必要的依赖库")
    print("-" * 30)

    results = []
    all_passed = True

    for lib in REQUIRED_LIBRARIES:
        installed, display_name, version = check_library_installation(lib)
        results.append((installed, display_name, version))

        if installed:
            # 如果没有获取到版本信息，展示为“未知”以提示用户
            print(f"\033[92m[✓] {display_name:15} 已安装 (版本: {version if version else '未知'})\033[0m")
        else:
            print(f"\033[91m[✗] {display_name:15} 未安装\033[0m")
            all_passed = False

    # 3. 输出总结报告与安装建议
    print(f"\n{'='*50}")
    print("环境验证总结")
    print("-" * 30)

    if all_passed:
        print("\033[92m✅ 恭喜！所有必需的库均已正确安装。\033[0m")
        print("   您可以开始进行数据分析和机器学习项目了。")

        # 提供一个简单且正确的快速验证示例，便于用户复制运行
        print(f"\n{'='*50}")
        print("快速验证示例（可复制到 Python 中运行）：")
        print("-" * 30)
        print("""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
import torch
import requests

print(f"NumPy 版本: {np.__version__}")
print(f"Pandas 版本: {pd.__version__}")
print(f"PyTorch 是否可用 GPU: {torch.cuda.is_available()}")
print("基础环境验证通过！")
""")
    else:
        print("\033[91m⚠️  部分库未安装。\033[0m")
        print("未安装的库:")
        for installed, display_name, _ in results:
            if not installed:
                print(f"  - {display_name}")

        print(f"\n安装建议:")
        print("1. 使用 pip 安装缺失的库（在终端中运行）:")
        print("   pip install numpy pandas matplotlib scikit-learn torch jupyter openai requests")
        print("2. 如果使用虚拟环境，请确保已激活环境")
        print("3. 对于 PyTorch，如需特定 CUDA 版本，请参考官方安装命令")

    print(f"\n{'='*50}")
    print("验证完成。")


if __name__ == "__main__":
    main()
