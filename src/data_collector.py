"""
数据采集模块 (Data Collector Module)

负责从外部数据源（如AKShare）获取中国A股指数的历史数据
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import json
from pathlib import Path
import akshare as ak


class DataCollector:
    """
    数据采集器
    
    负责从AKShare等数据源获取指数数据并保存到本地CSV文件
    """
    
    # 支持的指数配置
    SUPPORTED_INDICES = {
        '000016.SH': {
            'name': '上证50',
            'akshare_symbol': 'sh000016',
            'launch_date': '2004-01-02',
            'base_point': 1000,
            'base_date': '2003-12-31'
        },
        '000300.SH': {
            'name': '沪深300',
            'akshare_symbol': 'sh000300',
            'launch_date': '2005-04-08',
            'base_point': 1000,
            'base_date': '2004-12-31'
        },
        '000852.SH': {
            'name': '中证1000',
            'akshare_symbol': 'sh000852',
            'launch_date': '2014-10-17',
            'base_point': 1000,
            'base_date': '2014-10-16'
        },
        '399006.SZ': {
            'name': '创业板指',
            'akshare_symbol': 'sz399006',
            'launch_date': '2010-06-01',
            'base_point': 1000,
            'base_date': '2010-05-31'
        },
        '000688.SH': {
            'name': '科创50',
            'akshare_symbol': 'sh000688',
            'launch_date': '2019-12-31',
            'base_point': 1000,
            'base_date': '2019-12-30'
        },
        '000015.SH': {
            'name': '上证红利',
            'akshare_symbol': 'sh000015',
            'launch_date': '2005-01-04',
            'base_point': 1000,
            'base_date': '2004-12-31'
        },
        '000905.SH': {
            'name': '中证500',
            'akshare_symbol': 'sh000905',
            'launch_date': '2007-01-15',
            'base_point': 1000,
            'base_date': '2004-12-31'
        }
    }
    
    def __init__(self, data_dir='./data', data_source='akshare'):
        """
        初始化数据采集器
        
        Args:
            data_dir: 数据存储目录
            data_source: 数据源类型，默认为'akshare'
        """
        self.data_dir = Path(data_dir)
        self.data_source = data_source
        self.indices_dir = self.data_dir / 'indices'
        self.dividends_dir = self.data_dir / 'dividends'
        
        # 创建必要的目录
        self._create_directories()
    
    def _create_directories(self):
        """创建数据存储所需的目录结构"""
        self.indices_dir.mkdir(parents=True, exist_ok=True)
        self.dividends_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ 数据目录已创建: {self.data_dir}")
    
    def fetch_index_data(self, index_code, start_date=None, end_date=None):
        """
        获取指数历史数据
        
        Args:
            index_code: 指数代码，如 '000016.SH'
            start_date: 开始日期，格式 'YYYY-MM-DD'
            end_date: 结束日期，格式 'YYYY-MM-DD'
            
        Returns:
            DataFrame: 包含指数历史数据
        """
        if index_code not in self.SUPPORTED_INDICES:
            raise ValueError(f"不支持的指数代码: {index_code}")
        
        index_info = self.SUPPORTED_INDICES[index_code]
        akshare_symbol = index_info['akshare_symbol']
        
        # 设置默认日期范围
        if start_date is None:
            start_date = index_info['launch_date']
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        print(f"正在获取 {index_info['name']} ({index_code}) 的数据...")
        print(f"  日期范围: {start_date} 至 {end_date}")
        
        try:
            # 使用AKShare获取数据
            df = ak.stock_zh_index_daily(symbol=akshare_symbol)
            
            if df is None or df.empty:
                print(f"✗ 未获取到数据")
                return None
            
            # 转换日期格式
            df['date'] = pd.to_datetime(df['date'])
            
            # 筛选日期范围
            mask = (df['date'] >= start_date) & (df['date'] <= end_date)
            df = df[mask].copy()
            
            # 计算涨跌幅
            if 'pct_change' not in df.columns:
                df['pct_change'] = df['close'].pct_change() * 100
            
            # 重置索引
            df = df.reset_index(drop=True)
            
            print(f"✓ 成功获取 {len(df)} 条数据记录")
            return df
            
        except Exception as e:
            print(f"✗ 获取数据失败: {str(e)}")
            return None
    
    def save_to_csv(self, df, index_code):
        """
        保存数据到CSV文件
        
        Args:
            df: 数据DataFrame
            index_code: 指数代码
        """
        if df is None or df.empty:
            print(f"✗ 数据为空，无法保存")
            return False
        
        index_info = self.SUPPORTED_INDICES[index_code]
        filename = f"{index_code.replace('.', '_')}_{index_info['name']}.csv"
        filepath = self.indices_dir / filename
        
        try:
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            print(f"✓ 数据已保存至: {filepath}")
            return True
        except Exception as e:
            print(f"✗ 保存数据失败: {str(e)}")
            return False
    
    def fetch_and_save(self, index_code, start_date=None, end_date=None):
        """
        获取并保存指数数据（组合操作）
        
        Args:
            index_code: 指数代码
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            bool: 是否成功
        """
        df = self.fetch_index_data(index_code, start_date, end_date)
        if df is not None:
            return self.save_to_csv(df, index_code)
        return False
    
    def update_all_indices(self, start_date=None, end_date=None):
        """
        批量更新所有支持的指数数据
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
        """
        print("\n" + "="*60)
        print("开始批量更新指数数据")
        print("="*60 + "\n")
        
        success_count = 0
        fail_count = 0
        
        for index_code in self.SUPPORTED_INDICES.keys():
            print(f"\n[{success_count + fail_count + 1}/{len(self.SUPPORTED_INDICES)}] 处理 {index_code}")
            print("-" * 60)
            
            if self.fetch_and_save(index_code, start_date, end_date):
                success_count += 1
            else:
                fail_count += 1
        
        print("\n" + "="*60)
        print(f"批量更新完成: 成功 {success_count} 个, 失败 {fail_count} 个")
        print("="*60 + "\n")
        
        # 更新元数据
        self._update_metadata()
    
    def _update_metadata(self):
        """更新元数据文件"""
        metadata = {}
        
        for index_code, info in self.SUPPORTED_INDICES.items():
            metadata[index_code] = {
                'name': info['name'],
                'launch_date': info['launch_date'],
                'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'data_source': self.data_source,
                'base_point': info['base_point'],
                'base_date': info['base_date']
            }
        
        metadata_path = self.indices_dir / 'metadata.json'
        try:
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            print(f"✓ 元数据已更新: {metadata_path}")
        except Exception as e:
            print(f"✗ 更新元数据失败: {str(e)}")
    
    def get_supported_indices(self):
        """
        获取支持的指数列表
        
        Returns:
            DataFrame: 支持的指数信息
        """
        indices_list = []
        for code, info in self.SUPPORTED_INDICES.items():
            indices_list.append({
                '指数代码': code,
                '指数名称': info['name'],
                '发布日期': info['launch_date'],
                '基点': info['base_point']
            })
        
        return pd.DataFrame(indices_list)
    
    def check_data_availability(self):
        """
        检查本地数据可用性
        
        Returns:
            DataFrame: 数据可用性报告
        """
        availability = []
        
        for index_code, info in self.SUPPORTED_INDICES.items():
            filename = f"{index_code.replace('.', '_')}_{info['name']}.csv"
            filepath = self.indices_dir / filename
            
            if filepath.exists():
                try:
                    df = pd.read_csv(filepath)
                    availability.append({
                        '指数代码': index_code,
                        '指数名称': info['name'],
                        '状态': '✓ 已下载',
                        '数据条数': len(df),
                        '最早日期': df['date'].min() if 'date' in df.columns else 'N/A',
                        '最新日期': df['date'].max() if 'date' in df.columns else 'N/A'
                    })
                except Exception as e:
                    availability.append({
                        '指数代码': index_code,
                        '指数名称': info['name'],
                        '状态': f'✗ 错误: {str(e)}',
                        '数据条数': 0,
                        '最早日期': 'N/A',
                        '最新日期': 'N/A'
                    })
            else:
                availability.append({
                    '指数代码': index_code,
                    '指数名称': info['name'],
                    '状态': '○ 未下载',
                    '数据条数': 0,
                    '最早日期': 'N/A',
                    '最新日期': 'N/A'
                })
        
        return pd.DataFrame(availability)


if __name__ == '__main__':
    # 测试代码
    collector = DataCollector()
    
    # 显示支持的指数
    print("支持的指数列表:")
    print(collector.get_supported_indices())
    print("\n")
    
    # 检查数据可用性
    print("本地数据可用性:")
    print(collector.check_data_availability())