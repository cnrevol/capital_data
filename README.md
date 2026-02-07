# 中国A股指数投资组合回测系统

一个基于Python的投资组合回测系统，专为中国A股市场指数投资设计，支持多种再平衡策略、红利再投资等功能。

## 🌟 主要特性

- **多数据源支持**: 使用AKShare获取免费的中国A股指数数据
- **灵活的组合配置**: 支持多指数组合，自定义权重分配
- **再平衡策略**: 
  - 日历再平衡（月度/季度/年度）
  - 阈值触发再平衡
- **红利处理**: 支持红利再投资和现金分红两种模式
- **性能分析**: 计算多种绩效指标（收益率、波动率、夏普比率、最大回撤等）
- **数据可视化**: 生成净值曲线、回撤图等可视化图表
- **报告生成**: 自动生成详细的回测报告

## 📦 支持的指数

| 指数名称 | 指数代码 | 发布日期 |
|---------|---------|---------|
| 上证50 | 000016.SH | 2004-01-02 |
| 沪深300 | 000300.SH | 2005-04-08 |
| 中证500 | 000905.SH | 2007-01-15 |
| 中证1000 | 000852.SH | 2014-10-17 |
| 创业板指 | 399006.SZ | 2010-06-01 |
| 科创50 | 000688.SH | 2019-12-31 |
| 上证红利 | 000015.SH | 2005-01-04 |

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 下载数据

```python
from src.data_collector import DataCollector

# 创建数据采集器
collector = DataCollector(data_dir='./data')

# 下载指数数据
collector.fetch_and_save('000016.SH', start_date='2020-01-01')

# 或批量下载所有指数
collector.update_all_indices(start_date='2014-01-01')
```

### 3. 创建投资组合

```python
from src.portfolio_config import PortfolioConfig

# 创建配置
config = PortfolioConfig(name="均衡配置组合")

# 添加指数及权重
config.add_index('000016.SH', 0.30, '上证50')
config.add_index('000300.SH', 0.30, '沪深300')
config.add_index('000852.SH', 0.20, '中证1000')
config.add_index('399006.SZ', 0.20, '创业板指')

# 设置回测参数
config.set_date_range('2014-10-17', '2023-12-31')
config.set_rebalancing(frequency='quarterly', method='calendar')
config.set_dividend_policy(reinvest=True)

# 保存配置
config.save_config('data/portfolios/my_portfolio.json')
```

### 4. 运行回测（即将支持）

```python
from src.backtest_engine import BacktestEngine
from src.data_loader import DataLoader

# 加载配置和数据
config = PortfolioConfig.load_config('data/portfolios/my_portfolio.json')
loader = DataLoader(data_dir='./data')

# 运行回测
engine = BacktestEngine(config, loader)
results = engine.run_backtest()

# 生成报告
results.generate_report('reports/backtest_report.html')
```

## 📁 项目结构

```
capital_data/
├── src/                      # 源代码
│   ├── __init__.py
│   ├── data_collector.py     # 数据采集模块
│   ├── data_loader.py        # 数据加载模块
│   ├── portfolio_config.py   # 组合配置模块
│   ├── backtest_engine.py    # 回测引擎（待实现）
│   ├── rebalancing.py        # 再平衡策略（待实现）
│   ├── dividend_handler.py   # 红利处理（待实现）
│   ├── performance.py        # 绩效计算（待实现）
│   └── visualization.py      # 可视化模块（待实现）
├── data/                     # 数据目录
│   ├── indices/             # 指数数据
│   ├── dividends/           # 分红数据
│   └── portfolios/          # 组合配置
├── examples/                # 示例脚本
│   ├── 01_download_data.py
│   ├── 02_create_portfolio.py
│   └── 03_analyze_data.py
├── plans/                   # 设计文档
│   └── portfolio_system_design.md
├── requirements.txt         # 依赖包
└── README.md               # 本文件
```

## 📚 示例代码

系统提供了三个示例脚本，帮助您快速上手：

### 示例1: 下载数据
```bash
python examples/01_download_data.py
```
演示如何下载和管理指数数据。

### 示例2: 创建组合
```bash
python examples/02_create_portfolio.py
```
演示如何创建不同类型的投资组合配置。

### 示例3: 分析数据
```bash
python examples/03_analyze_data.py
```
演示如何加载和分析指数数据。

## 🔧 配置说明

### 投资组合配置

投资组合配置文件为JSON格式，包含以下主要参数：

```json
{
  "name": "均衡配置组合",
  "initial_capital": 1000000,
  "start_date": "2014-01-01",
  "end_date": "2024-01-01",
  "indices": {
    "000016.SH": {"name": "上证50", "weight": 0.30},
    "000300.SH": {"name": "沪深300", "weight": 0.30}
  },
  "rebalancing": {
    "frequency": "quarterly",
    "method": "calendar",
    "threshold": 0.05
  },
  "dividend": {
    "reinvest": true
  },
  "costs": {
    "transaction_cost_rate": 0.0003,
    "management_fee_rate": 0.0000
  }
}
```

### 再平衡策略

**日历再平衡** (`method: "calendar"`)
- `frequency: "monthly"` - 每月再平衡
- `frequency: "quarterly"` - 每季度再平衡
- `frequency: "yearly"` - 每年再平衡

**阈值再平衡** (`method: "threshold"`)
- 当任一资产权重偏离目标权重超过设定阈值时触发再平衡
- `threshold: 0.05` - 5%的偏离阈值

## 📊 绩效指标

系统计算以下绩效指标：

### 收益指标
- **总收益率**: 整个回测期间的总收益
- **年化收益率**: 年化后的收益率
- **累计收益**: 随时间的累计收益曲线

### 风险指标
- **年化波动率**: 收益率的标准差（年化）
- **最大回撤**: 从历史最高点的最大跌幅
- **下行波动率**: 仅考虑负收益的波动率

### 风险调整收益指标
- **夏普比率**: (年化收益率 - 无风险利率) / 年化波动率
- **卡玛比率**: 年化收益率 / 最大回撤
- **索提诺比率**: (年化收益率 - 无风险利率) / 下行波动率

### 其他指标
- **胜率**: 正收益交易日占比
- **盈亏比**: 平均盈利 / 平均亏损
- **交易次数**: 再平衡操作次数

## 🛠️ 开发状态

### ✅ 已完成（Phase 1）
- [x] 数据采集模块
- [x] 数据存储结构
- [x] 数据加载模块
- [x] 投资组合配置模块
- [x] 示例脚本
- [x] 设计文档

### 🚧 进行中（Phase 2）
- [ ] 回测引擎核心逻辑
- [ ] 再平衡策略实现
- [ ] 红利处理机制

### 📋 计划中（Phase 3 & 4）
- [ ] 绩效指标计算
- [ ] 数据可视化
- [ ] 报告生成
- [ ] 性能优化
- [ ] 单元测试

## 📖 详细文档

完整的系统设计文档请参阅: [`plans/portfolio_system_design.md`](plans/portfolio_system_design.md:1)

## 🤝 贡献

欢迎提交Issue和Pull Request来帮助改进本项目。

## 📝 许可

本项目采用MIT许可证。

## ⚠️ 免责声明

本系统仅用于学习和研究目的，不构成任何投资建议。历史回测结果不代表未来表现。投资有风险，入市需谨慎。

## 📧 联系方式

如有问题或建议，请通过GitHub Issues联系。

---

**开发进度**: Phase 1 完成 ✅ | Phase 2-4 开发中 🚧

最后更新: 2024-02-07