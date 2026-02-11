"""
示例4: 下载指数数据（包含分红信息）

演示如何下载包含分红数据的指数信息
"""

import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_collector import DataCollector


def main():
    """主函数"""
    print("\n" + "="*80)
    print(" "*20 + "下载指数数据（包含分红）")
    print("="*80 + "\n")
    
    # 创建数据采集器
    collector = DataCollector(data_dir='./data')
    
    print("说明:")
    print("-"*80)
    print("指数本身不直接分红，这里获取的是对应ETF的分红数据作为参考。")
    print("支持分红数据的指数及其对应ETF:")
    print("  - 上证50 (000016.SH) -> 50ETF (510050)")
    print("  - 沪深300 (000300.SH) -> 300ETF (510300)")
    print("  - 中证1000 (000852.SH) -> 1000ETF (159845)")
    print("  - 创业板指 (399006.SZ) -> 创业板ETF (159915)")
    print("  - 科创50 (000688.SH) -> 科创50ETF (588000)")
    print("\n")
    
    # 示例1: 下载单个指数及其分红数据
    print("1. 下载上证50及其分红数据:")
    print("-"*80)
    success = collector.fetch_and_save(
        index_code='000016.SH',
        start_date='2020-01-01',
        include_dividend=True  # 包含分红数据
    )
    
    if success:
        print("✓ 下载成功（包含价格和分红数据）")
    else:
        print("✗ 下载失败")
    print("\n")
    
    # 示例2: 批量下载多个指数及分红数据
    print("2. 批量下载指数及分红数据:")
    print("-"*80)
    
    target_indices = [
        ('000016.SH', '上证50'),
        ('000300.SH', '沪深300'),
        ('000852.SH', '中证1000'),
        ('399006.SZ', '创业板指'),
    ]
    
    success_count = 0
    for index_code, name in target_indices:
        print(f"\n处理 {name} ({index_code})...")
        print("-" * 60)
        
        if collector.fetch_and_save(
            index_code=index_code,
            start_date='2014-01-01',
            include_dividend=True
        ):
            success_count += 1
            print(f"✓ {name} 数据下载完成")
        else:
            print(f"✗ {name} 数据下载失败")
    
    print("\n" + "="*80)
    print(f"批量下载完成: 成功 {success_count}/{len(target_indices)} 个")
    print("="*80 + "\n")
    
    # 示例3: 仅下载分红数据
    print("3. 单独获取分红数据:")
    print("-"*80)
    df_dividend = collector.fetch_dividend_data('000016.SH', start_date='2020-01-01')
    
    if df_dividend is not None and not df_dividend.empty:
        print(f"\n上证50对应ETF的分红记录:")
        print(df_dividend.to_string(index=False))
        
        # 保存分红数据
        collector.save_dividend_data(df_dividend, '000016.SH')
    else:
        print("⚠ 无可用的分红数据")
    
    print("\n" + "="*80)
    print("数据下载完成！")
    print("价格数据保存在: data/indices/")
    print("分红数据保存在: data/dividends/")
    print("="*80 + "\n")
    
    # 示例4: 查看分红数据文件
    print("4. 查看已下载的分红数据文件:")
    print("-"*80)
    dividends_dir = Path('data/dividends')
    if dividends_dir.exists():
        dividend_files = list(dividends_dir.glob('*.csv'))
        if dividend_files:
            print(f"找到 {len(dividend_files)} 个分红数据文件:")
            for file in dividend_files:
                print(f"  - {file.name}")
        else:
            print("  暂无分红数据文件")
    else:
        print("  分红数据目录不存在")
    print("\n")


if __name__ == '__main__':
    main()