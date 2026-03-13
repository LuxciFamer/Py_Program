import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# 1. 读取CSV文件
def read_weather_data(Weather_Data):
    """读取天气数据CSV文件"""
    try:
        df = pd.read_csv(Weather_Data)
        print(f"成功读取文件，共{len(df)}行数据")
        return df
    except FileNotFoundError:
        print(f"错误：找不到文件 {Weather_Data}")
        return None
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None

# 2. 计算温度统计特征
def calculate_temperature_stats(df):
    """计算温度的统计特征"""
    if df is None or 'Temp_C' not in df.columns:
        print("错误：数据框为空或没有温度列")
        return None
    
    temp_data = df['Temp_C']
    
    stats = {
        'mean': np.mean(temp_data),
        'min': np.min(temp_data),
        'max': np.max(temp_data),
        'std': np.std(temp_data),
        'median': np.median(temp_data)
    }
    
    return stats

# 3. 绘制温度变化曲线
def plot_temperature_curves(df, output_image_path='temperature_plot.png'):
    """绘制温度变化曲线和7天滑动平均"""
    if df is None or 'Temp_C' not in df.columns or 'Date/Time' not in df.columns:
        print("错误：缺少必要的数据列")
        return
    
    # 转换日期时间列
    df['Date/Time'] = pd.to_datetime(df['Date/Time'])
    
    # 按日期排序
    df = df.sort_values('Date/Time')
    
    # 提取日期和温度
    dates = df['Date/Time']
    temperatures = df['Temp_C']
    
    # 计算7天滑动平均
    window_size = 7 * 24  # 7天 * 24小时/天
    rolling_avg = temperatures.rolling(window=window_size, min_periods=1).mean()
    
    # 创建图形
    plt.figure(figsize=(15, 8))
    
    # 绘制逐日温度（每小时数据）
    plt.plot(dates, temperatures, 'b-', alpha=0.5, linewidth=0.8, label='Hourly Temperature')
    
    # 绘制7天滑动平均
    plt.plot(dates, rolling_avg, 'r-', linewidth=2, label='7-Day Moving Average')
    
    # 设置图形属性
    plt.title('Temperature Variation with 7-Day Moving Average', fontsize=16, fontweight='bold')
    plt.xlabel('Date/Time', fontsize=12)
    plt.ylabel('Temperature (°C)', fontsize=12)
    plt.legend(loc='best', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # 自动调整x轴日期格式
    plt.gcf().autofmt_xdate()
    
    # 保存图形
    plt.tight_layout()
    plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
    print(f"温度变化曲线已保存为: {output_image_path}")
    
    # 显示图形
    plt.show()

# 4. 将结果保存到文件
def save_results_to_file(stats, output_file_path='temperature_results.txt'):
    """将统计结果保存到文本文件"""
    if stats is None:
        print("错误：没有统计结果可保存")
        return
    
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write("=" * 50 + "\n")
        f.write("TEMPERATURE STATISTICAL ANALYSIS RESULTS\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("Statistical Features of Temperature (°C):\n")
        f.write("-" * 40 + "\n")
        f.write(f"Mean Temperature:      {stats['mean']:.2f} °C\n")
        f.write(f"Minimum Temperature:   {stats['min']:.2f} °C\n")
        f.write(f"Maximum Temperature:   {stats['max']:.2f} °C\n")
        f.write(f"Standard Deviation:    {stats['std']:.2f} °C\n")
        f.write(f"Median Temperature:    {stats['median']:.2f} °C\n")
        
        f.write("\n" + "=" * 50 + "\n")
        f.write("Analysis completed on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        f.write("=" * 50 + "\n")
    
    print(f"统计结果已保存为: {output_file_path}")

# 主函数
def main():
    """主程序"""
    print("=" * 60)
    print("AI辅助编程实践 - 天气数据分析")
    print("=" * 60)
    
    # 文件路径
    csv_file = 'Weather_Data.csv'
    
    # 1. 读取数据
    print("\n1. 读取天气数据...")
    weather_df = read_weather_data(csv_file)
    
    if weather_df is None:
        return
    
    # 显示数据基本信息
    print(f"数据形状: {weather_df.shape}")
    print(f"数据列: {list(weather_df.columns)}")
    print(f"温度数据示例:\n{weather_df['Temp_C'].head()}")
    
    # 2. 计算统计特征
    print("\n2. 计算温度统计特征...")
    temperature_stats = calculate_temperature_stats(weather_df)
    
    if temperature_stats:
        print("\n温度统计特征:")
        print("-" * 40)
        print(f"均值:     {temperature_stats['mean']:.2f} °C")
        print(f"最小值:   {temperature_stats['min']:.2f} °C")
        print(f"最大值:   {temperature_stats['max']:.2f} °C")
        print(f"标准差:   {temperature_stats['std']:.2f} °C")
        print(f"中位数:   {temperature_stats['median']:.2f} °C")
    
    # 3. 绘制温度变化曲线
    print("\n3. 绘制温度变化曲线...")
    plot_temperature_curves(weather_df, 'temperature_variation.png')
    
    # 4. 保存结果到文件
    print("\n4. 保存结果到文件...")
    save_results_to_file(temperature_stats, 'temperature_analysis_results.txt')
    
    print("\n" + "=" * 60)
    print("程序执行完成！")
    print("=" * 60)

# 执行主程序
if __name__ == "__main__":
    main()
