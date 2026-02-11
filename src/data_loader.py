"""
数据加载模块 (Data Loader Module)

负责从本地CSV文件加载指数数据，提供便捷的数据访问接口
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json
from typing import List, Dict, Optional, Union


class DataLoader:
    """
    数据加载器
    
    从本地CSV文件加载指数历史数据，支持日期范围筛选和多指数加载
    """
    
    def __init__(self, data_dir='./data'):
        """
        初始化数据加载器
        
        Args:
            data_dir: 数据存储目录
        """
        self.data_dir = Path(data_dir)
        self.indices_dir = self.data_dir / 'indices'
        self.dividends_dir = self.data_dir / 'dividends'
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict:
        """
        加载元数据文件
        
        Returns:
            Dict: 元数据字典
        """
        metadata_path = self.indices_dir / 'metadata.json'
        
        if not metadata_path.exists():
            print(f"⚠ 元数据文件不存在: {metadata_path}")
            return {}
        
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            return metadata
        except Exception as e:
            print(f"✗ 加载元数据失败: {str(e)}")
            return {}
    
    def get_index_filepath(self, index_code: str) -> Path:
        """
        获取指数数据文件路径
        
        Args:
            index_code: 指数代码，如 '000016.SH'
            
        Returns:
            Path: 文件路径
        """
        if index_code in self.metadata:
            index_name = self.metadata[index_code]['name']
            filename = f"{index_code.replace('.', '_')}_{index_name}.csv"
        else:
            # 如果元数据中没有，尝试查找匹配的文件
            pattern = f"{index_code.replace('.', '_')}_*.csv"
            matching_files = list(self.indices_dir.glob(pattern))
            if matching_files:
                return matching_files[0]
            filename = f"{index_code.replace('.', '_')}.csv"
        
        return self.indices_dir / filename
    
    def load_index_data(self, 
                       index_code: str, 
                       start_date: Optional[str] = None, 
                       end_date: Optional[str] = None) -> Optional[pd.DataFrame]:
        """
        加载单个指数的历史数据
        
        Args:
            index_code: 指数代码，如 '000016.SH'
            start_date: 开始日期，格式 'YYYY-MM-DD'
            end_date: 结束日期，格式 'YYYY-MM-DD'
            
        Returns:
            DataFrame: 指数历史数据，如果失败返回None
        """
        filepath = self.get_index_filepath(index_code)
        
        if not filepath.exists():
            print(f"✗ 数据文件不存在: {filepath}")
            print(f"  提示: 请先使用 DataCollector 下载数据")
            return None
        
        try:
            # 读取CSV文件
            df = pd.read_csv(filepath)
            
            # 转换日期格式
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
            else:
                print(f"✗ 数据文件缺少 'date' 列")
                return None
            
            # 筛选日期范围
            if start_date is not None:
                df = df[df['date'] >= start_date]
            if end_date is not None:
                df = df[df['date'] <= end_date]
            
            # 设置日期为索引
            df = df.set_index('date').sort_index()
            
            if df.empty:
                print(f"⚠ 在指定日期范围内没有数据")
                return None
            
            return df
            
        except Exception as e:
            print(f"✗ 加载数据失败: {str(e)}")
            return None
    
    def load_multiple_indices(self, 
                             index_codes: List[str], 
                             start_date: Optional[str] = None, 
                             end_date: Optional[str] = None,
                             column: str = 'close') -> Optional[pd.DataFrame]:
        """
        加载多个指数的数据，合并为一个DataFrame
        
        Args:
            index_codes: 指数代码列表
            start_date: 开始日期
            end_date: 结束日期
            column: 要提取的列名，默认为'close'
            
        Returns:
            DataFrame: 多列DataFrame，每列为一个指数的数据
        """
        dfs = {}
        
        for index_code in index_codes:
            df = self.load_index_data(index_code, start_date, end_date)
            if df is not None and column in df.columns:
                # 获取指数名称作为列名
                if index_code in self.metadata:
                    col_name = f"{self.metadata[index_code]['name']}({index_code})"
                else:
                    col_name = index_code
                
                dfs[col_name] = df[column]
            else:
                print(f"⚠ 跳过 {index_code}: 数据加载失败或缺少列 '{column}'")
        
        if not dfs:
            print(f"✗ 未能加载任何指数数据")
            return None
        
        # 合并所有数据
        result = pd.DataFrame(dfs)
        
        # 填充缺失值（使用前向填充）
        result = result.fillna(method='ffill')
        
        return result
    
    def load_index_returns(self, 
                          index_code: str, 
                          start_date: Optional[str] = None, 
                          end_date: Optional[str] = None,
                          freq: str = 'daily') -> Optional[pd.Series]:
        """
        加载指数收益率数据
        
        Args:
            index_code: 指数代码
            start_date: 开始日期
            end_date: 结束日期
            freq: 收益率频率，'daily', 'weekly', 'monthly'
            
        Returns:
            Series: 收益率序列
        """
        df = self.load_index_data(index_code, start_date, end_date)
        
        if df is None or 'close' not in df.columns:
            return None
        
        # 计算收益率
        if freq == 'daily':
            returns = df['close'].pct_change()
        elif freq == 'weekly':
            returns = df['close'].resample('W').last().pct_change()
        elif freq == 'monthly':
            returns = df['close'].resample('M').last().pct_change()
        else:
            print(f"✗ 不支持的频率: {freq}")
            return None
        
        # 移除NaN值
        returns = returns.dropna()
        
        return returns
    
    def get_date_range(self, index_code: str) -> Optional[tuple]:
        """
        获取指数数据的日期范围
        
        Args:
            index_code: 指数代码
            
        Returns:
            tuple: (开始日期, 结束日期)
        """
        df = self.load_index_data(index_code)
        
        if df is None:
            return None
        
        return (df.index.min(), df.index.max())
    
    def get_common_date_range(self, index_codes: List[str]) -> Optional[tuple]:
        """
        获取多个指数的共同日期范围
        
        Args:
            index_codes: 指数代码列表
            
        Returns:
            tuple: (共同开始日期, 共同结束日期)
        """
        start_dates = []
        end_dates = []
        
        for index_code in index_codes:
            date_range = self.get_date_range(index_code)
            if date_range:
                start_dates.append(date_range[0])
                end_dates.append(date_range[1])
        
        if not start_dates:
            return None
        
        # 返回最晚的开始日期和最早的结束日期
        common_start = max(start_dates)
        common_end = min(end_dates)
        
        if common_start > common_end:
            print(f"⚠ 指数之间没有重叠的日期范围")
            return None
        
        return (common_start, common_end)
    
    def load_dividend_data(self, index_code: str) -> Optional[pd.DataFrame]:
        """
        加载分红数据
        
        Args:
            index_code: 指数代码
            
        Returns:
            DataFrame: 分红数据
        """
        filename = f"{index_code.replace('.', '_')}_dividends.csv"
        filepath = self.dividends_dir / filename
        
        if not filepath.exists():
            print(f"✗ 分红数据文件不存在: {filepath}")
            return None
        
        try:
            df = pd.read_csv(filepath)
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
                df = df.set_index('date').sort_index()
            return df
        except Exception as e:
            print(f"✗ 加载分红数据失败: {str(e)}")
            return None
    
    def get_index_info(self, index_code: str) -> Optional[Dict]:
        """
        获取指数的元数据信息
        
        Args:
            index_code: 指数代码
            
        Returns:
            Dict: 指数信息
        """
        if index_code in self.metadata:
            return self.metadata[index_code]
        else:
            print(f"⚠ 元数据中未找到 {index_code}")
            return None
    
    def list_available_indices(self) -> pd.DataFrame:
        """
        列出所有可用的指数数据
        
        Returns:
            DataFrame: 可用指数列表及其信息
        """
        indices_list = []
        
        # 从CSV文件中获取
        csv_files = list(self.indices_dir.glob('*.csv'))
        
        for filepath in csv_files:
            if filepath.name == 'metadata.json':
                continue
            
            # 解析文件名获取指数代码
            filename = filepath.stem
            parts = filename.split('_')
            if len(parts) >= 2:
                # 重构指数代码（例如 000016_SH -> 000016.SH）
                code_parts = parts[0].split('_')
                if len(code_parts) == 2:
                    index_code = f"{code_parts[0]}.{code_parts[1]}"
                else:
                    index_code = parts[0].replace('_', '.')
                
                index_name = '_'.join(parts[1:])
                
                # 获取数据统计
                try:
                    df = pd.read_csv(filepath)
                    data_count = len(df)
                    if 'date' in df.columns:
                        start_date = df['date'].min()
                        end_date = df['date'].max()
                    else:
                        start_date = 'N/A'
                        end_date = 'N/A'
                except:
                    data_count = 0
                    start_date = 'N/A'
                    end_date = 'N/A'
                
                indices_list.append({
                    '指数代码': index_code,
                    '指数名称': index_name,
                    '数据条数': data_count,
                    '开始日期': start_date,
                    '结束日期': end_date
                })
        
        if not indices_list:
            print("⚠ 没有找到任何指数数据文件")
            return pd.DataFrame()
        
        return pd.DataFrame(indices_list)
    
    def validate_data(self, index_code: str) -> Dict:
        """
        验证数据完整性
        
        Args:
            index_code: 指数代码
            
        Returns:
            Dict: 验证结果
        """
        df = self.load_index_data(index_code)
        
        if df is None:
            return {'valid': False, 'error': '无法加载数据'}
        
        validation = {
            'valid': True,
            'total_rows': len(df),
            'date_range': (df.index.min(), df.index.max()),
            'missing_dates': 0,
            'duplicate_dates': 0,
            'missing_values': {},
            'negative_values': {}
        }
        
        # 检查重复日期
        validation['duplicate_dates'] = df.index.duplicated().sum()
        
        # 检查缺失值
        for col in df.columns:
            missing_count = df[col].isna().sum()
            if missing_count > 0:
                validation['missing_values'][col] = missing_count
        
        # 检查负值（价格列不应该为负）
        price_columns = ['open', 'close', 'high', 'low']
        for col in price_columns:
            if col in df.columns:
                negative_count = (df[col] < 0).sum()
                if negative_count > 0:
                    validation['negative_values'][col] = negative_count
        
        # 检查日期连续性（工作日）
        date_diff = df.index.to_series().diff()
        large_gaps = (date_diff > pd.Timedelta(days=7)).sum()
        validation['large_date_gaps'] = large_gaps
        
        return validation


if __name__ == '__main__':
    # 测试代码
    loader = DataLoader()
    
    # 列出可用的指数
    print("可用的指数数据:")
    print(loader.list_available_indices())
    print("\n")
    
    # 示例: 加载单个指数
    print("加载上证50数据示例:")
    df = loader.load_index_data('000016.SH', start_date='2020-01-01', end_date='2023-12-31')
    if df is not None:
        print(df.head())