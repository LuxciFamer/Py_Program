"""
Python 数据分析与机器学习环境验证脚本
用于检查 numpy, pandas, matplotlib, scikit-learn, torch, jupyter, openai, requests 库的安装状态。
"""

import sys
import importlib.util
import subprocess
import warnings
warnings.filterwarnings('ignore')  # 可选：忽略部分警告信息

# 定义需要检查的库列表
REQUIRED_LIBRARIES = [
    'numpy',
    'pandas',
    'matplotlib',
    'sklearn',  # scikit-learn的包名
    'torch',
    'jupyter',
    'openai',
    'requests'
]

# 库名与导入名/显示名的映射（部分库的包名与导入名不同）
LIB_DISPLAY_NAMES = {
    'sklearn': 'scikit-learn'
}

def check_python_version():
    """检查Python版本，确保为3.x[6](@ref)"""
    required_version = (3, 6)  # 设定最低要求版本
    current_version = sys.version_info
    print("=" * 50)
    print("步骤 1: 检查 Python 版本")
    print("-" * 30)
    if current_version < required_version:
        print(f"\033[91m[失败] 当前 Python 版本是 {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        print(f"       需要 Python >= {required_version[0]}.{required_version[1]}\033[0m")
        return False
    else:
        print(f"\033[92m[通过] Python 版本符合要求: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}\033[0m")
        return True

def check_library_installation(lib_name):
    """
    检查单个库是否安装，并尝试获取其版本号[7](@ref)[8](@ref)
    方法：使用 importlib.util.find_spec 检查模块是否存在，然后尝试导入获取版本
    """
    display_name = LIB_DISPLAY_NAMES.get(lib_name, lib_name)
    
    # 方法1: 检查模块规范是否存在[7](@ref)[8](@ref)
    spec = importlib.util.find_spec(lib_name)
    if spec is None:
        # 对于scikit-learn，尝试其完整名称
        if lib_name == 'sklearn':
            spec = importlib.util.find_spec('sklearn')
        return False, display_name, None
    
    # 方法2: 尝试导入并获取版本信息
    try:
        module = __import__(lib_name)
        # 获取版本号的通用方法
        version = getattr(module, '__version__', None)
        if version is None:
            # 对于某些库，可能有不同的版本属性
            if lib_name == 'torch':
                version = torch.__version__
            elif lib_name == 'jupyter':
                # jupyter 是一个元包，检查其核心组件
                version = getattr(module, 'version', '版本信息不可用')
        return True, display_name, version
    except Exception as e:
        # 如果导入失败，则视为未安装
        return False, display_name, None

def main():
    """主函数，执行环境检查流程[6](@ref)"""
    print("\n\033[94m开始进行 Python 数据分析与机器学习环境验证...\033[0m")
    print("目标库: numpy, pandas, matplotlib, scikit-learn, torch, jupyter, openai, requests")
    
    # 1. 检查Python版本
    if not check_python_version():
        print("\n\033[91mPython 版本不符合要求，请先升级 Python 环境。\033[0m")
        return
    
    # 2. 检查各个库的安装状态
    print(f"\n{'='*50}")
    print("步骤 2: 检查必要的依赖库[6](@ref)")
    print("-" * 30)
    
    results = []
    all_passed = True
    
    for lib in REQUIRED_LIBRARIES:
        installed, display_name, version = check_library_installation(lib)
        results.append((installed, display_name, version))
        
        if installed:
            print(f"\033[92m[✓] {display_name:15} 已安装 (版本: {version if version else '未知'})\033[0m")
        else:
            print(f"\033[91m[✗] {display_name:15} 未安装\033[0m")
            all_passed = False
    
    # 3. 输出总结报告
    print(f"\n{'='*50}")
    print("环境验证总结")
    print("-" * 30)
    
    if all_passed:
        print("\033[92m✅ 恭喜！所有必需的库均已正确安装。\033[0m")
        print("   您可以开始进行数据分析和机器学习项目了。")
        
        # 提供快速验证示例（可选）
        print(f"\n{'='*50}")
        print("快速验证示例（可复制到Python中运行）：")
        print("-" * 30)
        print("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
import torch
import requests

print(f"NumPy数组示例: {np.array([1](@ref)[2](@ref)[3](@ref)}")
print(f"Pandas版本: {pd.__version__}")
print(f"PyTorch是否可用GPU: {torch.cuda.is_available()}")
print("基础环境验证通过！")""")
    else:
        print("\033[91m⚠️  部分库未安装。\033[0m")
        print("未安装的库:")
        for installed, display_name, _ in results:
            if not installed:
                print(f"  - {display_name}")
        
        print(f"\n安装建议:")
        print("1. 使用 pip 安装缺失的库（在终端中运行）[1](@ref)[4](@ref)[5](@ref):")
        print("   pip install numpy pandas matplotlib scikit-learn torch jupyter openai requests")
        print("2. 如果使用虚拟环境，请确保已激活环境[1](@ref)[2](@ref)[3](@ref)")
        print("3. 对于PyTorch，如需特定CUDA版本，请参考官方安装命令[2](@ref)[4](@ref)")
    
    print(f"\n{'='*50}")
    print("验证完成。")

if __name__ == "__main__":
    main()
