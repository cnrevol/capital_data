"""
示例2: 创建投资组合配置

演示如何创建和配置投资组合
"""

import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.portfolio_config import PortfolioConfig


def create_balanced_portfolio():
    """创建均衡配置组合"""
    print("\n" + "="*60)
    print("创建均衡配置组合")
    print("="*60 + "\n")
    
    # 创建配置对象
    config = PortfolioConfig(name="均衡配置组合")
    config.description = "大中小盘均衡配置，适合长期投资"
    
    # 设置初始资金
    config.initial_capital = 1000000  # 100万
    
    # 添加指数及权重
    config.add_index('000016.SH', 0.30, '上证50')
    config.add_index('000300.SH', 0.30, '沪深300')
    config.add_index('000852.SH', 0.20, '中证1000')
    config.add_index('399006.SZ', 0.20, '创业板指')
    
    # 设置回测日期范围
    config.set_date_range('2014-10-17', '2023-12-31')
    
    # 设置再平衡策略（季度再平衡）
    config.set_rebalancing(frequency='quarterly', method='calendar')
    
    # 设置红利再投资
    config.set_dividend_policy(reinvest=True)
    
    # 设置交易成本
    config.set_costs(transaction_cost=0.0003, management_fee=0.0000)
    
    # 打印配置摘要
    config.print_summary()
    
    # 保存配置
    config.save_config('data/portfolios/balanced_portfolio.json')
    
    return config


def create_largecap_portfolio():
    """创建大盘股组合"""
    print("\n" + "="*60)
    print("创建大盘股组合")
    print("="*60 + "\n")
    
    config = PortfolioConfig(name="大盘股组合")
    config.description = "专注于大盘蓝筹股，风险较低"
    
    config.initial_capital = 1000000
    
    # 添加大盘指数
    config.add_index('000016.SH', 0.50, '上证50')
    config.add_index('000300.SH', 0.50, '沪深300')
    
    config.set_date_range('2014-01-01', '2023-12-31')
    config.set_rebalancing(frequency='yearly', method='calendar')
    config.set_dividend_policy(reinvest=True)
    
    config.print_summary()
    config.save_config('data/portfolios/largecap_portfolio.json')
    
    return config


def create_growth_portfolio():
    """创建成长型组合"""
    print("\n" + "="*60)
    print("创建成长型组合")
    print("="*60 + "\n")
    
    config = PortfolioConfig(name="成长型组合")
    config.description = "侧重中小盘和创业板，追求高成长"
    
    config.initial_capital = 1000000
    
    # 添加成长性指数
    config.add_index('000852.SH', 0.40, '中证1000')
    config.add_index('399006.SZ', 0.40, '创业板指')
    config.add_index('000300.SH', 0.20, '沪深300')
    
    config.set_date_range('2014-10-17', '2023-12-31')
    config.set_rebalancing(frequency='quarterly', method='threshold', threshold=0.10)
    config.set_dividend_policy(reinvest=True)
    
    config.print_summary()
    config.save_config('data/portfolios/growth_portfolio.json')
    
    return config


def create_dividend_portfolio():
    """创建红利策略组合"""
    print("\n" + "="*60)
    print("创建红利策略组合")
    print("="*60 + "\n")
    
    config = PortfolioConfig(name="红利策略组合")
    config.description = "关注高股息指数，追求稳定现金流"
    
    config.initial_capital = 1000000
    
    # 添加红利指数
    config.add_index('000015.SH', 0.60, '上证红利')
    config.add_index('000016.SH', 0.40, '上证50')
    
    config.set_date_range('2014-01-01', '2023-12-31')
    config.set_rebalancing(frequency='yearly', method='calendar')
    
    # 红利再投资
    config.set_dividend_policy(reinvest=True)
    
    config.print_summary()
    config.save_config('data/portfolios/dividend_portfolio.json')
    
    return config


def load_and_modify_portfolio():
    """加载并修改已有配置"""
    print("\n" + "="*60)
    print("加载并修改已有配置")
    print("="*60 + "\n")
    
    # 加载配置
    config = PortfolioConfig.load_config('data/portfolios/balanced_portfolio.json')
    
    print("原始配置:")
    config.print_summary()
    
    # 修改配置
    print("\n修改配置...")
    config.name = "均衡配置组合 v2"
    config.description = "调整后的均衡配置"
    
    # 调整权重
    config.remove_index('399006.SZ')
    config.add_index('000905.SH', 0.20, '中证500')
    
    # 归一化权重
    config.normalize_weights()
    
    print("\n修改后的配置:")
    config.print_summary()
    
    # 保存为新配置
    config.save_config('data/portfolios/balanced_portfolio_v2.json')


def main():
    """主函数"""
    print("\n" + "="*80)
    print(" "*20 + "投资组合配置示例")
    print("="*80)
    
    # 创建几个示例组合
    create_balanced_portfolio()
    create_largecap_portfolio()
    create_growth_portfolio()
    create_dividend_portfolio()
    
    # 演示加载和修改
    load_and_modify_portfolio()
    
    print("\n" + "="*80)
    print("所有组合配置已创建完成！")
    print("配置文件保存在: data/portfolios/")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()