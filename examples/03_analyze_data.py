"""
示例3: 数据分析

演示如何加载和分析指数数据
"""

import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_loader import DataLoader
import pandas as pd


def analyze_single_index():
    """分析单个指数"""
    print("\n" + "="*60)
    print("分析单个指数 - 上证50")
    print("="*60 + "\n")
    
    loader = DataLoader(data_dir='./data')
    
    # 加载数据
    df = loader.load_index_data('000016.SH', start_date='2020-01-01')
    
    if df is None:
        print("✗ 数据加载失败，请先运行 01_download_data.py 下载数据")
        return
    
    print(f"数据概览:")
    print(f"  数据条数: {len(df)}")
    print(f"  日期范围: {df.index.min()} 至 {df.index.max()}")
    print(f"\n前5条数据:")
    print(df.head())
    
    # 基本统计
    print(f"\n收盘价统计:")
    print(df['close'].describe())
    
    # 计算收益率
    returns = df['close'].pct_change()
    print(f"\n收益率统计:")
    print(f"  平均日收益率: {returns.mean():.4%}")
    print(f"  日收益率标准差: {returns.std():.4%}")
    print(f"  最大单日涨幅: {returns.max():.2%}")
    print(f"  最大单日跌幅: {returns.min():.2%}")
    
    # 年化指标
    annual_return = (1 + returns.mean()) ** 252 - 1
    annual_volatility = returns.std() * (252 ** 0.5)
    
    print(f"\n年化指标:")
    print(f"  年化收益率: {annual_return:.2%}")
    print(f"  年化波动率: {annual_volatility:.2%}")
    
    if annual_volatility > 0:
        sharpe = annual_return / annual_volatility
        print(f"  夏普比率: {sharpe:.2f}")


def compare_multiple_indices():
    """比较多个指数"""
    print("\n" + "="*60)
    print("比较多个指数")
    print("="*60 + "\n")
    
    loader = DataLoader(data_dir='./data')
    
    # 加载多个指数的收盘价
    index_codes = ['000016.SH', '000300.SH', '000852.SH', '399006.SZ']
    
    df = loader.load_multiple_indices(
        index_codes=index_codes,
        start_date='2020-01-01',
        column='close'
    )
    
    if df is None:
        print("✗ 数据加载失败")
        return
    
    print(f"已加载 {len(df.columns)} 个指数的数据")
    print(f"数据条数: {len(df)}")
    print(f"\n最新收盘价:")
    print(df.tail())
    
    # 计算相关性
    returns = df.pct_change().dropna()
    correlation = returns.corr()
    
    print(f"\n收益率相关性矩阵:")
    print(correlation.round(3))
    
    # 计算累计收益
    cumulative_returns = (1 + returns).cumprod()
    final_returns = cumulative_returns.iloc[-1] - 1
    
    print(f"\n累计收益率:")
    for col in final_returns.index:
        print(f"  {col}: {final_returns[col]:.2%}")


def analyze_date_ranges():
    """分析数据日期范围"""
    print("\n" + "="*60)
    print("分析数据日期范围")
    print("="*60 + "\n")
    
    loader = DataLoader(data_dir='./data')
    
    # 列出所有可用指数
    available = loader.list_available_indices()
    print("可用指数及其日期范围:")
    print(available.to_string(index=False))
    
    # 获取共同日期范围
    index_codes = ['000016.SH', '000300.SH', '000852.SH', '399006.SZ']
    common_range = loader.get_common_date_range(index_codes)
    
    if common_range:
        print(f"\n这些指数的共同日期范围:")
        print(f"  开始日期: {common_range[0]}")
        print(f"  结束日期: {common_range[1]}")
        print(f"  天数: {(common_range[1] - common_range[0]).days}")


def validate_data_quality():
    """验证数据质量"""
    print("\n" + "="*60)
    print("验证数据质量")
    print("="*60 + "\n")
    
    loader = DataLoader(data_dir='./data')
    
    index_codes = ['000016.SH', '000300.SH']
    
    for index_code in index_codes:
        print(f"\n验证 {index_code}:")
        print("-" * 40)
        
        validation = loader.validate_data(index_code)
        
        if validation.get('valid'):
            print(f"✓ 数据有效")
            print(f"  总行数: {validation['total_rows']}")
            print(f"  日期范围: {validation['date_range'][0]} 至 {validation['date_range'][1]}")
            
            if validation['duplicate_dates'] > 0:
                print(f"  ⚠ 重复日期: {validation['duplicate_dates']}")
            
            if validation['missing_values']:
                print(f"  ⚠ 缺失值:")
                for col, count in validation['missing_values'].items():
                    print(f"    {col}: {count}")
            
            if validation['negative_values']:
                print(f"  ⚠ 负值:")
                for col, count in validation['negative_values'].items():
                    print(f"    {col}: {count}")
            
            if validation.get('large_date_gaps', 0) > 0:
                print(f"  ⚠ 大日期间隔: {validation['large_date_gaps']}")
        else:
            print(f"✗ 数据无效: {validation.get('error')}")


def main():
    """主函数"""
    print("\n" + "="*80)
    print(" "*25 + "数据分析示例")
    print("="*80)
    
    # 分析单个指数
    analyze_single_index()
    
    # 比较多个指数
    compare_multiple_indices()
    
    # 分析日期范围
    analyze_date_ranges()
    
    # 验证数据质量
    validate_data_quality()
    
    print("\n" + "="*80)
    print("数据分析完成！")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()