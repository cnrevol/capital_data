"""
Test script for logging and configuration functionality
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.data_collector import DataCollector
from src.data_loader import DataLoader
from src.portfolio_config import PortfolioConfig
from src.logger import get_logger

def test_logger():
    """Test basic logging functionality"""
    print("\n" + "="*60)
    print("Testing Logger Module")
    print("="*60)
    
    logger = get_logger('test', log_dir='./data/logs')
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    print("Logger test completed - check ./data/logs/ for log files")

def test_data_collector():
    """Test DataCollector with config file"""
    print("\n" + "="*60)
    print("Testing DataCollector with Config File")
    print("="*60)
    
    collector = DataCollector(
        data_dir='./data',
        config_path='./config/indices_config.json'
    )
    
    # Display supported indices
    print("\nSupported indices:")
    df = collector.get_supported_indices()
    print(df.to_string(index=False))
    
    # Check data availability
    print("\nChecking data availability:")
    availability = collector.check_data_availability()
    print(availability.to_string(index=False))

def test_data_loader():
    """Test DataLoader with logging"""
    print("\n" + "="*60)
    print("Testing DataLoader")
    print("="*60)
    
    loader = DataLoader(data_dir='./data')
    
    # List available indices
    print("\nAvailable indices:")
    indices = loader.list_available_indices()
    if not indices.empty:
        print(indices.to_string(index=False))
    else:
        print("No data files found - please download data first")

def test_portfolio_config():
    """Test PortfolioConfig with logging"""
    print("\n" + "="*60)
    print("Testing PortfolioConfig")
    print("="*60)
    
    config = PortfolioConfig(name="Test Portfolio", log_dir='./data/logs')
    
    # Add indices
    config.add_index('000016.SH', 0.25, '上证50')
    config.add_index('000300.SH', 0.25, '沪深300')
    config.add_index('000852.SH', 0.25, '中证1000')
    config.add_index('000905.SH', 0.25, '中证500')
    
    # Set parameters
    config.set_date_range('2020-01-01', '2023-12-31')
    config.set_rebalancing('quarterly', 'calendar')
    config.set_dividend_policy(True)
    
    # Display summary
    config.print_summary()
    
    # Validate
    is_valid, errors = config.validate()
    if is_valid:
        print("\nConfiguration is valid")
    else:
        print("\nConfiguration has errors:")
        for error in errors:
            print(f"  - {error}")

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("Portfolio Backtesting System - Logging and Configuration Tests")
    print("="*70)
    
    try:
        test_logger()
        test_data_collector()
        test_data_loader()
        test_portfolio_config()
        
        print("\n" + "="*70)
        print("All tests completed successfully")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\nError during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()