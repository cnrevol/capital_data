"""
示例1: 下载指数数据

演示如何使用DataCollector下载中国A股指数的历史数据
"""

import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_collector import DataCollector


def main():
    """主函数"""
    print("="*60)
    print("示例1: 下载指数数据")
    print("="*60 + "\n")
    
    # 创建数据采集器
    collector = DataCollector(
        data_dir='./data',
        config_path='./capital_data/config/indices_config.json'
    )
    
    # 显示支持的指数列表
    print("1. 查看支持的指数:")
    print("-"*60)
    indices_df = collector.get_supported_indices()
    print(indices_df.to_string(index=False))
    print("\n")
    
    # 检查本地数据可用性
    print("2. 检查本地数据可用性:")
    print("-"*60)
    availability_df = collector.check_data_availability()
    print(availability_df.to_string(index=False))
    print("\n")
    
    # 示例：下载单个指数数据
    print("3. 下载单个指数数据 (上证50):")
    print("-"*60)
    success = collector.fetch_and_save(
        index_code='000016.SH',
        start_date='2020-01-01',
        end_date='2023-12-31'
    )
    
    if success:
        print("[OK] 下载成功！")
    else:
        print("[FAIL] 下载失败！")
    print("\n")
    
    # 批量下载所有指数（可选，注释掉以避免频繁请求）
    print("4. 批量下载所有指数 (可选):")
    print("-"*60)
    print("提示: 取消注释以下代码可批量下载所有指数")
    # print("# collector.update_all_indices(start_date='2020-01-01')")
    print("\n")
    collector.update_all_indices(start_date='2020-01-01')
    # 建议：按需下载
    print("5. 推荐做法 - 按需下载特定指数:")
    print("-"*60)
    target_indices = [
        '000016.SH',  # 上证50
        '000300.SH',  # 沪深300
        '000852.SH',  # 中证1000
        '399006.SZ',  # 创业板指
    ]
    
    for index_code in target_indices:
        print(f"\n下载 {index_code}...")
        collector.fetch_and_save(
            index_code=index_code,
            start_date='2014-01-01'  # 从中证1000发布日开始
        )
    
    print("\n" + "="*60)
    print("数据下载完成！")
    print("="*60)


if __name__ == '__main__':
    main()