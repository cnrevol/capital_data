"""
投资组合配置模块 (Portfolio Configuration Module)

定义投资组合的配置参数，包括资产配置、再平衡策略、红利处理等
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class PortfolioConfig:
    """
    投资组合配置类
    
    管理投资组合的所有配置参数
    """
    
    def __init__(self, name: str = "未命名组合"):
        """
        初始化投资组合配置
        
        Args:
            name: 组合名称
        """
        self.name = name
        self.indices = {}  # {index_code: weight}
        self.start_date = None
        self.end_date = None
        self.initial_capital = 1000000  # 初始资金，默认100万
        
        # 再平衡配置
        self.rebalance_frequency = 'quarterly'  # monthly, quarterly, yearly, none
        self.rebalance_method = 'calendar'  # calendar, threshold
        self.rebalance_threshold = 0.05  # 5%偏离度触发再平衡
        
        # 红利配置
        self.dividend_reinvest = True  # 是否红利再投资
        
        # 交易成本
        self.transaction_cost_rate = 0.0003  # 0.03%
        self.management_fee_rate = 0.0000  # 管理费率，年化
        
        # 其他配置
        self.description = ""
        self.created_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def add_index(self, index_code: str, weight: float, name: Optional[str] = None):
        """
        添加指数及其权重
        
        Args:
            index_code: 指数代码，如 '000016.SH'
            weight: 权重，应为0到1之间的数值
            name: 指数名称（可选）
        """
        if weight < 0 or weight > 1:
            raise ValueError(f"权重必须在0到1之间，当前值: {weight}")
        
        self.indices[index_code] = {
            'weight': weight,
            'name': name or index_code
        }
        
        print(f"✓ 已添加指数: {name or index_code} ({index_code}), 权重: {weight:.2%}")
    
    def remove_index(self, index_code: str):
        """
        移除指数
        
        Args:
            index_code: 指数代码
        """
        if index_code in self.indices:
            del self.indices[index_code]
            print(f"✓ 已移除指数: {index_code}")
        else:
            print(f"⚠ 指数不存在: {index_code}")
    
    def set_date_range(self, start_date: str, end_date: str):
        """
        设置回测日期范围
        
        Args:
            start_date: 开始日期，格式 'YYYY-MM-DD'
            end_date: 结束日期，格式 'YYYY-MM-DD'
        """
        self.start_date = start_date
        self.end_date = end_date
        print(f"✓ 回测日期范围: {start_date} 至 {end_date}")
    
    def set_rebalancing(self, frequency: str = 'quarterly', 
                       method: str = 'calendar', 
                       threshold: float = 0.05):
        """
        设置再平衡策略
        
        Args:
            frequency: 再平衡频率 ('monthly', 'quarterly', 'yearly', 'none')
            method: 再平衡方法 ('calendar', 'threshold')
            threshold: 阈值（当method='threshold'时使用）
        """
        valid_frequencies = ['monthly', 'quarterly', 'yearly', 'none']
        valid_methods = ['calendar', 'threshold']
        
        if frequency not in valid_frequencies:
            raise ValueError(f"无效的频率: {frequency}，有效值: {valid_frequencies}")
        if method not in valid_methods:
            raise ValueError(f"无效的方法: {method}，有效值: {valid_methods}")
        
        self.rebalance_frequency = frequency
        self.rebalance_method = method
        self.rebalance_threshold = threshold
        
        print(f"✓ 再平衡策略: {method}方式, 频率: {frequency}")
        if method == 'threshold':
            print(f"  阈值: {threshold:.2%}")
    
    def set_dividend_policy(self, reinvest: bool = True):
        """
        设置红利政策
        
        Args:
            reinvest: 是否红利再投资
        """
        self.dividend_reinvest = reinvest
        policy = "红利再投资" if reinvest else "现金分红"
        print(f"✓ 红利政策: {policy}")
    
    def set_costs(self, transaction_cost: float = 0.0003, 
                  management_fee: float = 0.0000):
        """
        设置交易成本
        
        Args:
            transaction_cost: 交易成本率
            management_fee: 管理费率（年化）
        """
        self.transaction_cost_rate = transaction_cost
        self.management_fee_rate = management_fee
        print(f"✓ 交易成本: {transaction_cost:.4%}, 管理费: {management_fee:.4%}")
    
    def validate(self) -> tuple:
        """
        验证配置有效性
        
        Returns:
            tuple: (是否有效, 错误信息列表)
        """
        errors = []
        
        # 检查是否有指数
        if not self.indices:
            errors.append("未添加任何指数")
        
        # 检查权重和是否为1
        if self.indices:
            total_weight = sum(idx['weight'] for idx in self.indices.values())
            if abs(total_weight - 1.0) > 0.0001:  # 允许小的浮点误差
                errors.append(f"权重和必须为1.0，当前为 {total_weight:.4f}")
        
        # 检查日期范围
        if not self.start_date:
            errors.append("未设置开始日期")
        if not self.end_date:
            errors.append("未设置结束日期")
        
        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                errors.append("开始日期必须早于结束日期")
        
        # 检查初始资金
        if self.initial_capital <= 0:
            errors.append("初始资金必须大于0")
        
        is_valid = len(errors) == 0
        return (is_valid, errors)
    
    def normalize_weights(self):
        """
        归一化权重，使其和为1
        """
        if not self.indices:
            print("⚠ 没有指数可以归一化")
            return
        
        total_weight = sum(idx['weight'] for idx in self.indices.values())
        
        if total_weight == 0:
            print("✗ 权重总和为0，无法归一化")
            return
        
        for index_code in self.indices:
            self.indices[index_code]['weight'] /= total_weight
        
        print(f"✓ 权重已归一化（原总和: {total_weight:.4f}）")
    
    def get_weights_dict(self) -> Dict[str, float]:
        """
        获取权重字典
        
        Returns:
            Dict: {index_code: weight}
        """
        return {code: info['weight'] for code, info in self.indices.items()}
    
    def get_index_codes(self) -> List[str]:
        """
        获取所有指数代码列表
        
        Returns:
            List: 指数代码列表
        """
        return list(self.indices.keys())
    
    def to_dict(self) -> Dict:
        """
        转换为字典格式
        
        Returns:
            Dict: 配置字典
        """
        return {
            'name': self.name,
            'description': self.description,
            'initial_capital': self.initial_capital,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'indices': self.indices,
            'rebalancing': {
                'frequency': self.rebalance_frequency,
                'method': self.rebalance_method,
                'threshold': self.rebalance_threshold
            },
            'dividend': {
                'reinvest': self.dividend_reinvest
            },
            'costs': {
                'transaction_cost_rate': self.transaction_cost_rate,
                'management_fee_rate': self.management_fee_rate
            },
            'created_time': self.created_time
        }
    
    @classmethod
    def from_dict(cls, config_dict: Dict) -> 'PortfolioConfig':
        """
        从字典创建配置对象
        
        Args:
            config_dict: 配置字典
            
        Returns:
            PortfolioConfig: 配置对象
        """
        config = cls(name=config_dict.get('name', '未命名组合'))
        config.description = config_dict.get('description', '')
        config.initial_capital = config_dict.get('initial_capital', 1000000)
        config.start_date = config_dict.get('start_date')
        config.end_date = config_dict.get('end_date')
        config.indices = config_dict.get('indices', {})
        
        # 再平衡配置
        rebalancing = config_dict.get('rebalancing', {})
        config.rebalance_frequency = rebalancing.get('frequency', 'quarterly')
        config.rebalance_method = rebalancing.get('method', 'calendar')
        config.rebalance_threshold = rebalancing.get('threshold', 0.05)
        
        # 红利配置
        dividend = config_dict.get('dividend', {})
        config.dividend_reinvest = dividend.get('reinvest', True)
        
        # 成本配置
        costs = config_dict.get('costs', {})
        config.transaction_cost_rate = costs.get('transaction_cost_rate', 0.0003)
        config.management_fee_rate = costs.get('management_fee_rate', 0.0000)
        
        config.created_time = config_dict.get('created_time', 
                                             datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        return config
    
    def save_config(self, filepath: str):
        """
        保存配置到JSON文件
        
        Args:
            filepath: 文件路径
        """
        # 验证配置
        is_valid, errors = self.validate()
        if not is_valid:
            print("⚠ 配置验证失败，但仍将保存:")
            for error in errors:
                print(f"  - {error}")
        
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
            print(f"✓ 配置已保存至: {filepath}")
        except Exception as e:
            print(f"✗ 保存配置失败: {str(e)}")
    
    @classmethod
    def load_config(cls, filepath: str) -> 'PortfolioConfig':
        """
        从JSON文件加载配置
        
        Args:
            filepath: 文件路径
            
        Returns:
            PortfolioConfig: 配置对象
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"配置文件不存在: {filepath}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                config_dict = json.load(f)
            
            config = cls.from_dict(config_dict)
            print(f"✓ 已加载配置: {config.name}")
            return config
            
        except Exception as e:
            raise Exception(f"加载配置失败: {str(e)}")
    
    def print_summary(self):
        """
        打印配置摘要
        """
        print("\n" + "="*60)
        print(f"投资组合配置: {self.name}")
        print("="*60)
        
        if self.description:
            print(f"\n描述: {self.description}")
        
        print(f"\n基本信息:")
        print(f"  初始资金: ¥{self.initial_capital:,.0f}")
        print(f"  回测期间: {self.start_date} 至 {self.end_date}")
        
        print(f"\n指数配置:")
        for code, info in self.indices.items():
            print(f"  {info['name']:12s} ({code}): {info['weight']:6.2%}")
        
        total_weight = sum(idx['weight'] for idx in self.indices.values())
        print(f"  {'权重总和':12s}           : {total_weight:6.2%}")
        
        print(f"\n再平衡策略:")
        print(f"  方式: {self.rebalance_method}")
        print(f"  频率: {self.rebalance_frequency}")
        if self.rebalance_method == 'threshold':
            print(f"  阈值: {self.rebalance_threshold:.2%}")
        
        print(f"\n红利政策:")
        policy = "红利再投资" if self.dividend_reinvest else "现金分红"
        print(f"  {policy}")
        
        print(f"\n交易成本:")
        print(f"  交易成本率: {self.transaction_cost_rate:.4%}")
        print(f"  管理费率: {self.management_fee_rate:.4%}")
        
        # 验证配置
        is_valid, errors = self.validate()
        print(f"\n配置状态:")
        if is_valid:
            print(f"  ✓ 配置有效")
        else:
            print(f"  ✗ 配置存在问题:")
            for error in errors:
                print(f"    - {error}")
        
        print("="*60 + "\n")


if __name__ == '__main__':
    # 测试代码
    config = PortfolioConfig(name="测试组合")
    config.add_index('000016.SH', 0.30, '上证50')
    config.add_index('000300.SH', 0.30, '沪深300')
    config.add_index('000852.SH', 0.20, '中证1000')
    config.add_index('399006.SZ', 0.20, '创业板指')
    config.set_date_range('2020-01-01', '2023-12-31')
    config.set_rebalancing('quarterly', 'calendar')
    config.set_dividend_policy(True)
    config.print_summary()