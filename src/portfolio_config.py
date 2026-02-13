"""
投资组合配置模块 (Portfolio Configuration Module)

定义投资组合的配置参数，包括资产配置、再平衡策略、红利处理等
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from .logger import get_logger


class PortfolioConfig:
    """
    投资组合配置类
    
    管理投资组合的所有配置参数
    """
    
    def __init__(self, name: str = "未命名组合", log_dir='./logs'):
        """
        初始化投资组合配置
        
        Args:
            name: 组合名称
            log_dir: 日志目录
        """
        self.name = name
        self.logger = get_logger('portfolio_config', log_dir=log_dir)
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
        
        self.logger.info(f"Added index: {name or index_code} ({index_code}), weight: {weight:.2%}")
    
    def remove_index(self, index_code: str):
        """
        移除指数
        
        Args:
            index_code: 指数代码
        """
        if index_code in self.indices:
            del self.indices[index_code]
            self.logger.info(f"Removed index: {index_code}")
        else:
            self.logger.warning(f"Index does not exist: {index_code}")
    
    def set_date_range(self, start_date: str, end_date: str):
        """
        设置回测日期范围
        
        Args:
            start_date: 开始日期，格式 'YYYY-MM-DD'
            end_date: 结束日期，格式 'YYYY-MM-DD'
        """
        self.start_date = start_date
        self.end_date = end_date
        self.logger.info(f"Backtest date range: {start_date} to {end_date}")
    
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
        
        self.logger.info(f"Rebalancing strategy: {method} method, frequency: {frequency}")
        if method == 'threshold':
            self.logger.info(f"Threshold: {threshold:.2%}")
    
    def set_dividend_policy(self, reinvest: bool = True):
        """
        设置红利政策
        
        Args:
            reinvest: 是否红利再投资
        """
        self.dividend_reinvest = reinvest
        policy = "Dividend reinvestment" if reinvest else "Cash dividend"
        self.logger.info(f"Dividend policy: {policy}")
    
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
        self.logger.info(f"Transaction cost: {transaction_cost:.4%}, management fee: {management_fee:.4%}")
    
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
            self.logger.warning("No indices to normalize")
            return
        
        total_weight = sum(idx['weight'] for idx in self.indices.values())
        
        if total_weight == 0:
            self.logger.error("Total weight is 0, cannot normalize")
            return
        
        for index_code in self.indices:
            self.indices[index_code]['weight'] /= total_weight
        
        self.logger.info(f"Weights normalized (original total: {total_weight:.4f})")
    
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
            self.logger.warning("Configuration validation failed, but will still save:")
            for error in errors:
                self.logger.warning(f"  - {error}")
        
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
            self.logger.info(f"Configuration saved to: {filepath}")
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {str(e)}")
    
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
            config.logger.info(f"Configuration loaded: {config.name}")
            return config
            
        except Exception as e:
            raise Exception(f"加载配置失败: {str(e)}")
    
    def print_summary(self):
        """
        打印配置摘要
        """
        summary = []
        summary.append("\n" + "="*60)
        summary.append(f"Portfolio Configuration: {self.name}")
        summary.append("="*60)
        
        if self.description:
            summary.append(f"\nDescription: {self.description}")
        
        summary.append(f"\nBasic Information:")
        summary.append(f"  Initial Capital: {self.initial_capital:,.0f}")
        summary.append(f"  Backtest Period: {self.start_date} to {self.end_date}")
        
        summary.append(f"\nIndex Configuration:")
        for code, info in self.indices.items():
            summary.append(f"  {info['name']:12s} ({code}): {info['weight']:6.2%}")
        
        total_weight = sum(idx['weight'] for idx in self.indices.values())
        summary.append(f"  {'Total Weight':12s}           : {total_weight:6.2%}")
        
        summary.append(f"\nRebalancing Strategy:")
        summary.append(f"  Method: {self.rebalance_method}")
        summary.append(f"  Frequency: {self.rebalance_frequency}")
        if self.rebalance_method == 'threshold':
            summary.append(f"  Threshold: {self.rebalance_threshold:.2%}")
        
        summary.append(f"\nDividend Policy:")
        policy = "Dividend reinvestment" if self.dividend_reinvest else "Cash dividend"
        summary.append(f"  {policy}")
        
        summary.append(f"\nTransaction Costs:")
        summary.append(f"  Transaction cost rate: {self.transaction_cost_rate:.4%}")
        summary.append(f"  Management fee rate: {self.management_fee_rate:.4%}")
        
        # 验证配置
        is_valid, errors = self.validate()
        summary.append(f"\nConfiguration Status:")
        if is_valid:
            summary.append(f"  Valid")
        else:
            summary.append(f"  Invalid - Issues found:")
            for error in errors:
                summary.append(f"    - {error}")
        
        summary.append("="*60 + "\n")
        
        # Print and log
        summary_text = "\n".join(summary)
        print(summary_text)
        self.logger.info("Configuration summary displayed")


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