# Changelog

## [v0.1.1] - 2024-02-12

### Added
- **Logging Module** ([`src/logger.py`](src/logger.py))
  - Professional logging system with file and console output
  - Daily rotating log files stored in `data/logs/`
  - Clean log format without emoji or special characters
  - Automatic log cleanup for old files

- **Configuration File** ([`config/indices_config.json`](config/indices_config.json))
  - Centralized index configuration management
  - Easy to add or modify index definitions
  - Includes all major Chinese A-share indices

- **Test Script** ([`test_logging.py`](test_logging.py))
  - Comprehensive testing for logging functionality
  - Validates configuration loading
  - Tests all core modules

### Changed
- **data_collector.py**
  - Replaced all `print()` statements with logging
  - Now loads index configuration from JSON file
  - Improved error handling and status messages
  - Added configuration file path parameter

- **data_loader.py**
  - Replaced all `print()` statements with logging
  - Fixed pandas deprecation warning (`fillna(method='ffill')` -> `ffill()`)
  - Improved error messages and warnings
  - Better metadata handling

- **portfolio_config.py**
  - Replaced all `print()` statements with logging
  - Enhanced configuration summary output
  - Improved validation messages
  - Added log directory parameter

- **examples/03_analyze_data.py**
  - Removed Unicode special characters (✓, ✗, ⚠) for Windows compatibility
  - Replaced with text markers ([OK], [ERROR], [WARNING])

- **__init__.py**
  - Added logger exports for easier imports

- **README.md**
  - Updated with new features and structure
  - Added documentation for logging and configuration
  - Updated project status and changelog

### Fixed
- Pandas FutureWarning about `fillna(method='ffill')` deprecation
- Unicode encoding issues on Windows systems
- Configuration file loading errors

### Technical Details

#### Logging Implementation
```python
from src.logger import get_logger

logger = get_logger('module_name', log_dir='./logs')
logger.info("Information message")
logger.warning("Warning message")
logger.error("Error message")
```

#### Configuration File Structure
```json
{
  "indices": {
    "000016.SH": {
      "name": "上证50",
      "akshare_symbol": "sh000016",
      "launch_date": "2004-01-02",
      "base_point": 1000,
      "base_date": "2003-12-31"
    }
  },
  "data_source": "akshare",
  "default_start_date": "2014-01-01"
}
```

#### Supported Indices
1. 上证50 (000016.SH)
2. 沪深300 (000300.SH)
3. 中证500 (000905.SH)
4. 中证1000 (000852.SH)
5. 上证红利 (000015.SH) - ✨ NEW
6. 创业板指 (399006.SZ)
7. 科创50 (000688.SH) - ✨ NEW

### Migration Guide

#### For Existing Code
If you have existing code using the old print-based output, no changes are required. The modules will automatically use logging while maintaining backward compatibility.

#### To Enable Logging in Your Code
```python
from src import get_logger

# Initialize logger
logger = get_logger('my_module', log_dir='./data/logs')

# Use logging instead of print
logger.info("Operation completed")
logger.warning("Warning: something needs attention")
logger.error("Error occurred")
```

#### To Customize Index Configuration
Edit [`config/indices_config.json`](config/indices_config.json) to add or modify indices.

### Testing
Run the test script to verify all functionality:
```bash
python test_logging.py
```

Run example scripts:
```bash
python examples/01_download_data.py
python examples/02_create_portfolio.py
python examples/03_analyze_data.py
```

---

## [v0.1.0] - 2024-02-07

### Added
- Initial release with core functionality
- Data collection module
- Data loading module
- Portfolio configuration module
- Basic examples and documentation